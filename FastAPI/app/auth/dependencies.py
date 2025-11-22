from typing import Annotated

from fastapi import Depends

from app.auth.repositories import TokenRepository
from app.auth.services import AuthService
from app.core.db import DbSessionDep
from app.core.exceptions import UnauthorizedError
from app.core.redis_session import RedisDep
from app.core.security import get_token_payload, TokenDep
from app.user.dependencies import UserServiceDep
from app.user.models import User


def get_token_repository(redis: RedisDep) -> TokenRepository:
    return TokenRepository(redis)


TokenRepositoryDep = Annotated[TokenRepository, Depends(get_token_repository)]


def get_auth_service(
    db: DbSessionDep, user_service: UserServiceDep, redis: TokenRepositoryDep
) -> AuthService:
    return AuthService(db, user_service, redis)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(auth_service: AuthServiceDep, token: TokenDep) -> User:
    payload = get_token_payload(token)
    username: str = payload.get("sub")
    user_id: int = payload.get("id")
    if username is None or user_id is None:
        raise UnauthorizedError("Token payload missing")
    user = await auth_service.repo.get_by_id(user_id)
    if user is None:
        raise UnauthorizedError("User not found")
    return user

UserDep = Annotated[User, Depends(get_current_user)]