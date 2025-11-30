from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from app.auth.dependencies import UserDep
from app.core.db import DbSessionDep
from app.core.exceptions import NotFoundError
from app.fridge.models import Fridge
from app.fridge.services import FridgeService


def get_fridge_service(db: DbSessionDep) -> FridgeService:
    return FridgeService(db)


FridgeServiceDep = Annotated[FridgeService, Depends(get_fridge_service)]


async def get_fridge(db: DbSessionDep, user: UserDep) -> Fridge:
    result = await db.execute(select(Fridge).where(Fridge.user_id == user.id))
    fridge = result.scalar_one_or_none()
    if fridge is None:
        raise NotFoundError("Fridge not found")
    return fridge


FridgeDep = Annotated[Fridge, Depends(get_fridge)]
