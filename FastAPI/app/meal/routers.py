from collections.abc import Sequence
from datetime import date

from fastapi import APIRouter

from app.auth.dependencies import UserDep
from app.fridge.dependencies import FridgeDep
from app.meal.dependencies import MealServiceDep
from app.meal.models import MealLog
from app.meal.schemas import (
    MealLogFromProductCreate,
    MealLogQuickCreate,
    MealLogRead,
)

router = APIRouter(prefix="/meals", tags=["meals"])


@router.post("/quick", response_model=MealLogRead)
async def add_meal_log_quick(
    meal_service: MealServiceDep, user: UserDep, log_in: MealLogQuickCreate
) -> MealLog:
    return await meal_service.create_meal_log_quick(user.id, data=log_in)


@router.post("/from-product", response_model=MealLogRead)
async def add_meal_log_from_fridge_product(
    meal_service: MealServiceDep,
    user: UserDep,
    fridge: FridgeDep,
    log_in: MealLogFromProductCreate,
):
    return await meal_service.create_meal_log_from_fridge_product(
        user.id, fridge.id, data=log_in
    )


@router.get("/{log_id}", response_model=MealLogRead)
async def read_meal_log_by_id(
    meal_service: MealServiceDep, user: UserDep, log_id: int
) -> MealLog:
    return await meal_service.get_meal_log_by_id(user.id, meal_id=log_id)


@router.get("/{log_date}/meal-logs", response_model=Sequence[MealLogRead])
async def read_meal_logs(meal_service: MealServiceDep, user: UserDep, log_date: date):
    return await meal_service.get_meal_logs(user.id, meal_date=log_date)


@router.delete("/{log_id}", response_model=MealLogRead)
async def delete_meal_log(
    meal_service: MealServiceDep, user: UserDep, log_id: int
) -> MealLog:
    return await meal_service.delete_meal_log(user.id, meal_id=log_id)
