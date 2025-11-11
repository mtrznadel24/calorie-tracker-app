from typing import Annotated

from fastapi import Depends

from app.core.db import DbSessionDep
from app.user.services import UserService


def get_user_service(db: DbSessionDep) -> UserService:
    return UserService(db)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]