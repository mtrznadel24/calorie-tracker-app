from typing import Annotated

from fastapi import Depends

from app.auth.repositories import TokenRepository
from app.auth.services import AuthService
from app.core.db import DbSessionDep
from app.core.redis_session import RedisDep
from app.user.dependencies import UserServiceDep


def get_token_repository(redis: RedisDep) -> TokenRepository:
    return TokenRepository(redis)


RedisDep = Annotated[TokenRepository, Depends(get_token_repository)]


def get_auth_service(
    db: DbSessionDep, user_service: UserServiceDep, redis: RedisDep
) -> AuthService:
    return AuthService(db, user_service, redis)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
