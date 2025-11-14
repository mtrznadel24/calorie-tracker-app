from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import NutrientType
from app.core.exceptions import ConflictError
from app.fridge.models import (
    FoodCategory,
    FridgeMeal,
    FridgeMealIngredient,
    FridgeProduct,
)
from app.fridge.repositories import FridgeMealRepository, FridgeProductRepository
from app.fridge.schemas import (
    FridgeMealCreate,
    FridgeMealIngredientCreate,
    FridgeMealIngredientUpdate,
    FridgeMealUpdate,
    FridgeProductCreate,
    FridgeProductUpdate,
)


# Fridge products
class FridgeService:
    def __init__(self, db: AsyncSession):
        self.meal_repo = FridgeMealRepository(db)
        self.product_repo = FridgeProductRepository(db)

    async def create_fridge_product(
        self, fridge_id: int, data: FridgeProductCreate
    ) -> FridgeProduct:
        product = FridgeProduct(
            **data.model_dump(exclude_unset=True), fridge_id=fridge_id
        )
        self.product_repo.add(product)
        try:
            await self.product_repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Product already exists")
        return await self.product_repo.refresh_and_return(product)

    async def get_fridge_products(
        self,
        fridge_id: int,
        is_favourite: bool = False,
        category: FoodCategory = None,
        skip: int = 0,
        limit: int = 25,
    ) -> Sequence[FridgeProduct]:

        return await self.product_repo.get_fridge_product_list(
            fridge_id, is_favourite, category, skip, limit
        )

    async def get_fridge_product(
        self, fridge_id: int, product_id: int
    ) -> FridgeProduct:
        return await self.product_repo.get_fridge_product(fridge_id, product_id)

    async def update_fridge_product(
        self, fridge_id: int, product_id: int, data: FridgeProductUpdate
    ) -> FridgeProduct:
        product = await self.product_repo.get_fridge_product(fridge_id, product_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        try:
            await self.product_repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Product already exists")
        return await self.product_repo.refresh_and_return(product)

    async def delete_fridge_product(
        self, fridge_id: int, product_id: int
    ) -> FridgeProduct:
        try:
            return await self.product_repo.delete_fridge_product(fridge_id, product_id)
        except IntegrityError:
            raise ConflictError("Could not delete fridge product")

    # Fridge meals

    async def create_fridge_meal(
        self, fridge_id: int, data: FridgeMealCreate
    ) -> FridgeMeal:
        meal = FridgeMeal(**data.model_dump(exclude_unset=True), fridge_id=fridge_id)
        self.meal_repo.add(meal)
        try:
            await self.meal_repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Meal already exists")
        return await self.meal_repo.refresh_and_return(meal)

    async def get_fridge_meals(
        self,
        fridge_id: int,
        is_favourite: bool = False,
        skip: int = 0,
        limit: int = 25,
    ) -> Sequence[FridgeMeal]:
        return await self.meal_repo.get_fridge_meal_list(
            fridge_id, is_favourite, skip, limit
        )

    async def get_fridge_meal(self, fridge_id: int, meal_id: int) -> FridgeMeal:
        return await self.meal_repo.get_fridge_meal(fridge_id, meal_id)

    async def update_fridge_meal(
        self, fridge_id: int, meal_id: int, data: FridgeMealUpdate
    ) -> FridgeMeal:
        meal = await self.meal_repo.get_fridge_meal(fridge_id, meal_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(meal, field, value)
        try:
            await self.meal_repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Meal already exists")
        return await self.meal_repo.refresh_and_return(meal)

    async def delete_fridge_meal(self, fridge_id: int, meal_id: int) -> FridgeMeal:
        try:
            return await self.meal_repo.delete_fridge_meal(fridge_id, meal_id)
        except IntegrityError:
            raise ConflictError("Could not delete fridge meal")

    async def get_fridge_meal_nutrient_sum(
        self, fridge_id: int, meal_id: int, nutrient_type: NutrientType
    ) -> float:
        return await self.meal_repo.get_fridge_meal_nutrient_sum(
            fridge_id, meal_id, nutrient_type
        )

    async def get_fridge_meal_macro(
        self, fridge_id: int, meal_id: int
    ) -> dict[str, float]:
        return await self.meal_repo.get_fridge_meal_macro(fridge_id, meal_id)

    # Fridge meal ingredients

    async def add_fridge_meal_ingredient(
        self, fridge_id: int, meal_id: int, data: FridgeMealIngredientCreate
    ) -> FridgeMealIngredient:
        await self.meal_repo.get_fridge_meal(fridge_id, meal_id)
        ingredient = FridgeMealIngredient(**data.model_dump(), fridge_meal_id=meal_id)
        try:
            return await self.meal_repo.add_meal_ingredient(ingredient)
        except IntegrityError:
            raise ConflictError("Ingredient already exists")

    async def get_fridge_meal_ingredients(
        self, fridge_id: int, meal_id: int
    ) -> Sequence[FridgeMealIngredient]:
        return await self.meal_repo.get_fridge_meal_ingredients(fridge_id, meal_id)

    async def get_fridge_meal_ingredient(
        self, fridge_id: int, meal_id: int, ingredient_id: int
    ) -> FridgeMealIngredient:
        return await self.meal_repo.get_fridge_meal_ingredient(
            fridge_id, meal_id, ingredient_id
        )

    async def update_fridge_meal_ingredient(
        self,
        fridge_id: int,
        meal_id: int,
        ingredient_id: int,
        data: FridgeMealIngredientUpdate,
    ) -> FridgeMealIngredient:
        await self.meal_repo.get_fridge_meal(fridge_id, meal_id)
        ingredient = await self.meal_repo.get_fridge_meal_ingredient(
            fridge_id, meal_id, ingredient_id
        )
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(ingredient, field, value)

        try:
            await self.meal_repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Meal ingredient already exists")
        return await self.meal_repo.refresh_and_return_ingredient(ingredient)

    async def delete_fridge_meal_ingredient(
        self, fridge_id: int, meal_id: int, ingredient_id: int
    ) -> FridgeMealIngredient:
        await self.meal_repo.get_fridge_meal(fridge_id, meal_id)
        ingredient = await self.meal_repo.get_fridge_meal_ingredient(
            fridge_id, meal_id, ingredient_id
        )
        try:
            return await self.meal_repo.delete_ingredient(ingredient)
        except IntegrityError:
            raise ConflictError("Could not delete ingredient")
