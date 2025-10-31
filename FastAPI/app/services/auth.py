from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS ,ALGORITHM, SECRET_KEY
from app.core.db import DbSessionDep
from app.core.exceptions import UnauthorizedError
from app.core.redis_session import delete_refresh_token, is_refresh_token_valid, add_refresh_token
from app.core.security import TokenDep, verify_password, create_access_token, create_refresh_token
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user import create_user


def authenticate_user(email: str, password: str, db: DbSessionDep) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise UnauthorizedError("Invalid credentials")
    return user

async def get_current_user(token: TokenDep, db: DbSessionDep):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise UnauthorizedError("Token payload missing")
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except JWTError:
        raise UnauthorizedError("Invalid or expired token")


def register_user(user: UserCreate, db: DbSessionDep):
    user = create_user(db, user)
    access_token = create_access_token(user.username, user.id)
    refresh_token, jti = create_refresh_token(user.username, user.id)
    return access_token, refresh_token


def login_user(form_data: OAuth2PasswordRequestForm, db: DbSessionDep):
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token = create_access_token(user.username, user.id)
    refresh_token, jti = create_refresh_token(user.username, user.id)
    return access_token, refresh_token


def refresh_tokens(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise UnauthorizedError("Invalid or expired token")
    jti = payload["jti"]
    if not is_refresh_token_valid(jti):
        raise UnauthorizedError("Invalid refresh token")
    username = payload["sub"]
    user_id = payload["id"]
    delete_refresh_token(jti)
    access_token = create_access_token(username, user_id)
    new_refresh_token, new_jti = create_refresh_token(username, user_id)
    add_refresh_token(new_jti, user_id, REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600)
    return access_token, new_refresh_token


def logout_user(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        jti = payload.get("jti")
        if jti:
            delete_refresh_token(jti)
    except JWTError:
        pass