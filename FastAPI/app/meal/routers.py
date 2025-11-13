from datetime import date
from typing import Dict, List, Sequence

from fastapi import APIRouter

from app.core.enums import NutrientType
from app.core.security import UserDep
from app.meal.dependencies import MealServiceDep
from app.meal.models import Meal, MealIngredient, MealType
from app.meal.schemas import (
    MealCreate,
    MealIngredientCreate,
    MealIngredientRead,
    MealIngredientUpdate,
    MealRead,
)

router = APIRouter(prefix="/meals", tags=["meals"])


@router.post("/", response_model=MealRead)
async def create_meal_route(
    meal_service: MealServiceDep, user: UserDep, meal_in: MealCreate
) -> Meal:
    return await meal_service.create_meal(user.id, data=meal_in)


@router.get("/lookup", response_model=MealRead)
async def read_meal_route(
    meal_service: MealServiceDep, user: UserDep, meal_date: date, meal_type: MealType
) -> Meal:
    return await meal_service.get_meal(user.id, meal_date=meal_date, meal_type=meal_type)


@router.get("/{meal_id}", response_model=MealRead)
async def read_meal_by_id_route(meal_service: MealServiceDep, user: UserDep, meal_id: int) -> Meal:
    return await meal_service.get_meal_by_id(user.id, meal_id=meal_id)


@router.delete("/{meal_id}", response_model=MealRead)
async def delete_meal_route(meal_service: MealServiceDep, user: UserDep, meal_id: int) -> Meal:
    return await meal_service.delete_meal(user.id, meal_id=meal_id)


@router.get("/{meal_id}/nutrients", response_model=float)
async def get_meal_nutrient_sum_route(
    meal_service: MealServiceDep, user: UserDep, meal_id: int, nutrient_type: NutrientType
) -> float:
    return await meal_service.get_meal_nutrient_sum(
        user.id, meal_id=meal_id, nutrient_type=nutrient_type
    )


@router.get("/{meal_id}/macro", response_model=Dict[str, float])
async def get_meal_macro_route(
    meal_service: MealServiceDep, user: UserDep, meal_id: int
) -> Dict[str, float]:
    return await meal_service.get_meal_macro(user.id, meal_id=meal_id)


@router.get("/daily/nutrients", response_model=float)
async def get_meals_nutrient_sum_for_day_route(
    meal_service: MealServiceDep,
    user: UserDep,
    meal_date: date,
    nutrient_type: NutrientType,
) -> float:
    return await meal_service.get_meals_nutrient_sum_for_day(
        user.id, meal_date=meal_date, nutrient_type=nutrient_type
    )


@router.get("/daily/macro", response_model=Dict[str, float])
async def get_macro_for_day_route(
    meal_service: MealServiceDep, user: UserDep, meal_date: date
) -> Dict[str, float]:
    return await meal_service.get_macro_for_day(user.id, meal_date=meal_date)


# Meal Ingredients


@router.post("/{meal_id}/ingredients", response_model=MealIngredientRead)
async def add_ingredient_to_meal_route(
    meal_service: MealServiceDep, user: UserDep, meal_id: int, meal_in: MealIngredientCreate
) -> MealIngredient:

    return await meal_service.add_ingredient_to_meal(user.id, meal_id=meal_id, data=meal_in)


@router.get("/{meal_id}/ingredients", response_model=List[MealIngredientRead])
async def read_meal_ingredients_route(
    meal_service: MealServiceDep, user: UserDep, meal_id: int
) -> Sequence[MealIngredient]:
    return await meal_service.get_meal_ingredients(user.id, meal_id=meal_id)


@router.get("/{meal_id}/ingredients/{ingredient_id}", response_model=MealIngredientRead)
async def read_meal_ingredient_route(
    meal_service: MealServiceDep, user: UserDep, meal_id: int, ingredient_id: int
) -> MealIngredient:
    return await meal_service.get_meal_ingredient_by_id(
        user.id, meal_id=meal_id, ingredient_id=ingredient_id
    )


@router.put("/{meal_id}/ingredients/{ingredient_id}", response_model=MealIngredientRead)
async def update_meal_ingredient_route(
    meal_service: MealServiceDep,
    user: UserDep,
    meal_id: int,
    ingredient_id: int,
    meal_ingredient_in: MealIngredientUpdate,
) -> MealIngredient:
    return await meal_service.update_meal_ingredient(
        user.id,
        meal_id=meal_id,
        ingredient_id=ingredient_id,
        data=meal_ingredient_in,
    )


@router.delete(
    "/{meal_id}/ingredients/{ingredient_id}", response_model=MealIngredientRead
)
async def delete_meal_ingredient_route(
    meal_service: MealServiceDep, user: UserDep, meal_id: int, ingredient_id: int
) -> MealIngredient:
    return await meal_service.delete_meal_ingredient(
        user.id, meal_id=meal_id, ingredient_id=ingredient_id
    )
