from datetime import date
from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db, DbSessionDep
from app.core.enums import NutrientType
from app.core.security import UserDep
from app.models.meals import MealType
from app.schemas.meals import (
    MealCreate,
    MealIngredientCreate,
    MealIngredientRead,
    MealIngredientUpdate,
    MealRead,
)
from app.services.meals import (
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
def create_meal_route(
    db: DbSessionDep, user: UserDep, meal_in: MealCreate
):
    return create_meal(db, user.id, data=meal_in)


@router.get("/", response_model=List[MealRead])
def read_meal_route(
    db: DbSessionDep, user: UserDep, meal_date: date, meal_type: MealType
):
    return get_meal(db, user.id, meal_date=meal_date, meal_type=meal_type)


@router.get("/{meal_id}", response_model=MealRead)
def read_meal_by_id_route(db: DbSessionDep, user: UserDep, meal_id: int):
    return get_meal_by_id(db, user.id, meal_id=meal_id)


@router.delete("/{meal_id}", response_model=MealRead)
def delete_meal_route(db: DbSessionDep, user: UserDep, meal_id: int):
    return delete_meal(db, user.id, meal_id=meal_id)


@router.get("/{meal_id}/nutrients", response_model=float)
def get_meal_nutrient_sum_route(
    db: DbSessionDep,
    user: UserDep,
    meal_id: int,
    nutrient_type: NutrientType
):
    return get_meal_nutrient_sum(
        db, user.id, meal_id=meal_id, nutrient_type=nutrient_type
    )


@router.get("/{meal_id}/macro", response_model=Dict[str, float])
def get_meal_macro_route(db: DbSessionDep, user: UserDep, meal_id: int):
    return get_meal_macro(db, user.id, meal_id=meal_id)


@router.get("/nutrients", response_model=float)
def get_meals_nutrient_sum_for_day_route(
    db: DbSessionDep,
    user: UserDep,
    meal_date: date,
    nutrient_type: NutrientType,
):
    return get_meals_nutrient_sum_for_day(
        db, user.id, meal_date=meal_date, nutrient_type=nutrient_type
    )


@router.get("/macro", response_model=Dict[str, float])
def get_macro_for_day_route(
    db: DbSessionDep, user: UserDep, meal_date: date
):
    return get_macro_for_day(db, user.id, meal_date=meal_date)


# Meal Ingredients


@router.post("/{meal_id}/ingredients", response_model=MealIngredientRead)
def add_ingredient_to_meal_route(
    db: DbSessionDep,
    user: UserDep,
    meal_id: int,
    meal_in: MealIngredientCreate
):

    return add_ingredient_to_meal(db, user.id, meal_id=meal_id, data=meal_in)


@router.get("/{meal_id}/ingredients", response_model=List[MealIngredientRead])
def read_meal_ingredients_route(
    db: DbSessionDep, user: UserDep, meal_id: int
):
    return get_meal_ingredients(db, user.id, meal_id=meal_id)


@router.get("/{meal_id}/ingredients/{ingredient_id}", response_model=MealIngredientRead)
def read_meal_ingredient_route(
    db: DbSessionDep, user: UserDep, meal_id: int, ingredient_id: int
):
    return get_meal_ingredient_by_id(
        db, user.id, meal_id=meal_id, ingredient_id=ingredient_id
    )


@router.put("/{meal_id}/ingredients/{ingredient_id}", response_model=MealIngredientRead)
def update_fridge_meal_ingredient_route(
    db: DbSessionDep,
    user: UserDep,
    meal_id: int,
    ingredient_id: int,
    meal_ingredient_in: MealIngredientUpdate
):
    return update_meal_ingredient(
        db,
        user.id,
        meal_id=meal_id,
        ingredient_id=ingredient_id,
        data=meal_ingredient_in,
    )


@router.delete(
    "/{meal_id}/ingredients/{ingredient_id}", response_model=MealIngredientRead
)
def delete_meal_ingredient_route(
    db: DbSessionDep, user: UserDep, meal_id: int, ingredient_id: int
):
    return delete_meal_ingredient(
        db, user.id, meal_id=meal_id, ingredient_id=ingredient_id
    )
