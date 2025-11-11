from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repositories import AuthRepository, TokenRepository
from app.core.exceptions import UnauthorizedError

from app.core.security import (
    TokenDep,
    create_access_token,
    create_refresh_token,
    get_token_payload,
    verify_password,
)
from app.user.models import User
from app.user.schemas import UserCreate
from app.user.services import UserService


class AuthService:
    def __init__(self, db: AsyncSession, user_service: UserService, token_repo: TokenRepository):
        self.repo = AuthRepository(db)
        self.user_service = user_service
        self.token_repo = token_repo

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid credentials")
        return user


    async def get_current_user(self, token: TokenDep) -> User:
        payload = get_token_payload(token)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise UnauthorizedError("Token payload missing")
        user = await self.repo.get_by_id(user_id)
        if user is None:
            raise UnauthorizedError("User not found")
        return user


    async def register_user(self, user: UserCreate) -> tuple[str, str]:
        user = await self.user_service.create_user(user)
        access_token = create_access_token(user.username, user.id)
        refresh_token, jti = create_refresh_token(user.username, user.id)
        await self.token_repo.add_refresh_token_to_redis(jti, user.id)
        return access_token, refresh_token


    async def login_user(
            self,
            form_data: OAuth2PasswordRequestForm
    ) -> tuple[str, str]:
        user = await self.authenticate_user(form_data.username, form_data.password)
        access_token = create_access_token(user.username, user.id)
        refresh_token, jti = create_refresh_token(user.username, user.id)
        await self.token_repo.add_refresh_token_to_redis(jti, user.id)
        return access_token, refresh_token


    async def refresh_tokens(self, refresh_token: str) -> tuple[str, str]:
        payload = get_token_payload(refresh_token)
        jti = payload["jti"]
        if not await self.token_repo.is_refresh_token_valid(jti):
            raise UnauthorizedError("Invalid refresh token")
        username = payload["sub"]
        user_id = payload["id"]
        if not username or not user_id:
            raise UnauthorizedError("Token payload missing")
        await self.token_repo.delete_refresh_token_from_redis(jti)
        access_token = create_access_token(username, user_id)
        new_refresh_token, new_jti = create_refresh_token(username, user_id)
        await self.token_repo.add_refresh_token_to_redis(new_jti, user_id)
        return access_token, new_refresh_token


    async def logout_user(self, refresh_token: str) -> None:
        payload = get_token_payload(refresh_token)
        jti = payload.get("jti")
        if jti:
            await self.token_repo.delete_refresh_token_from_redis(jti)
