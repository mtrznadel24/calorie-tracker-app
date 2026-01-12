from fastapi import APIRouter, Depends, Response, status

from app.auth.dependencies import UserDep
from app.core.rate_limiting import rate_limiter as RateLimiter
from app.user.dependencies import UserServiceDep
from app.user.models import User
from app.user.schemas import (
    DeleteUserData,
    UserRead,
    UserUpdate,
    UserUpdateEmail,
    UserUpdatePassword,
)

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserRead)
async def read_current_user(user_service: UserServiceDep, user: UserDep) -> User:
    return await user_service.get_current_user(user)


@router.put("/me", response_model=UserRead)
async def update_user_profile(
    user_service: UserServiceDep, user: UserDep, data: UserUpdate
) -> User:
    await user_service.update_user(user.id, data)
    return await user_service.get_current_user(user)


@router.put("/me/email", response_model=UserRead)
async def update_user_email(
    user_service: UserServiceDep, user: UserDep, data: UserUpdateEmail
) -> User:
    await user_service.change_user_email(user.id, data)
    return await user_service.get_current_user(user)


@router.put("/me/password", response_model=UserRead)
async def update_user_password(
    user_service: UserServiceDep,
    user: UserDep,
    data: UserUpdatePassword,
    _: int = Depends(RateLimiter(times=5, seconds=300)),
) -> User:
    return await user_service.change_user_password(user.id, data)


@router.delete("/me")
async def delete_user(
    user_service: UserServiceDep, user: UserDep, data: DeleteUserData
):
    await user_service.delete_user(user.id, data)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
