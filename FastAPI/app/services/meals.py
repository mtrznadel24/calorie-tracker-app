from collections.abc import Sequence
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import NutrientType
from app.core.exceptions import ConflictError, NotFoundError
from app.models.meals import Meal, MealIngredient, MealIngredientDetails, MealType
from app.models.user import User
from app.schemas.meals import MealCreate, MealIngredientCreate, MealIngredientUpdate
from app.utils.crud import create_instance, delete_by_id, get_or_404, update_by_id

fields = [
    NutrientType.CALORIES,
    NutrientType.PROTEINS,
    NutrientType.FATS,
    NutrientType.CARBS,
]

# Meal Utils


async def get_user_meal_or_404(db: AsyncSession, user_id: int, meal_id: int) -> Meal:
    result = await db.execute(
        select(Meal).where(Meal.id == meal_id, Meal.user_id == user_id)
    )
    meal = result.scalars().first()
    if not meal:
        raise NotFoundError("Meal not found")
    return meal


# Meal


async def create_meal(db: AsyncSession, user_id: int, data: MealCreate) -> Meal:
    await get_or_404(db, User, user_id)
    return await create_instance(db, Meal, data.model_dump())


async def get_meal(
    db: AsyncSession, user_id: int, meal_date: date, meal_type: MealType
) -> Meal:
    result = await db.execute(
        select(Meal)
        .where(Meal.user_id == user_id)
        .where(Meal.date == meal_date)
        .where(Meal.type == meal_type)
    )
    return result.scalar_one_or_none()


async def get_meal_by_id(db: AsyncSession, user_id: int, meal_id: int) -> Meal:
    return await get_user_meal_or_404(db, user_id, meal_id)


async def delete_meal(db: AsyncSession, user_id: int, meal_id: int) -> Meal:
    await get_or_404(db, User, user_id)
    return await delete_by_id(db, Meal, meal_id)


async def get_meal_nutrient_sum(
    db: AsyncSession, user_id: int, meal_id: int, nutrient_type: NutrientType
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
    result = await db.execute(stmt)
    return result.scalar() or 0.0


async def get_meal_macro(
    db: AsyncSession, user_id: int, meal_id: int
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
                for field in fields
            ]
        )
        .select_from(MealIngredient)
        .join(MealIngredientDetails)
        .join(Meal)
        .where(Meal.user_id == user_id, Meal.id == meal_id)
    )
    result = await db.execute(stmt)
    row = result.one_or_none()
    return {field.value: getattr(row, field.value) or 0.0 for field in fields}


async def get_meals_nutrient_sum_for_day(
    db: AsyncSession, user_id: int, meal_date: date, nutrient_type: NutrientType
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
    result = await db.execute(stmt)
    return result.scalar() or 0.0


async def get_macro_for_day(
    db: AsyncSession, user_id: int, meal_date: date
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
                for field in fields
            ]
        )
        .select_from(MealIngredient)
        .join(MealIngredientDetails)
        .join(Meal)
        .where(Meal.user_id == user_id, Meal.date == meal_date)
    )
    result = await db.execute(stmt)
    row = result.one_or_none()
    return {field.value: getattr(row, field.value) or 0.0 for field in fields}


# Meal ingredient


async def add_ingredient_to_meal(
    db: AsyncSession, user_id: int, meal_id: int, data: MealIngredientCreate
) -> MealIngredient:
    await get_user_meal_or_404(db, user_id, meal_id)
    ingredient = MealIngredient(weight=data.weight, meal_id=meal_id)
    db.add(ingredient)
    await db.flush()

    details = MealIngredientDetails(id=ingredient.id, **data.details.model_dump())
    db.add(details)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictError("Invalid ingredient data (constraint violation)")
    except SQLAlchemyError:
        await db.rollback()
        raise

    await db.refresh(ingredient)
    return ingredient


async def get_meal_ingredients(
    db: AsyncSession, user_id: int, meal_id: int
) -> Sequence[MealIngredient]:
    await get_user_meal_or_404(db, user_id, meal_id)
    result = await db.execute(
        select(MealIngredient).where(MealIngredient.meal_id == meal_id)
    )
    return result.scalars().all()


async def get_meal_ingredient_by_id(
    db: AsyncSession, user_id: int, meal_id, ingredient_id: int
) -> MealIngredient:
    await get_user_meal_or_404(db, user_id, meal_id)
    result = await db.execute(
        select(MealIngredient).where(
            MealIngredient.id == ingredient_id, MealIngredient.meal_id == meal_id
        )
    )
    return result.scalar_one_or_none()


async def update_meal_ingredient(
    db: AsyncSession,
    user_id: int,
    meal_id,
    ingredient_id: int,
    data: MealIngredientUpdate,
) -> MealIngredient:
    await get_user_meal_or_404(db, user_id, meal_id)
    ingredient = await get_or_404(db, MealIngredient, ingredient_id)

    if data.weight:
        await update_by_id(db, MealIngredient, ingredient_id, {"weight": data.weight})

    if data.details:
        if not ingredient.details:
            raise NotFoundError("Ingredient details not found")
        await update_by_id(
            db, MealIngredientDetails, ingredient.details.id, data.details.model_dump()
        )

    return ingredient


async def delete_meal_ingredient(
    db: AsyncSession, user_id: int, meal_id, ingredient_id: int
) -> MealIngredient:
    await get_user_meal_or_404(db, user_id, meal_id)
    return await delete_by_id(db, MealIngredient, ingredient_id)


async def get_ingredient_details(
    db: AsyncSession, user_id: int, meal_id, ingredient_id: int
) -> MealIngredientDetails:
    await get_user_meal_or_404(db, user_id, meal_id)
    ingredient = await get_or_404(db, MealIngredient, ingredient_id)
    return ingredient.details
