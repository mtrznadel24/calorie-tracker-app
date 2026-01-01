from collections.abc import Sequence
from datetime import date

from fastapi import APIRouter

from app.auth.dependencies import UserDep
from app.meal.dependencies import MealServiceDep
from app.meal.models import MealLog
from app.meal.schemas import (
    MealLogQuickCreate,
    MealLogRead,
)

router = APIRouter(prefix="/meals", tags=["meals"])


@router.post("/quick", response_model=MealLogRead)
async def add_meal_log_quick(
    meal_service: MealServiceDep, user: UserDep, meal_in: MealLogQuickCreate
) -> MealLog:
    return await meal_service.create_meal_log_quick(user.id, data=meal_in)


@router.get("/{meal_id}", response_model=MealLogRead)
async def read_meal_log_by_id(
    meal_service: MealServiceDep, user: UserDep, meal_id: int
) -> MealLog:
    return await meal_service.get_meal_log_by_id(user.id, meal_id=meal_id)


@router.get("/{meal_date}/meal-logs", response_model=Sequence[MealLogRead])
async def read_meal_logs(meal_service: MealServiceDep, user: UserDep, meal_date: date):
    return await meal_service.get_meal_logs(user.id, meal_date=meal_date)


@router.delete("/{meal_id}", response_model=MealLogRead)
async def delete_meal_log(
    meal_service: MealServiceDep, user: UserDep, meal_id: int
) -> MealLog:
    return await meal_service.delete_meal(user.id, meal_id=meal_id)
