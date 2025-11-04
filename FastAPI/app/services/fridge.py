from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import NutrientType
from app.models.fridge import (
    FoodCategory,
    FridgeMeal,
    FridgeMealIngredient,
    FridgeProduct,
)
from app.schemas.fridge import (
    FridgeMealCreate,
    FridgeMealIngredientCreate,
    FridgeMealIngredientUpdate,
    FridgeMealUpdate,
    FridgeProductCreate,
    FridgeProductUpdate,
)
from app.utils.crud import create_instance, delete_by_id, update_by_id
from app.utils.crud_fridge import (
    create_fridge_instance,
    delete_fridge_object,
    get_fridge_object_or_404,
    update_fridge_object,
)

# Fridge products


async def create_fridge_product(
    db: AsyncSession, fridge_id: int, data: FridgeProductCreate
) -> FridgeProduct:
    return await create_fridge_instance(
        db, FridgeProduct, fridge_id, {**data.model_dump(), "fridge_id": fridge_id}
    )


async def get_fridge_products(
    db: AsyncSession,
    fridge_id: int,
    is_favourite: bool = False,
    category: FoodCategory = None,
    skip: int = 0,
    limit: int = 25,
) -> Sequence[FridgeProduct]:

    stmt = select(FridgeProduct).where(FridgeProduct.fridge_id == fridge_id)
    if is_favourite:
        stmt = stmt.where(FridgeProduct.is_favourite.is_(True))
    if category is not None:
        stmt = stmt.where(FridgeProduct.category == category)
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_fridge_product(
    db: AsyncSession, fridge_id: int, product_id: int
) -> FridgeProduct:
    return await get_fridge_object_or_404(db, FridgeProduct, fridge_id, product_id)


async def update_fridge_product(
    db: AsyncSession, fridge_id: int, product_id: int, data: FridgeProductUpdate
) -> FridgeProduct:
    return await update_fridge_object(
        db, FridgeProduct, fridge_id, product_id, data.model_dump(exclude_unset=True)
    )


async def delete_fridge_product(
    db: AsyncSession, fridge_id: int, product_id: int
) -> FridgeProduct:
    return await delete_fridge_object(db, FridgeProduct, fridge_id, product_id)


# Fridge meals


async def create_fridge_meal(
    db: AsyncSession, fridge_id: int, data: FridgeMealCreate
) -> FridgeMeal:
    return await create_fridge_instance(
        db, FridgeMeal, fridge_id, {**data.model_dump(), "fridge_id": fridge_id}
    )


async def get_fridge_meals(
    db: AsyncSession,
    fridge_id: int,
    is_favourite: bool = False,
    skip: int = 0,
    limit: int = 25,
) -> Sequence[FridgeMeal]:
    stmt = select(FridgeMeal).where(FridgeMeal.fridge_id == fridge_id)
    if is_favourite:
        stmt = stmt.where(FridgeMeal.is_favourite.is_(True))
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_fridge_meal(db: AsyncSession, fridge_id: int, meal_id: int) -> FridgeMeal:
    return await get_fridge_object_or_404(db, FridgeMeal, fridge_id, meal_id)


async def update_fridge_meal(
    db: AsyncSession, fridge_id: int, meal_id: int, data: FridgeMealUpdate
) -> FridgeMeal:
    return await update_fridge_object(
        db, FridgeMeal, fridge_id, meal_id, data.model_dump(exclude_unset=True)
    )


async def delete_fridge_meal(
    db: AsyncSession, fridge_id: int, meal_id: int
) -> FridgeMeal:
    return await delete_fridge_object(db, FridgeMeal, fridge_id, meal_id)


async def get_fridge_meal_nutrient_sum(
    db: AsyncSession, fridge_id: int, meal_id: int, nutrient_type: NutrientType
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
    result = await db.execute(stmt)
    return result.scalar() or 0.0


async def get_fridge_meal_macro(
    db: AsyncSession, fridge_id: int, meal_id: int
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
                ).alias(field.value)
                for field in fields
            ]
        )
        .select_from(FridgeMealIngredient)
        .join(FridgeProduct)
        .join(FridgeMeal)
        .where(FridgeMeal.fridge_id == fridge_id, FridgeMeal.id == meal_id)
    )
    result = await db.execute(stmt)
    row = result.one_or_none()
    return {field.value: getattr(row, field.value) or 0.0 for field in fields}


# Fridge meal ingredients


async def add_fridge_meal_ingredient(
    db: AsyncSession, fridge_id: int, meal_id: int, data: FridgeMealIngredientCreate
) -> FridgeMealIngredient:
    await get_fridge_object_or_404(db, FridgeMeal, fridge_id, meal_id)
    return await create_instance(
        db, FridgeMealIngredient, {**data.model_dump(), "fridge_meal_id": meal_id}
    )


async def get_fridge_meal_ingredients(
    db: AsyncSession, fridge_id: int, meal_id: int
) -> Sequence[FridgeMealIngredient]:
    result = await db.execute(
        select(FridgeMealIngredient)
        .join(FridgeMeal, FridgeMealIngredient.fridge_meal_id == FridgeMeal.id)
        .where(FridgeMeal.fridge_id == fridge_id, FridgeMeal.id == meal_id)
    )
    return result.scalars().all()


async def get_fridge_meal_ingredient(
    db: AsyncSession, fridge_id: int, meal_id: int, ingredient_id: int
) -> FridgeMealIngredient:
    result = await db.execute(
        select(FridgeMealIngredient)
        .join(FridgeMeal, FridgeMealIngredient.fridge_meal_id == FridgeMeal.id)
        .where(
            FridgeMeal.fridge_id == fridge_id,
            FridgeMeal.id == meal_id,
            FridgeMealIngredient.id == ingredient_id,
        )
    )

    return result.scalar_one_or_none()


async def update_fridge_meal_ingredient(
    db: AsyncSession,
    fridge_id: int,
    meal_id: int,
    ingredient_id: int,
    data: FridgeMealIngredientUpdate,
) -> FridgeMealIngredient:
    await get_fridge_object_or_404(db, FridgeMeal, fridge_id, meal_id)
    return await update_by_id(
        db, FridgeMealIngredient, ingredient_id, data.model_dump(exclude_unset=True)
    )


async def delete_fridge_meal_ingredient(
    db: AsyncSession, fridge_id: int, meal_id: int, ingredient_id: int
) -> FridgeMealIngredient:
    await get_fridge_object_or_404(db, FridgeMeal, fridge_id, meal_id)
    return await delete_by_id(db, FridgeMealIngredient, ingredient_id)
