from typing import Type

from pyasn1.type.univ import Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import UserScopedRepository, BaseRepository
from app.core.enums import NutrientType, nutrient_type_list
from app.meal.models import Meal, MealType, MealIngredient, MealIngredientDetails
from datetime import date


class MealRepository(UserScopedRepository[Meal]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Meal)

    async def get_meal_by_date_and_type(self, user_id: int, date: date, type: MealType) -> Meal:
        result = await self.db.execute(
            select(Meal)
            .where(Meal.user_id == user_id)
            .where(Meal.date == date)
            .where(Meal.type == type)
        )
        return result.scalar_one_or_none()

    async def get_meal_nutrient_sum(self, user_id: int, meal_id: int, nutrient_type: NutrientType) -> float:
        stmt = (
            select(
                func.sum(
                    (
                            getattr(MealIngredientDetails, nutrient_type.value + "_100g")
                            * MealIngredient.weight
                    )
                    / 100
                )
            )
            .select_from(MealIngredient)
            .join(MealIngredientDetails)
            .join(Meal)
            .where(Meal.user_id == user_id, Meal.id == meal_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0.0

    async def get_meal_macro(
        self, user_id: int, meal_id: int
    ) -> dict[str, float]:
        stmt = (
            select(
                *[
                    func.sum(
                        (
                            getattr(MealIngredientDetails, field.value + "_100g")
                            * MealIngredient.weight
                        )
                        / 100
                    ).alias(field.value)
                    for field in nutrient_type_list
                ]
            )
            .select_from(MealIngredient)
            .join(MealIngredientDetails)
            .join(Meal)
            .where(Meal.user_id == user_id, Meal.id == meal_id)
        )
        result = await self.db.execute(stmt)
        row = result.one_or_none()
        return {field.value: getattr(row, field.value) or 0.0 for field in nutrient_type_list}

    async def get_meals_nutrient_sum_for_day(
        self, user_id: int, meal_date: date, nutrient_type: NutrientType
    ) -> float:
        stmt = (
            select(
                func.sum(
                    (
                        getattr(MealIngredientDetails, nutrient_type.value + "_100g")
                        * MealIngredient.weight
                    )
                    / 100
                )
            )
            .select_from(MealIngredient)
            .join(MealIngredientDetails)
            .join(Meal)
            .where(Meal.user_id == user_id, Meal.date == meal_date)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0.0

    async def get_macro_for_day(
        self, user_id: int, meal_date: date
    ) -> dict[str, float]:
        stmt = (
            select(
                *[
                    func.sum(
                        (
                            getattr(MealIngredientDetails, field.value + "_100g")
                            * MealIngredient.weight
                        )
                        / 100
                    ).alias(field.value)
                    for field in nutrient_type_list
                ]
            )
            .select_from(MealIngredient)
            .join(MealIngredientDetails)
            .join(Meal)
            .where(Meal.user_id == user_id, Meal.date == meal_date)
        )
        result = await self.db.execute(stmt)
        row = result.one_or_none()
        return {field.value: getattr(row, field.value) or 0.0 for field in nutrient_type_list}


class MealIngredientRepository(BaseRepository[MealIngredient]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, MealIngredient)

    async def get_meal_ingredients(self, meal_id: int) -> Sequence[MealIngredient]:
        result = await self.db.execute(
            select(MealIngredient).where(MealIngredient.meal_id == meal_id)
        )
        return result.scalars().all()

    async def get_meal_ingredient_by_id(self, meal_id: int, ingredient_id: int) -> MealIngredient:
        result = await self.db.execute(
            select(MealIngredient).where(
                MealIngredient.id == ingredient_id, MealIngredient.meal_id == meal_id
            )
        )
        return result.scalar_one_or_none()