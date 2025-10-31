from fastapi import APIRouter

from app.core.db import DbSessionDep
from app.core.security import UserDep
from app.schemas.user import UserRead, UserUpdate, UserUpdateEmail, UserUpdatePassword
from app.services.user import update_user, change_user_email, change_user_password

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserRead)
async def read_current_user(user: UserDep):
    return user


@router.put('/me', response_model=UserRead)
async def update_user_profile(db: DbSessionDep, user: UserDep, data: UserUpdate):
    return update_user(db, user.id, data)

@router.put("/me/email", response_model=UserRead)
async def update_user_email(db: DbSessionDep, user: UserDep, data: UserUpdateEmail):
    return change_user_email(db, user.id, data)

@router.put("/me/password", response_model=UserRead)
async def update_user_password(db: DbSessionDep, user: UserDep, data: UserUpdatePassword):
    return change_user_password(db, user.id, data)