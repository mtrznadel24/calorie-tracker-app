from collections.abc import Sequence
from datetime import date

from fastapi import APIRouter

from app.auth.dependencies import UserDep
from app.fridge.dependencies import FridgeDep
from app.meal.dependencies import MealServiceDep
from app.meal.models import Meal, MealIngredient, MealType
from app.meal.schemas import (
    MealCreate,
    MealIngredientCreate,
    MealIngredientRead,
    MealIngredientUpdate,
    MealRead,
    WeightRequest, MealLogRead,
)
from app.utils.enums import NutrientType

router = APIRouter(prefix="/meals", tags=["meals"])


@router.post("", response_model=MealRead)
async def add_meal(
    meal_service: MealServiceDep, user: UserDep, meal_in: MealCreate
) -> Meal:
    return await meal_service.create_meal(user.id, data=meal_in)


@router.get("/lookup", response_model=MealRead | None)
async def read_meal(
    meal_service: MealServiceDep, user: UserDep, meal_date: date, meal_type: MealType
) -> Meal:
    return await meal_service.get_meal(
        user.id, meal_date=meal_date, meal_type=meal_type
    )


@router.get("/{meal_id}", response_model=MealRead)
async def read_meal_by_id(
    meal_service: MealServiceDep, user: UserDep, meal_id: int
) -> Meal:
    return await meal_service.get_meal_by_id(user.id, meal_id=meal_id)

@router.get("/{meal_date}/meal-logs", response_model=Sequence[MealLogRead])
async def read_meal_logs(
        meal_service: MealServiceDep, user: UserDep, meal_date: date
):
    return await meal_service.get_meal_logs(user.id, meal_date=meal_date)

@router.delete("/{meal_id}", response_model=MealRead)
async def delete_meal(
    meal_service: MealServiceDep, user: UserDep, meal_id: int
) -> Meal:
    return await meal_service.delete_meal(user.id, meal_id=meal_id)


@router.get("/daily/nutrients", response_model=float)
async def get_meals_nutrient_sum_for_day(
    meal_service: MealServiceDep,
    user: UserDep,
    meal_date: date,
    nutrient_type: NutrientType,
) -> float:
    return await meal_service.get_meals_nutrient_sum_for_day(
        user.id, meal_date=meal_date, nutrient_type=nutrient_type
    )


@router.get("/daily/macro", response_model=dict[str, float])
async def get_macro_for_day(
    meal_service: MealServiceDep, user: UserDep, meal_date: date
) -> dict[str, float]:
    return await meal_service.get_macro_for_day(user.id, meal_date=meal_date)


@router.get("/{meal_id}/nutrients", response_model=float)
async def get_meal_nutrient_sum(
    meal_service: MealServiceDep,
    user: UserDep,
    meal_id: int,
    nutrient_type: NutrientType,
) -> float:
    return await meal_service.get_meal_nutrient_sum(
        user.id, meal_id=meal_id, nutrient_type=nutrient_type
    )


@router.get("/{meal_id}/macro", response_model=dict[str, float])
async def get_meal_macro(
    meal_service: MealServiceDep, user: UserDep, meal_id: int
) -> dict[str, float]:
    return await meal_service.get_meal_macro(user.id, meal_id=meal_id)


# Meal Ingredients


@router.post("/{meal_date}/{meal_type}/ingredients", response_model=MealIngredientRead)
async def add_ingredient_to_meal(
    meal_service: MealServiceDep,
    user: UserDep,
    meal_date: date,
    meal_type: MealType,
    meal_in: MealIngredientCreate,
) -> MealIngredient:
    return await meal_service.add_ingredient_to_meal(
        user.id, meal_date, meal_type, data=meal_in
    )


@router.get("/{meal_id}/ingredients", response_model=list[MealIngredientRead])
async def read_meal_ingredients(
    meal_service: MealServiceDep, user: UserDep, meal_id: int
) -> Sequence[MealIngredient]:
    return await meal_service.get_meal_ingredients(user.id, meal_id=meal_id)


@router.get("/{meal_id}/ingredients/{ingredient_id}", response_model=MealIngredientRead)
async def read_meal_ingredient(
    meal_service: MealServiceDep, user: UserDep, meal_id: int, ingredient_id: int
) -> MealIngredient:
    return await meal_service.get_meal_ingredient_by_id(
        user.id, meal_id=meal_id, ingredient_id=ingredient_id
    )


@router.put("/{meal_id}/ingredients/{ingredient_id}", response_model=MealIngredientRead)
async def update_meal_ingredient(
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
async def delete_meal_ingredient(
    meal_service: MealServiceDep, user: UserDep, meal_id: int, ingredient_id: int
) -> MealIngredient:
    return await meal_service.delete_meal_ingredient(
        user.id, meal_id=meal_id, ingredient_id=ingredient_id
    )


@router.post(
    "/{meal_date}/{meal_type}/ingredients/from-fridge-product/{fridge_product_id}",
    response_model=MealIngredientRead,
)
async def add_fridge_product_to_meal(
    meal_service: MealServiceDep,
    user: UserDep,
    fridge: FridgeDep,
    fridge_product_id: int,
    meal_date: date,
    meal_type: MealType,
    weight: WeightRequest,
):
    return await meal_service.add_fridge_product_to_meal(
        user.id, fridge.id, fridge_product_id, meal_date, meal_type, weight
    )


@router.post(
    "/{meal_date}/{meal_type}/ingredients/from-fridge-meal/{fridge_meal_id}",
    response_model=list[MealIngredientRead],
)
async def add_fridge_meal_to_meal(
    meal_service: MealServiceDep,
    user: UserDep,
    fridge: FridgeDep,
    fridge_meal_id: int,
    meal_date: date,
    meal_type: MealType,
    weight: WeightRequest,
):
    return await meal_service.add_fridge_meal_to_meal(
        user.id, fridge.id, fridge_meal_id, meal_date, meal_type, weight
    )
