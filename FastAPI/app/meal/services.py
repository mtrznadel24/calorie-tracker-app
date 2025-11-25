from datetime import date
from typing import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.meal.models import Meal, MealIngredient, MealIngredientDetails, MealType
from app.meal.repositories import MealIngredientRepository, MealRepository
from app.meal.schemas import MealCreate, MealIngredientCreate, MealIngredientUpdate
from app.utils.enums import NutrientType

# Meal


class MealService:
    def __init__(self, db: AsyncSession):
        self.repo = MealRepository(db)
        self.ingredient_repo = MealIngredientRepository(db)

    async def create_meal(self, user_id: int, data: MealCreate) -> Meal:
        meal = Meal(**data.model_dump(exclude_unset=True), user_id=user_id)
        self.repo.add(meal)
        try:
            await self.repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Meal already exists")
        return meal

    async def get_meal(
        self, user_id: int, meal_date: date, meal_type: MealType
    ) -> Meal:
        return await self.repo.get_meal_by_date_and_type(user_id, meal_date, meal_type)

    async def get_meal_by_id(self, user_id: int, meal_id: int) -> Meal:
        return await self.repo.get_by_id_for_user(user_id, meal_id)

    async def delete_meal(self, user_id: int, meal_id: int) -> Meal:
        return await self.repo.delete_by_id_for_user(user_id, meal_id)

    async def get_meal_nutrient_sum(
        self, user_id: int, meal_id: int, nutrient_type: NutrientType
    ) -> float:
        return await self.repo.get_meal_nutrient_sum(user_id, meal_id, nutrient_type)

    async def get_meal_macro(self, user_id: int, meal_id: int) -> dict[str, float]:
        return await self.repo.get_meal_macro(user_id, meal_id)

    async def get_meals_nutrient_sum_for_day(
        self, user_id: int, meal_date: date, nutrient_type: NutrientType
    ) -> float:
        return await self.repo.get_meals_nutrient_sum_for_day(
            user_id, meal_date, nutrient_type
        )

    async def get_macro_for_day(
        self, user_id: int, meal_date: date
    ) -> dict[str, float]:
        return await self.repo.get_macro_for_day(user_id, meal_date)

    # Meal ingredient

    async def add_ingredient_to_meal(
        self, user_id: int, meal_id: int, data: MealIngredientCreate
    ) -> MealIngredient:
        await self.repo.get_by_id_for_user(user_id, meal_id)
        ingredient = MealIngredient(weight=data.weight, meal_id=meal_id)
        ingredient.details = MealIngredientDetails(**data.details.model_dump())
        self.ingredient_repo.add(ingredient)

        try:
            await self.repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Ingredient already exists")

        return await self.ingredient_repo.refresh_and_return(ingredient)

    async def get_meal_ingredients(
        self, user_id: int, meal_id: int
    ) -> Sequence[MealIngredient]:
        await self.repo.get_by_id_for_user(user_id, meal_id)
        return await self.ingredient_repo.get_meal_ingredients(meal_id)

    async def get_meal_ingredient_by_id(
        self, user_id: int, meal_id, ingredient_id: int
    ) -> MealIngredient:
        await self.repo.get_by_id_for_user(user_id, meal_id)
        return await self.ingredient_repo.get_meal_ingredient_by_id(
            meal_id, ingredient_id
        )

    async def update_meal_ingredient(
        self,
        user_id: int,
        meal_id,
        ingredient_id: int,
        data: MealIngredientUpdate,
    ) -> MealIngredient:
        await self.repo.get_by_id_for_user(user_id, meal_id)
        ingredient = await self.ingredient_repo.get_by_id(ingredient_id)

        if data.weight:
            setattr(ingredient, "weight", data.weight)

        if data.details:
            if not ingredient.details:
                raise NotFoundError("Ingredient details not found")
            for field, value in data.details.model_dump(exclude_unset=True).items():
                setattr(ingredient.details, field, value)
        try:
            await self.ingredient_repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Ingredient already exists")

        return await self.ingredient_repo.refresh_and_return(ingredient)

    async def delete_meal_ingredient(
        self, user_id: int, meal_id, ingredient_id: int
    ) -> MealIngredient:
        await self.repo.get_by_id_for_user(user_id, meal_id)
        return await self.ingredient_repo.delete_by_id(ingredient_id)

    async def get_ingredient_details(
        self, user_id: int, meal_id, ingredient_id: int
    ) -> MealIngredientDetails:
        await self.repo.get_by_id_for_user(user_id, meal_id)
        ingredient = await self.ingredient_repo.get_by_id(ingredient_id)
        return ingredient.details
