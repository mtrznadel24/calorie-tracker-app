from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.core.exceptions import NotFoundError
from app.fridge.models import (
    FoodCategory,
    FridgeMeal,
    FridgeMealIngredient,
    FridgeProduct,
)
from app.utils.enums import NutrientType


class FridgeProductRepository(BaseRepository[FridgeProduct]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, FridgeProduct)

    async def get_fridge_product_list(
        self,
        fridge_id: int,
        is_favourite: bool,
        category: FoodCategory,
        skip: int,
        limit: int,
    ) -> Sequence[FridgeProduct]:
        stmt = select(FridgeProduct).where(FridgeProduct.fridge_id == fridge_id)
        if is_favourite:
            stmt = stmt.where(FridgeProduct.is_favourite.is_(True))
        if category is not None:
            stmt = stmt.where(FridgeProduct.category == category)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_fridge_product(
        self, fridge_id: int, product_id: int
    ) -> FridgeProduct:
        result = await self.db.execute(
            select(FridgeProduct).where(
                FridgeProduct.id == product_id, FridgeProduct.fridge_id == fridge_id
            )
        )
        product = result.scalar_one_or_none()
        if product is None:
            raise NotFoundError("Fridge product not found")
        return product

    async def delete_fridge_product(
        self, fridge_id: int, object_id: int
    ) -> FridgeProduct:
        product = await self.get_fridge_product(fridge_id, object_id)
        await self.db.delete(product)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return product


class FridgeMealRepository(BaseRepository[FridgeMeal]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, FridgeMeal)

    async def get_fridge_meal_list(
        self,
        fridge_id: int,
        is_favourite: bool,
        skip: int,
        limit: int,
    ) -> Sequence[FridgeMeal]:
        stmt = select(FridgeMeal).where(FridgeMeal.fridge_id == fridge_id)
        if is_favourite:
            stmt = stmt.where(FridgeMeal.is_favourite.is_(True))
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_fridge_meal(self, fridge_id: int, meal_id: int) -> FridgeMeal:
        result = await self.db.execute(
            select(FridgeMeal).where(
                FridgeMeal.id == meal_id, FridgeMeal.fridge_id == fridge_id
            )
        )
        meal = result.scalar_one_or_none()
        if meal is None:
            raise NotFoundError("Meal not found")
        return meal

    async def delete_fridge_meal(self, fridge_id: int, object_id: int) -> FridgeMeal:
        meal = await self.get_fridge_meal(fridge_id, object_id)
        await self.db.delete(meal)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return meal

    async def get_fridge_meal_nutrient_sum(
        self, fridge_id: int, meal_id: int, nutrient_type: NutrientType
    ) -> float:
        stmt = (
            select(
                func.sum(
                    (
                        getattr(FridgeProduct, nutrient_type.value + "_100g")
                        * FridgeMealIngredient.weight
                    )
                    / 100
                )
            )
            .select_from(FridgeMealIngredient)
            .join(FridgeProduct)
            .join(FridgeMeal)
            .where(FridgeMeal.fridge_id == fridge_id, FridgeMeal.id == meal_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0.0

    async def get_fridge_meal_macro(
        self, fridge_id: int, meal_id: int
    ) -> dict[str, float]:
        fields = [
            NutrientType.CALORIES,
            NutrientType.PROTEINS,
            NutrientType.FATS,
            NutrientType.CARBS,
        ]
        stmt = (
            select(
                *[
                    func.sum(
                        (
                            getattr(FridgeProduct, field.value + "_100g")
                            * FridgeMealIngredient.weight
                        )
                        / 100
                    ).label(field.value)
                    for field in fields
                ]
            )
            .select_from(FridgeMealIngredient)
            .join(FridgeProduct)
            .join(FridgeMeal)
            .where(FridgeMeal.fridge_id == fridge_id, FridgeMeal.id == meal_id)
        )
        result = await self.db.execute(stmt)
        row = result.one_or_none()
        return {field.value: getattr(row, field.value) or 0.0 for field in fields}

    async def add_meal_ingredient(self, ingredient: FridgeMealIngredient):
        self.db.add(ingredient)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise NotFoundError("Ingredient not found")
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        await self.db.refresh(ingredient)
        return ingredient

    async def get_fridge_meal_ingredients(
        self, fridge_id: int, meal_id: int
    ) -> Sequence[FridgeMealIngredient]:
        result = await self.db.execute(
            select(FridgeMealIngredient)
            .join(FridgeMeal, FridgeMealIngredient.fridge_meal_id == FridgeMeal.id)
            .where(FridgeMeal.fridge_id == fridge_id, FridgeMeal.id == meal_id)
        )
        return result.scalars().all()

    async def get_fridge_meal_ingredient(
        self, fridge_id: int, meal_id: int, ingredient_id: int
    ) -> FridgeMealIngredient:
        result = await self.db.execute(
            select(FridgeMealIngredient)
            .join(FridgeMeal, FridgeMealIngredient.fridge_meal_id == FridgeMeal.id)
            .where(
                FridgeMeal.fridge_id == fridge_id,
                FridgeMeal.id == meal_id,
                FridgeMealIngredient.id == ingredient_id,
            )
        )

        ingredient = result.scalar_one_or_none()

        if ingredient is None:
            raise NotFoundError("Ingredient not found")
        return ingredient

    async def refresh_and_return_ingredient(self, ingredient) -> FridgeMealIngredient:
        await self.db.refresh(ingredient)
        return ingredient

    async def delete_ingredient(
        self, fridge_id: int, meal_id: int, ingredient_id: int
    ) -> FridgeMealIngredient:
        ingredient = await self.get_fridge_meal_ingredient(
            fridge_id, meal_id, ingredient_id
        )
        await self.db.delete(ingredient)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return ingredient
