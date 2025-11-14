from typing import Annotated

from fastapi import Depends

from app.core.db import DbSessionDep
from app.fridge.services import FridgeService


def get_fridge_service(db: DbSessionDep) -> FridgeService:
    return FridgeService(db)


FridgeServiceDep = Annotated[FridgeService, Depends(get_fridge_service)]
