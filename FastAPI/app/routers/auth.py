from fastapi import APIRouter, Depends, Cookie, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.db import DbSessionDep
from app.core.exceptions import UnauthorizedError
from app.schemas.auth import Token
from app.schemas.user import UserCreate
from app.services.auth import refresh_tokens, logout_user, register_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=201)
def register_endpoint(response: Response, user_in: UserCreate, db: DbSessionDep):
    access_token, refresh_token = register_user(user_in, db)
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
def login_endpoint(response: Response, db: DbSessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    access_token, refresh_token = login_user(form_data, db)
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
def refresh_endpoint(response: Response, refresh_token: str = Cookie(...)):
    try:
        access_token, new_refresh_token = refresh_tokens(refresh_token=refresh_token)
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
def logout_endpoint(refresh_token: str = Cookie(...)):
    return logout_user(refresh_token)



