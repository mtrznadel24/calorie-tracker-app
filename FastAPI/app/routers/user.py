from fastapi import APIRouter

from app.core.security import UserDep
from app.schemas.user import UserRead

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserRead)
async def read_current_user(user: UserDep):
    return user
