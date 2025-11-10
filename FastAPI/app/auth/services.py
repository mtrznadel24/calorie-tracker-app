from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError
from app.core.redis_session import (
    add_refresh_token_to_redis,
    delete_refresh_token_from_redis,
    is_refresh_token_valid,
)
from app.core.security import (
    TokenDep,
    create_access_token,
    create_refresh_token,
    get_token_payload,
    verify_password,
)
from app.user.models import User
from app.user.schemas import UserCreate
from app.user.services import create_user


async def authenticate_user(email: str, password: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise UnauthorizedError("Invalid credentials")
    return user


async def get_current_user(token: TokenDep, db: AsyncSession) -> User:
    payload = get_token_payload(token)
    username: str = payload.get("sub")
    user_id: int = payload.get("id")
    if username is None or user_id is None:
        raise UnauthorizedError("Token payload missing")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise UnauthorizedError("User not found")
    return user


async def register_user(user: UserCreate, db: AsyncSession) -> tuple[str, str]:
    user = await create_user(db, user)
    access_token = create_access_token(user.username, user.id)
    refresh_token, jti = create_refresh_token(user.username, user.id)
    await add_refresh_token_to_redis(jti, user.id)
    return access_token, refresh_token


async def login_user(
    form_data: OAuth2PasswordRequestForm, db: AsyncSession
) -> tuple[str, str]:
    user = await authenticate_user(form_data.username, form_data.password, db)
    access_token = create_access_token(user.username, user.id)
    refresh_token, jti = create_refresh_token(user.username, user.id)
    await add_refresh_token_to_redis(jti, user.id)
    return access_token, refresh_token


async def refresh_tokens(refresh_token: str) -> tuple[str, str]:
    payload = get_token_payload(refresh_token)
    jti = payload["jti"]
    if not await is_refresh_token_valid(jti):
        raise UnauthorizedError("Invalid refresh token")
    username = payload["sub"]
    user_id = payload["id"]
    if not username or not user_id:
        raise UnauthorizedError("Token payload missing")
    await delete_refresh_token_from_redis(jti)
    access_token = create_access_token(username, user_id)
    new_refresh_token, new_jti = create_refresh_token(username, user_id)
    await add_refresh_token_to_redis(new_jti, user_id)
    return access_token, new_refresh_token


async def logout_user(refresh_token: str):
    payload = get_token_payload(refresh_token)
    jti = payload.get("jti")
    if jti:
        await delete_refresh_token_from_redis(jti)
