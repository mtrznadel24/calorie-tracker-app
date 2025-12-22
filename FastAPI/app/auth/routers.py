import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependencies import AuthServiceDep
from app.auth.schemas import RefreshTokenRequest, TokenPair
from app.core.exceptions import UnauthorizedError
from app.core.rate_limiting import check_and_record_login_attempt, clear_login_attempts
from app.core.rate_limiting import rate_limiter as RateLimiter
from app.core.redis_session import RedisDep
from app.user.schemas import UserCreate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenPair, status_code=201)
async def register(
    auth_service: AuthServiceDep,
    user_in: UserCreate,
    _: int = Depends(RateLimiter(times=5, seconds=300)),
) -> TokenPair:
    logger.info("register attempt for email=%s", user_in.email)
    access_token, refresh_token = await auth_service.register_user(user_in)

    # Only for web apps
    # response.set_cookie(
    #     key="refresh_token",
    #     value=refresh_token,
    #     httponly=True,
    #     secure=True,
    #     samesite="lax",
    #     max_age=3600 * 24 * 7,
    # )

    logger.info("User registered successfully email=%s", user_in.email)
    return TokenPair(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/login", response_model=TokenPair, status_code=200)
async def login(
    auth_service: AuthServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    redis: RedisDep,
    _: int = Depends(RateLimiter(times=10, seconds=60)),
) -> TokenPair:
    logger.info("Login attempt for username=%s", form_data.username)
    await check_and_record_login_attempt(form_data.username, redis)

    access_token, refresh_token = await auth_service.login_user(form_data)

    await clear_login_attempts(form_data.username, redis)

    # Only for web apps
    # response.set_cookie(
    #     key="refresh_token",
    #     value=refresh_token,
    #     httponly=True,
    #     secure=True,
    #     samesite="lax",
    #     max_age=3600 * 24 * 7,
    # )

    logger.info("Login successful for username=%s", form_data.username)
    return TokenPair(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/refresh", response_model=TokenPair, status_code=200)
async def refresh(
    auth_service: AuthServiceDep,
    refresh_token_in: RefreshTokenRequest,
    _: int = Depends(RateLimiter(times=10, seconds=60)),
) -> TokenPair:
    try:
        access_token, new_refresh_token = await auth_service.refresh_tokens(
            refresh_token=refresh_token_in.refresh_token
        )

        # Only for web apps
        # response.set_cookie(
        #     key="refresh_token",
        #     value=new_refresh_token,
        #     httponly=True,
        #     secure=True,
        #     samesite="lax",
        #     max_age=3600 * 24 * 7,
        # )

        logger.info("Token refreshed successfully")
        return TokenPair(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )
    except UnauthorizedError:
        # response.delete_cookie(key="refresh_token")
        logger.warning("Invalid refresh token used")
        raise HTTPException(status_code=401, detail="Invalid refresh token") from None


@router.post("/logout", status_code=200)
async def logout(auth_service: AuthServiceDep, refresh_token_in: RefreshTokenRequest):
    # response.delete_cookie(key="refresh_token")
    return await auth_service.logout_user(refresh_token_in.refresh_token)
