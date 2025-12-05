import logging
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_token_payload,
    verify_password,
)
from app.user.models import User
from app.user.schemas import UserCreate
from app.user.services import UserService

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: AsyncSession, token_repo):
        self.user_service = UserService(db)
        self.token_repo = token_repo

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.user_service.repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            logger.warning("Failed login attempt for email=%s", email)
            raise UnauthorizedError("Invalid credentials")
        return user

    async def register_user(self, user: UserCreate) -> tuple[str, str]:
        try:
            user = await self.user_service.create_user(user)
        except UnauthorizedError:
            logger.warning("Failed to register user email=%s", user.email)
            raise
        access_token = create_access_token(user.username, user.id)
        refresh_token, jti = create_refresh_token(user.username, user.id)
        await self.token_repo.add_refresh_token_to_redis(jti, user.id)
        return access_token, refresh_token

    async def login_user(self, form_data: OAuth2PasswordRequestForm) -> tuple[str, str]:
        user = await self.authenticate_user(form_data.username, form_data.password)
        access_token = create_access_token(user.username, user.id)
        refresh_token, jti = create_refresh_token(user.username, user.id)
        await self.token_repo.add_refresh_token_to_redis(jti, user.id)
        return access_token, refresh_token

    async def refresh_tokens(self, refresh_token: str) -> tuple[str, str]:
        payload = get_token_payload(refresh_token)
        jti = payload["jti"]
        if not await self.token_repo.is_refresh_token_valid(jti):
            logger.warning("Invalid refresh token jti=%s", jti)
            raise UnauthorizedError("Invalid refresh token")
        username = payload["sub"]
        user_id = payload["id"]
        if not username or not user_id:
            raise UnauthorizedError("Token payload missing")
        await self.token_repo.delete_refresh_token_from_redis(jti)
        access_token = create_access_token(username, user_id)
        new_refresh_token, new_jti = create_refresh_token(username, user_id)
        await self.token_repo.add_refresh_token_to_redis(new_jti, user_id)
        logger.info("Refresh token rotated for user_id=%s", user_id)
        return access_token, new_refresh_token

    async def logout_user(self, refresh_token: str) -> None:
        payload = get_token_payload(refresh_token)
        jti = payload.get("jti")
        if jti:
            deleted = await self.token_repo.delete_refresh_token_from_redis(jti)
            if deleted:
                logger.info("User logged out, refresh token jti=%s removed", jti)
            else:
                logger.warning("Logout attempted with non-existent token jti=%s", jti)
