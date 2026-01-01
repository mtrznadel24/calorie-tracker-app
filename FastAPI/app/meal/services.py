import datetime
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.fridge.repositories import FridgeMealRepository, FridgeProductRepository
from app.meal.models import MealLog
from app.meal.repositories import MealRepository
from app.meal.schemas import (
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

    async def get_meal_log_by_id(self, user_id: int, meal_id: int) -> MealLog:
        return await self.repo.get_by_id_for_user(user_id, meal_id)

    async def get_meal_logs(
        self, user_id: int, meal_date: datetime.date
    ) -> Sequence[MealLogRead]:
        return await self.repo.get_meal_logs(user_id, meal_date)

    async def delete_meal_log(self, user_id: int, meal_id: int) -> MealLog:
        return await self.repo.delete_by_id_for_user(user_id, meal_id)

    # async def add_fridge_product_to_meal(
    #     self,
    #     user_id: int,
    #     fridge_id: int,
    #     fridge_product_id: int,
    #     meal_date: date,
    #     meal_type: MealType,
    #     weight: WeightRequest,
    # ) -> MealIngredient:
    #     meal = await self.get_or_create_meal(user_id, meal_date, meal_type)
    #     product = await self.fridge_product_repo.get_fridge_product(
    #         fridge_id, fridge_product_id
    #     )
    #     meal_ingredient = MealIngredient(weight=weight.weight, meal_id=meal.id)
    #     meal_ingredient.details = MealIngredientDetails(
    #         product_name=product.product_name,
    #         calories_100g=product.calories_100g,
    #         proteins_100g=product.proteins_100g,
    #         fats_100g=product.fats_100g,
    #         carbs_100g=product.carbs_100g,
    #     )
    #
    #     self.ingredient_repo.add(meal_ingredient)
    #     try:
    #         await self.repo.commit_or_conflict()
    #     except IntegrityError:
    #         raise ConflictError("Ingredient already exists") from None
    #     return await self.ingredient_repo.refresh_and_return(meal_ingredient)
    #
    # async def add_fridge_meal_to_meal(
    #     self,
    #     user_id: int,
    #     fridge_id: int,
    #     fridge_meal_id: int,
    #     meal_date: date,
    #     meal_type: MealType,
    #     weight: WeightRequest | None = None,
    # ) -> Sequence[MealIngredient]:
    #     meal = await self.get_or_create_meal(user_id, meal_date, meal_type)
    #     meal_ingredients = await self.fridge_meal_repo.get_fridge_meal_ingredients(
    #         fridge_id, fridge_meal_id
    #     )
    #     if not meal_ingredients:
    #         raise NotFoundError("Fridge meal has no ingredients")
    #     meal_weight = await self.fridge_meal_repo.get_fridge_meal_weight(
    #         fridge_id, fridge_meal_id
    #     )
    #
    #     k = weight.weight / meal_weight if weight else 1
    #
    #     ingredients = []
    #     for ing in meal_ingredients:
    #         meal_ing = MealIngredient(
    #             meal_id=meal.id,
    #             weight=round(ing.weight * k),
    #         )
    #         meal_ing.details = MealIngredientDetails(
    #             product_name=ing.fridge_product.product_name,
    #             calories_100g=ing.fridge_product.calories_100g,
    #             proteins_100g=ing.fridge_product.proteins_100g,
    #             fats_100g=ing.fridge_product.fats_100g,
    #             carbs_100g=ing.fridge_product.carbs_100g,
    #         )
    #         ingredients.append(meal_ing)
    #
    #     await self.ingredient_repo.add_all_ingredients(ingredients)
    #     try:
    #         await self.repo.commit_or_conflict()
    #     except IntegrityError:
    #         raise ConflictError("Ingredient already exists") from None
    #
    #     for ing in ingredients:
    #         await self.repo.refresh(ing)
    #
    #     return ingredients
