from collections.abc import Sequence
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository, UserScopedRepository
from app.core.exceptions import NotFoundError
from app.meal.models import Meal, MealIngredient, MealIngredientDetails, MealType
from app.utils.enums import NutrientType, nutrient_type_list


class MealRepository(UserScopedRepository[Meal]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Meal)

    async def get_meal_by_date_and_type(
        self, user_id: int, date: date, type: MealType
    ) -> Meal | None:
        result = await self.db.execute(
            select(Meal)
            .where(Meal.user_id == user_id)
            .where(Meal.date == date)
            .where(Meal.type == type)
        )
        return result.scalar_one_or_none()

    async def get_meal_nutrient_sum(
        self, user_id: int, meal_id: int, nutrient_type: NutrientType
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
            .where(Meal.user_id == user_id, Meal.id == meal_id)
        )
        result = await self.db.execute(stmt)
        value = result.scalar() or 0.0
        if nutrient_type == NutrientType.CALORIES:
            return round(value, 0)
        else:
            return round(value, 1)

    async def get_meal_macro(self, user_id: int, meal_id: int) -> dict[str, float]:
        stmt = (
            select(
                *[
                    func.sum(
                        (
                            getattr(MealIngredientDetails, field.value + "_100g")
                            * MealIngredient.weight
                        )
                        / 100
                    ).label(field.value)
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
        return {
            field.value: round(
                getattr(row, field.value) or 0.0,
                0 if field == NutrientType.CALORIES else 1,
            )
            for field in nutrient_type_list
        }

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
        value = result.scalar() or 0.0
        if nutrient_type == NutrientType.CALORIES:
            return round(value, 0)
        else:
            return round(value, 1)

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
                    ).label(field.value)
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
        return {
            field.value: round(
                getattr(row, field.value) or 0.0,
                0 if field == NutrientType.CALORIES else 1,
            )
            for field in nutrient_type_list
        }


class MealIngredientRepository(BaseRepository[MealIngredient]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, MealIngredient)

    async def get_meal_ingredients(self, meal_id: int) -> Sequence[MealIngredient]:
        result = await self.db.execute(
            select(MealIngredient).where(MealIngredient.meal_id == meal_id)
        )
        return result.scalars().all()

    async def get_meal_ingredient_by_id(
        self, meal_id: int, ingredient_id: int
    ) -> MealIngredient:
        result = await self.db.execute(
            select(MealIngredient).where(
                MealIngredient.id == ingredient_id, MealIngredient.meal_id == meal_id
            )
        )
        ingredient = result.scalar_one_or_none()
        if ingredient is None:
            raise NotFoundError("Meal ingredient not found")
        return ingredient

    async def add_all_ingredients(self, ingredients):
        self.db.add_all(ingredients)
