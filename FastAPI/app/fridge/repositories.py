from collections.abc import Sequence

from sqlalchemy import Row, func, literal, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.base_repository import BaseRepository
from app.core.exceptions import NotFoundError
from app.fridge.models import (
    FridgeMeal,
    FridgeMealIngredient,
    FridgeProduct,
)
from app.utils.enums import NutrientType


class FridgeProductRepository(BaseRepository[FridgeProduct]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, FridgeProduct)

    async def get_fridge_product_list(self, fridge_id: int) -> Sequence[FridgeProduct]:
        stmt = select(FridgeProduct).where(FridgeProduct.fridge_id == fridge_id)
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
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return product


class FridgeMealRepository(BaseRepository[FridgeMeal]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, FridgeMeal)

    def add_all_ingredients(self, ingredients):
        self.db.add_all(ingredients)

    async def get_fridge_meal_list(self, fridge_id: int):
        def calc_macro(column_name):
            return func.coalesce(
                func.sum(
                    (getattr(FridgeProduct, column_name) * FridgeMealIngredient.weight)
                    / 100
                ),
                0,
            )

        stmt = (
            select(
                FridgeMeal.id,
                FridgeMeal.name,
                FridgeMeal.is_favourite,
                calc_macro("calories_100g").label("calories"),
                calc_macro("proteins_100g").label("proteins"),
                calc_macro("fats_100g").label("fats"),
                calc_macro("carbs_100g").label("carbs"),
                func.count(FridgeMealIngredient.id).label("products_count"),
                func.coalesce(func.sum(FridgeMealIngredient.weight), 0).label("weight"),
            )
            .select_from(FridgeMeal)
            .outerjoin(
                FridgeMealIngredient,
                FridgeMeal.id == FridgeMealIngredient.fridge_meal_id,
            )
            .outerjoin(
                FridgeProduct,
                FridgeMealIngredient.fridge_product_id == FridgeProduct.id,
            )
            .where(FridgeMeal.fridge_id == fridge_id)
            .group_by(FridgeMeal.id)
        )

        result = await self.db.execute(stmt)
        return result.all()

    async def get_fridge_meal_entity(self, fridge_id: int, meal_id: int) -> FridgeMeal:
        stmt = (
            select(FridgeMeal)
            .options(
                selectinload(FridgeMeal.ingredients).selectinload(
                    FridgeMealIngredient.fridge_product
                )
            )
            .where(FridgeMeal.fridge_id == fridge_id, FridgeMeal.id == meal_id)
        )
        result = await self.db.execute(stmt)
        meal = result.scalar_one_or_none()

        if meal is None:
            raise NotFoundError("Meal not found")
        return meal

    async def get_fridge_meal(self, fridge_id: int, meal_id: int) -> Row:
        def calc_macro(column_name):
            return func.coalesce(
                func.sum(
                    (getattr(FridgeProduct, column_name) * FridgeMealIngredient.weight)
                    / 100
                ),
                0,
            )

        stmt = (
            select(
                FridgeMeal.id,
                FridgeMeal.name,
                FridgeMeal.is_favourite,
                calc_macro("calories_100g").label("calories"),
                calc_macro("proteins_100g").label("proteins"),
                calc_macro("fats_100g").label("fats"),
                calc_macro("carbs_100g").label("carbs"),
                func.count(FridgeMealIngredient.id).label("products_count"),
                func.coalesce(func.sum(FridgeMealIngredient.weight), 0).label("weight"),
            )
            .select_from(FridgeMeal)
            .outerjoin(
                FridgeMealIngredient,
                FridgeMeal.id == FridgeMealIngredient.fridge_meal_id,
            )
            .outerjoin(
                FridgeProduct,
                FridgeMealIngredient.fridge_product_id == FridgeProduct.id,
            )
            .where(FridgeMeal.fridge_id == fridge_id, FridgeMeal.id == meal_id)
            .group_by(FridgeMeal.id)
        )

        result = await self.db.execute(stmt)
        meal = result.first()
        if meal is None:
            raise NotFoundError("Meal not found")
        return meal

    async def delete_fridge_meal(self, fridge_id: int, object_id: int) -> FridgeMeal:
        meal = await self.get_fridge_meal_entity(fridge_id, object_id)
        await self.db.delete(meal)
        try:
            await self.db.commit()
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
        value = result.scalar() or 0.0
        if nutrient_type == NutrientType.CALORIES:
            return round(value, 0)
        else:
            return round(value, 1)

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
        return {
            field.value: round(
                getattr(row, field.value) or 0.0,
                0 if field == NutrientType.CALORIES else 1,
            )
            for field in fields
        }

    async def get_fridge_meal_weight(
        self, fridge_id: int, fridge_meal_id: int
    ) -> float:
        stmt = (
            select(func.sum(FridgeMealIngredient.weight))
            .join(FridgeMeal)
            .where(FridgeMeal.fridge_id == fridge_id, FridgeMeal.id == fridge_meal_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0.0

    async def add_meal_ingredient(self, ingredient: FridgeMealIngredient):
        self.db.add(ingredient)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise NotFoundError("Ingredient not found") from None
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        await self.db.refresh(ingredient)
        return ingredient

    async def get_fridge_meal_ingredients(
        self, fridge_id: int, meal_id: int
    ) -> Sequence[Row]:
        stmt = (
            select(
                FridgeMealIngredient.id,
                FridgeMealIngredient.weight,
                FridgeMealIngredient.fridge_product_id,
                FridgeProduct.product_name,
                (
                    FridgeProduct.calories_100g
                    * FridgeMealIngredient.weight
                    / literal(100)
                ).label("calories"),
            )
            .join(FridgeMeal, FridgeMealIngredient.fridge_meal_id == FridgeMeal.id)
            .join(
                FridgeProduct,
                FridgeMealIngredient.fridge_product_id == FridgeProduct.id,
            )
            .where(FridgeMeal.fridge_id == fridge_id, FridgeMeal.id == meal_id)
        )

        result = await self.db.execute(stmt)

        return result.all()

    async def get_fridge_meal_ingredient_entity(
        self, fridge_id: int, meal_id: int, ingredient_id: int
    ):
        stmt = (
            select(FridgeMealIngredient)
            .join(FridgeMeal, FridgeMealIngredient.fridge_meal_id == FridgeMeal.id)
            .where(
                FridgeMeal.fridge_id == fridge_id,
                FridgeMeal.id == meal_id,
                FridgeMealIngredient.id == ingredient_id,
            )
        )
        result = await self.db.execute(stmt)

        ingredient = result.scalar_one_or_none()

        if ingredient is None:
            raise NotFoundError("Ingredient not found")
        return ingredient

    async def get_fridge_meal_ingredient(
        self, fridge_id: int, meal_id: int, ingredient_id: int
    ):
        stmt = (
            select(
                FridgeMealIngredient.id,
                FridgeMealIngredient.weight,
                FridgeMealIngredient.fridge_product_id,
                FridgeProduct.product_name,
                (
                    FridgeProduct.calories_100g
                    * FridgeMealIngredient.weight
                    / literal(100)
                ).label("calories"),
            )
            .join(FridgeMeal, FridgeMealIngredient.fridge_meal_id == FridgeMeal.id)
            .join(
                FridgeProduct,
                FridgeMealIngredient.fridge_product_id == FridgeProduct.id,
            )
            .where(
                FridgeMeal.fridge_id == fridge_id,
                FridgeMeal.id == meal_id,
                FridgeMealIngredient.id == ingredient_id,
            )
        )
        result = await self.db.execute(stmt)

        ingredient = result.first()

        if ingredient is None:
            raise NotFoundError("Ingredient not found")
        return ingredient

    async def refresh_and_return_ingredient(self, ingredient) -> FridgeMealIngredient:
        await self.db.refresh(ingredient)
        return ingredient

    async def delete_ingredient(
        self, fridge_id: int, meal_id: int, ingredient_id: int
    ) -> FridgeMealIngredient:
        ingredient = await self.get_fridge_meal_ingredient_entity(
            fridge_id, meal_id, ingredient_id
        )
        await self.db.delete(ingredient)
        try:
            await self.db.commit()
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return ingredient
