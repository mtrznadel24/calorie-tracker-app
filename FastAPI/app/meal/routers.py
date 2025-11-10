from datetime import date
from typing import Dict, List, Sequence

from fastapi import APIRouter

from app.core.db import DbSessionDep
from app.core.enums import NutrientType
from app.core.security import UserDep
from app.meal.models import Meal, MealIngredient, MealType
from app.meal.schemas import (
    MealCreate,
    MealIngredientCreate,
    MealIngredientRead,
    MealIngredientUpdate,
    MealRead,
)
from app.meal.services import (
    add_ingredient_to_meal,
    create_meal,
    delete_meal,
    delete_meal_ingredient,
    get_macro_for_day,
    get_meal,
    get_meal_by_id,
    get_meal_ingredient_by_id,
    get_meal_ingredients,
    get_meal_macro,
    get_meal_nutrient_sum,
    get_meals_nutrient_sum_for_day,
    update_meal_ingredient,
)

router = APIRouter(prefix="/meals", tags=["meals"])


@router.post("/", response_model=MealRead)
async def create_meal_route(
    db: DbSessionDep, user: UserDep, meal_in: MealCreate
) -> Meal:
    return await create_meal(db, user.id, data=meal_in)


@router.get("/current", response_model=MealRead)
async def read_meal_route(
    db: DbSessionDep, user: UserDep, meal_date: date, meal_type: MealType
) -> Meal:
    return await get_meal(db, user.id, meal_date=meal_date, meal_type=meal_type)


@router.get("/{meal_id}", response_model=MealRead)
async def read_meal_by_id_route(db: DbSessionDep, user: UserDep, meal_id: int) -> Meal:
    return await get_meal_by_id(db, user.id, meal_id=meal_id)


@router.delete("/{meal_id}", response_model=MealRead)
async def delete_meal_route(db: DbSessionDep, user: UserDep, meal_id: int) -> Meal:
    return await delete_meal(db, user.id, meal_id=meal_id)


@router.get("/{meal_id}/nutrients", response_model=float)
async def get_meal_nutrient_sum_route(
    db: DbSessionDep, user: UserDep, meal_id: int, nutrient_type: NutrientType
) -> float:
    return await get_meal_nutrient_sum(
        db, user.id, meal_id=meal_id, nutrient_type=nutrient_type
    )


@router.get("/{meal_id}/macro", response_model=Dict[str, float])
async def get_meal_macro_route(
    db: DbSessionDep, user: UserDep, meal_id: int
) -> Dict[str, float]:
    return await get_meal_macro(db, user.id, meal_id=meal_id)


@router.get("/nutrients", response_model=float)
async def get_meals_nutrient_sum_for_day_route(
    db: DbSessionDep,
    user: UserDep,
    meal_date: date,
    nutrient_type: NutrientType,
) -> float:
    return await get_meals_nutrient_sum_for_day(
        db, user.id, meal_date=meal_date, nutrient_type=nutrient_type
    )


@router.get("/macro", response_model=Dict[str, float])
async def get_macro_for_day_route(
    db: DbSessionDep, user: UserDep, meal_date: date
) -> Dict[str, float]:
    return await get_macro_for_day(db, user.id, meal_date=meal_date)


# Meal Ingredients


@router.post("/{meal_id}/ingredients", response_model=MealIngredientRead)
async def add_ingredient_to_meal_route(
    db: DbSessionDep, user: UserDep, meal_id: int, meal_in: MealIngredientCreate
) -> MealIngredient:

    return await add_ingredient_to_meal(db, user.id, meal_id=meal_id, data=meal_in)


@router.get("/{meal_id}/ingredients", response_model=List[MealIngredientRead])
async def read_meal_ingredients_route(
    db: DbSessionDep, user: UserDep, meal_id: int
) -> Sequence[MealIngredient]:
    return await get_meal_ingredients(db, user.id, meal_id=meal_id)


@router.get("/{meal_id}/ingredients/{ingredient_id}", response_model=MealIngredientRead)
async def read_meal_ingredient_route(
    db: DbSessionDep, user: UserDep, meal_id: int, ingredient_id: int
) -> MealIngredient:
    return await get_meal_ingredient_by_id(
        db, user.id, meal_id=meal_id, ingredient_id=ingredient_id
    )


@router.put("/{meal_id}/ingredients/{ingredient_id}", response_model=MealIngredientRead)
async def update_meal_ingredient_route(
    db: DbSessionDep,
    user: UserDep,
    meal_id: int,
    ingredient_id: int,
    meal_ingredient_in: MealIngredientUpdate,
) -> MealIngredient:
    return await update_meal_ingredient(
        db,
        user.id,
        meal_id=meal_id,
        ingredient_id=ingredient_id,
        data=meal_ingredient_in,
    )


@router.delete(
    "/{meal_id}/ingredients/{ingredient_id}", response_model=MealIngredientRead
)
async def delete_meal_ingredient_route(
    db: DbSessionDep, user: UserDep, meal_id: int, ingredient_id: int
) -> MealIngredient:
    return await delete_meal_ingredient(
        db, user.id, meal_id=meal_id, ingredient_id=ingredient_id
    )
