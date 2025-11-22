from fastapi import APIRouter

from app.auth.dependencies import UserDep
from app.user.dependencies import UserServiceDep
from app.user.models import User
from app.user.schemas import UserRead, UserUpdate, UserUpdateEmail, UserUpdatePassword

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserRead)
async def read_current_user(user: UserDep) -> User:
    return user


@router.put("/me", response_model=UserRead)
async def update_user_profile(
    user_service: UserServiceDep, user: UserDep, data: UserUpdate
) -> User:
    return await user_service.update_user(user.id, data)


@router.put("/me/email", response_model=UserRead)
async def update_user_email(
    user_service: UserServiceDep, user: UserDep, data: UserUpdateEmail
) -> User:
    return await user_service.change_user_email(user.id, data)


@router.put("/me/password", response_model=UserRead)
async def update_user_password(
    user_service: UserServiceDep, user: UserDep, data: UserUpdatePassword
) -> User:
    return await user_service.change_user_password(user.id, data)
