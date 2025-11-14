from typing import Annotated

from fastapi import Depends

from app.core.db import DbSessionDep
from app.meal.services import MealService


def get_meal_service(db: DbSessionDep) -> MealService:
    return MealService(db)


MealServiceDep = Annotated[MealService, Depends(get_meal_service)]
