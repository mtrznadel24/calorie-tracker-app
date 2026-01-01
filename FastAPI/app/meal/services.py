import datetime
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.fridge.repositories import FridgeMealRepository, FridgeProductRepository
from app.meal.models import MealLog
from app.meal.repositories import MealRepository
from app.meal.schemas import (
    MealLogFromProductCreate,
    MealLogQuickCreate,
    MealLogRead,
)

# Meal


class MealService:
    def __init__(self, db: AsyncSession):
        self.repo = MealRepository(db)
        self.fridge_product_repo = FridgeProductRepository(db)
        self.fridge_meal_repo = FridgeMealRepository(db)

    async def create_meal_log_quick(
        self, user_id: int, data: MealLogQuickCreate
    ) -> MealLog:
        meal = MealLog(**data.model_dump(exclude_unset=True), user_id=user_id)
        self.repo.add(meal)
        await self.repo.commit_or_conflict()
        return await self.repo.refresh_and_return(meal)

    async def create_meal_log_from_fridge_product(
        self, user_id, fridge_id: int, data: MealLogFromProductCreate
    ) -> MealLog:
        product = await self.fridge_product_repo.get_fridge_product(
            fridge_id, data.fridge_product_id
        )

        ratio = data.weight / 100.0
        log = MealLog(
            user_id=user_id,
            date=data.date,
            type=data.type,
            weight=data.weight,
            name=product.product_name,
            calories=round(product.calories_100g * ratio, 0),
            proteins=round(product.proteins_100g * ratio, 1),
            fats=round(product.fats_100g * ratio, 1),
            carbs=round(product.carbs_100g * ratio, 1),
        )
        self.repo.add(log)
        await self.repo.commit_or_conflict()
        return await self.repo.refresh_and_return(log)

    async def get_meal_log_by_id(self, user_id: int, meal_id: int) -> MealLog:
        return await self.repo.get_by_id_for_user(user_id, meal_id)

    async def get_meal_logs(
        self, user_id: int, meal_date: datetime.date
    ) -> Sequence[MealLogRead]:
        return await self.repo.get_meal_logs(user_id, meal_date)

    async def delete_meal_log(self, user_id: int, meal_id: int) -> MealLog:
        return await self.repo.delete_by_id_for_user(user_id, meal_id)
