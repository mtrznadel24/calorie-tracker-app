import datetime
from collections.abc import Sequence
from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.fridge.repositories import FridgeMealRepository, FridgeProductRepository
from app.meal.models import Meal, MealIngredient, MealIngredientDetails, MealType
from app.meal.repositories import MealIngredientRepository, MealRepository
from app.meal.schemas import (
    MealCreate,
    MealIngredientCreate,
    MealIngredientUpdate,
    WeightRequest, MealLogRead,
)
from app.utils.enums import NutrientType

# Meal


class MealService:
    def __init__(self, db: AsyncSession):
        self.repo = MealRepository(db)
        self.ingredient_repo = MealIngredientRepository(db)
        self.fridge_product_repo = FridgeProductRepository(db)
        self.fridge_meal_repo = FridgeMealRepository(db)

    async def create_meal(self, user_id: int, data: MealCreate) -> Meal:
        existing = await self.get_meal(user_id, data.date, data.type)
        if existing:
            return existing
        meal = Meal(**data.model_dump(exclude_unset=True), user_id=user_id)
        self.repo.add(meal)
        await self.repo.commit_or_conflict()
        return await self.repo.refresh_and_return(meal)

    async def get_meal(
        self, user_id: int, meal_date: date, meal_type: MealType
    ) -> Meal | None:
        return await self.repo.get_meal_by_date_and_type(user_id, meal_date, meal_type)

    async def get_or_create_meal(
        self, user_id: int, meal_date: date, meal_type: MealType
    ) -> Meal:
        meal = await self.get_meal(user_id, meal_date, meal_type)
        if not meal:
            meal = await self.create_meal(
                user_id, MealCreate(date=meal_date, type=meal_type)
            )
        return meal

    async def get_meal_by_id(self, user_id: int, meal_id: int) -> Meal:
        return await self.repo.get_by_id_for_user(user_id, meal_id)

    async def get_meal_logs(self, user_id: int, meal_date: datetime.date) -> Sequence[MealLogRead]:
        return await self.repo.get_meal_logs(user_id, meal_date)

    async def delete_meal(self, user_id: int, meal_id: int) -> Meal:
        return await self.repo.delete_by_id_for_user(user_id, meal_id)

    async def get_meal_nutrient_sum(
        self, user_id: int, meal_id: int, nutrient_type: NutrientType
    ) -> float:
        await self.repo.get_by_id_for_user(user_id, meal_id)
        return await self.repo.get_meal_nutrient_sum(user_id, meal_id, nutrient_type)

    async def get_meal_macro(self, user_id: int, meal_id: int) -> dict[str, float]:
        await self.repo.get_by_id_for_user(user_id, meal_id)
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
        self,
        user_id: int,
        meal_date: date,
        meal_type: MealType,
        data: MealIngredientCreate,
    ) -> MealIngredient:
        meal = await self.get_or_create_meal(user_id, meal_date, meal_type)
        ingredient = MealIngredient(weight=data.weight, meal_id=meal.id)
        ingredient.details = MealIngredientDetails(**data.details.model_dump())
        self.ingredient_repo.add(ingredient)

        try:
            await self.repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Ingredient already exists") from None

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
            ingredient.weight = data.weight

        if data.details:
            if not ingredient.details:
                raise NotFoundError("Ingredient details not found")
            for field, value in data.details.model_dump(exclude_unset=True).items():
                setattr(ingredient.details, field, value)
        try:
            await self.ingredient_repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Ingredient already exists") from None

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

    async def add_fridge_product_to_meal(
        self,
        user_id: int,
        fridge_id: int,
        fridge_product_id: int,
        meal_date: date,
        meal_type: MealType,
        weight: WeightRequest,
    ) -> MealIngredient:
        meal = await self.get_or_create_meal(user_id, meal_date, meal_type)
        product = await self.fridge_product_repo.get_fridge_product(
            fridge_id, fridge_product_id
        )
        meal_ingredient = MealIngredient(weight=weight.weight, meal_id=meal.id)
        meal_ingredient.details = MealIngredientDetails(
            product_name=product.product_name,
            calories_100g=product.calories_100g,
            proteins_100g=product.proteins_100g,
            fats_100g=product.fats_100g,
            carbs_100g=product.carbs_100g,
        )

        self.ingredient_repo.add(meal_ingredient)
        try:
            await self.repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Ingredient already exists") from None
        return await self.ingredient_repo.refresh_and_return(meal_ingredient)

    async def add_fridge_meal_to_meal(
        self,
        user_id: int,
        fridge_id: int,
        fridge_meal_id: int,
        meal_date: date,
        meal_type: MealType,
        weight: WeightRequest | None = None,
    ) -> Sequence[MealIngredient]:
        meal = await self.get_or_create_meal(user_id, meal_date, meal_type)
        meal_ingredients = await self.fridge_meal_repo.get_fridge_meal_ingredients(
            fridge_id, fridge_meal_id
        )
        if not meal_ingredients:
            raise NotFoundError("Fridge meal has no ingredients")
        meal_weight = await self.fridge_meal_repo.get_fridge_meal_weight(
            fridge_id, fridge_meal_id
        )

        k = weight.weight / meal_weight if weight else 1

        ingredients = []
        for ing in meal_ingredients:
            meal_ing = MealIngredient(
                meal_id=meal.id,
                weight=round(ing.weight * k),
            )
            meal_ing.details = MealIngredientDetails(
                product_name=ing.fridge_product.product_name,
                calories_100g=ing.fridge_product.calories_100g,
                proteins_100g=ing.fridge_product.proteins_100g,
                fats_100g=ing.fridge_product.fats_100g,
                carbs_100g=ing.fridge_product.carbs_100g,
            )
            ingredients.append(meal_ing)

        await self.ingredient_repo.add_all_ingredients(ingredients)
        try:
            await self.repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Ingredient already exists") from None

        for ing in ingredients:
            await self.repo.refresh(ing)

        return ingredients
