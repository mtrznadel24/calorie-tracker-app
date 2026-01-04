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

    async def create_meal_logs_from_fridge_meal(
        self, user_id, fridge_id: int, data: MealLogFromProductCreate
    ) -> Sequence[MealLog]:
        meal = await self.fridge_meal_repo.get_fridge_meal_entity(
            fridge_id, data.fridge_meal_id
        )

        meal_weight = sum(i.weight for i in meal.ingredients)
        scale_factor = data.weight / meal_weight
        logs = []
        for ingredient in meal.ingredients:
            product = ingredient.fridge_product
            scaled_weight = ingredient.weight * scale_factor
            ratio = scaled_weight / 100.0
            logs.append(
                MealLog(
                    user_id=user_id,
                    date=data.date,
                    type=data.type,
                    weight=round(scaled_weight, 1),
                    name=product.product_name,
                    calories=round(product.calories_100g * ratio, 0),
                    proteins=round(product.proteins_100g * ratio, 1),
                    fats=round(product.fats_100g * ratio, 1),
                    carbs=round(product.carbs_100g * ratio, 1),
                )
            )
        self.repo.add_all_products(logs)
        await self.repo.commit_or_conflict()
        for log in logs:
            await self.repo.refresh(log)
        return logs

    async def get_meal_log_by_id(self, user_id: int, meal_id: int) -> MealLog:
        return await self.repo.get_by_id_for_user(user_id, meal_id)

    async def get_meal_logs(
        self, user_id: int, meal_date: datetime.date
    ) -> Sequence[MealLogRead]:
        return await self.repo.get_meal_logs(user_id, meal_date)

    async def update_meal_log_name(self, user_id, log_id: int, new_name: str):
        log = await self.repo.get_by_id_for_user(user_id, log_id)
        log.name = new_name
        await self.repo.commit_or_conflict()
        await self.repo.refresh(log)
        return log

    async def update_meal_log_weight(self, user_id, log_id: int, new_weight: float):
        log = await self.repo.get_by_id_for_user(user_id, log_id)
        ratio = new_weight / log.weight
        log.weight = new_weight
        log.calories *= ratio
        log.proteins *= ratio
        log.fats *= ratio
        log.carbs *= ratio
        await self.repo.commit_or_conflict()
        await self.repo.refresh(log)
        return log

    async def delete_meal_log(self, user_id: int, meal_id: int) -> MealLog:
        return await self.repo.delete_by_id_for_user(user_id, meal_id)
