import logging
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependencies import AuthServiceDep
from app.auth.schemas import Token
from app.core.exceptions import UnauthorizedError
from app.core.rate_limiting import check_and_record_login_attempt, clear_login_attempts
from app.core.rate_limiting import rate_limiter as RateLimiter
from app.core.redis_session import RedisDep
from app.user.schemas import UserCreate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=201)
async def register(
    auth_service: AuthServiceDep,
    response: Response,
    user_in: UserCreate,
    _: int = Depends(RateLimiter(times=5, seconds=300)),
) -> Token:
    logger.info("register attempt for email=%s", user_in.email)
    access_token, refresh_token = await auth_service.register_user(user_in)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600 * 24 * 7,
    )
    logger.info("User registered successfully email=%s", user_in.email)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login", response_model=Token, status_code=200)
async def login(
    auth_service: AuthServiceDep,
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    redis: RedisDep,
    _: int = Depends(RateLimiter(times=10, seconds=60)),
) -> Token:
    logger.info("Login attempt for username=%s", form_data.username)
    await check_and_record_login_attempt(form_data.username, redis)

    access_token, refresh_token = await auth_service.login_user(form_data)

    await clear_login_attempts(form_data.username, redis)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600 * 24 * 7,
    )
    logger.info("Login successful for username=%s", form_data.username)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/refresh", response_model=Token, status_code=200)
async def refresh(
    auth_service: AuthServiceDep,
    response: Response,
    refresh_token: str = Cookie(...),
    _: int = Depends(RateLimiter(times=10, seconds=60)),
) -> Token:
    try:
        access_token, new_refresh_token = await auth_service.refresh_tokens(
            refresh_token=refresh_token
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600 * 24 * 7,
        )
        logger.info("Token refreshed successfully")
        return Token(access_token=access_token, token_type="bearer")
    except UnauthorizedError:
        response.delete_cookie(key="refresh_token")
        logger.warning("Invalid refresh token used")
        raise HTTPException(status_code=401, detail="Invalid refresh token") from None


@router.post("/logout", status_code=200)
async def logout(
    auth_service: AuthServiceDep, response: Response, refresh_token: str = Cookie(...)
):
    response.delete_cookie(key="refresh_token")
    return await auth_service.logout_user(refresh_token)
