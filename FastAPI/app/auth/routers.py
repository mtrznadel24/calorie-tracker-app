from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.depedencies import AuthServiceDep
from app.auth.schemas import Token
from app.core.exceptions import UnauthorizedError
from app.user.schemas import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=201)
async def register_endpoint(
    auth_service: AuthServiceDep, response: Response, user_in: UserCreate
) -> Token:
    access_token, refresh_token = await auth_service.register_user(user_in)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600 * 24 * 7,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/token", response_model=Token, status_code=200)
async def login_endpoint(
    auth_service: AuthServiceDep,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    access_token, refresh_token = await auth_service.login_user(form_data)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600 * 24 * 7,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/refresh", response_model=Token, status_code=200)
async def refresh_endpoint(
    auth_service: AuthServiceDep, response: Response, refresh_token: str = Cookie(...)
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
        return Token(access_token=access_token, token_type="bearer")
    except UnauthorizedError:
        response.delete_cookie(key="refresh_token")
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout", status_code=200)
async def logout_endpoint(auth_service: AuthServiceDep, response: Response, refresh_token: str = Cookie(...)):
    response.delete_cookie(key="refresh_token")
    return await auth_service.logout_user(refresh_token)
