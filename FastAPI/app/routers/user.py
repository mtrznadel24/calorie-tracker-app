from fastapi import APIRouter

from app.core.db import DbSessionDep
from app.core.security import UserDep
from app.models import User
from app.schemas.user import UserRead, UserUpdate, UserUpdateEmail, UserUpdatePassword
from app.services.user import change_user_email, change_user_password, update_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserRead)
async def read_current_user(user: UserDep) -> User:
    return user


@router.put("/me", response_model=UserRead)
async def update_user_profile(
    db: DbSessionDep, user: UserDep, data: UserUpdate
) -> User:
    return await update_user(db, user.id, data)


@router.put("/me/email", response_model=UserRead)
async def update_user_email(
    db: DbSessionDep, user: UserDep, data: UserUpdateEmail
) -> User:
    return await change_user_email(db, user.id, data)


@router.put("/me/password", response_model=UserRead)
async def update_user_password(
    db: DbSessionDep, user: UserDep, data: UserUpdatePassword
) -> User:
    return await change_user_password(db, user.id, data)
