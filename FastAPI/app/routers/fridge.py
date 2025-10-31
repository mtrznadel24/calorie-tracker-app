from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.enums import NutrientType
from app.models.fridge import FoodCategory
from app.schemas.fridge import (
    FridgeMealCreate,
    FridgeMealIngredientCreate,
    FridgeMealIngredientRead,
    FridgeMealIngredientUpdate,
    FridgeMealRead,
    FridgeMealUpdate,
    FridgeProductCreate,
    FridgeProductRead,
    FridgeProductUpdate,
)
from app.services.fridge import (
    add_fridge_meal_ingredient,
    create_fridge_meal,
    create_fridge_product,
    delete_fridge_meal,
    delete_fridge_meal_ingredient,
    delete_fridge_product,
    get_fridge_meal,
    get_fridge_meal_ingredient,
    get_fridge_meal_ingredients,
    get_fridge_meal_macro,
    get_fridge_meal_nutrient_sum,
    get_fridge_meals,
    get_fridge_product,
    get_fridge_products,
    update_fridge_meal,
    update_fridge_meal_ingredient,
    update_fridge_product,
)
from app.core.db import DbSessionDep

router = APIRouter(prefix="/fridges", tags=["fridges"])

# Fridge products


@router.post("/{fridge_id}/products", response_model=FridgeProductRead)
def add_fridge_product_route(
    fridge_id: int, product_in: FridgeProductCreate, db: DbSessionDep
):
    return create_fridge_product(db, fridge_id, product_in)


@router.get("/{fridge_id}/products", response_model=List[FridgeProductRead])
def read_fridge_products_route(
    db: DbSessionDep,
    fridge_id: int,
    is_favourite: bool = False,
    category: Optional[FoodCategory] = None,
    skip: int = 0,
    limit: int = 25
):
    return get_fridge_products(db, fridge_id, is_favourite, category, skip, limit)


@router.get("/{fridge_id}/products/{product_id}", response_model=FridgeProductRead)
def read_fridge_product_route(
    db: DbSessionDep, fridge_id: int, product_id: int
):
    return get_fridge_product(db, fridge_id, product_id)


@router.put("/{fridge_id}/products/{product_id}", response_model=FridgeProductRead)
def update_fridge_product_route(
    db: DbSessionDep,
    fridge_id: int,
    product_id: int,
    product_in: FridgeProductUpdate,
):
    return update_fridge_product(db, fridge_id, product_id, product_in)


@router.delete("/{fridge_id}/products/{product_id}", response_model=FridgeProductRead)
def delete_fridge_product_route(
    db: DbSessionDep, fridge_id: int, product_id: int
):
    return delete_fridge_product(db, fridge_id, product_id)


# Fridge meals


@router.post("/{fridge_id}/meals", response_model=FridgeMealRead)
def add_fridge_meal_route(
    db: DbSessionDep, fridge_id: int, meal_in: FridgeMealCreate
):
    return create_fridge_meal(db, fridge_id, meal_in)


@router.get("/{fridge_id}/meals", response_model=List[FridgeMealRead])
def read_fridge_meals_route(
    db: DbSessionDep,
    fridge_id: int,
    is_favourite: bool = False,
    skip: int = 0,
    limit: int = 25
):
    return get_fridge_meals(db, fridge_id, is_favourite, skip, limit)


@router.get("/{fridge_id}/meals/{meal_id}", response_model=FridgeMealRead)
def read_fridge_meal_route(db: DbSessionDep, fridge_id: int, meal_id: int):
    return get_fridge_meal(db, fridge_id, meal_id)


@router.put("/{fridge_id}/meals/{meal_id}", response_model=FridgeMealRead)
def update_fridge_meal_route(
    db: DbSessionDep,
    fridge_id: int,
    meal_id: int,
    meal_in: FridgeMealUpdate,
):
    return update_fridge_meal(db, fridge_id, meal_id, meal_in)


@router.delete("/{fridge_id}/meals/{meal_id}", response_model=FridgeMealRead)
def delete_fridge_meal_route(
    db: DbSessionDep, fridge_id: int, meal_id: int
):
    return delete_fridge_meal(db, fridge_id, meal_id)


@router.get(
    "/{fridge_id}/meals/{meal_id}/nutrients/{nutrient_type}", response_model=float
)
def read_fridge_meal_nutrient_sum_route(
    db: DbSessionDep,
    fridge_id: int,
    meal_id: int,
    nutrient_type: NutrientType,
):
    return get_fridge_meal_nutrient_sum(db, fridge_id, meal_id, nutrient_type)


@router.get("/{fridge_id}/meals/{meal_id}/macros", response_model=Dict[str, float])
def read_fridge_meal_macros_route(
    db: DbSessionDep, fridge_id: int, meal_id: int
):
    return get_fridge_meal_macro(db, fridge_id, meal_id)


# Fridge meal ingredients


@router.post(
    "/{fridge_id}/meals/{meal_id}/ingredients", response_model=FridgeMealIngredientRead
)
def add_fridge_meal_ingredient_route(
    db: DbSessionDep,
    fridge_id: int,
    meal_id: int,
    ingredient_in: FridgeMealIngredientCreate,
):
    return add_fridge_meal_ingredient(db, fridge_id, meal_id, ingredient_in)


@router.get(
    "/{fridge_id}/meals/{meal_id}/ingredients",
    response_model=List[FridgeMealIngredientRead],
)
def read_fridge_meal_ingredients_route(
    db: DbSessionDep, fridge_id: int, meal_id: int
):
    return get_fridge_meal_ingredients(db, fridge_id, meal_id)


@router.get(
    "/{fridge_id}/meals/{meal_id}/ingredients/{ingredient_id}",
    response_model=FridgeMealIngredientRead,
)
def read_fridge_meal_ingredient_route(
    db: DbSessionDep, fridge_id: int, meal_id: int, ingredient_id: int
):
    return get_fridge_meal_ingredient(db, fridge_id, meal_id, ingredient_id)


@router.put(
    "/{fridge_id}/meals/{meal_id}/ingredients/{ingredient_id}",
    response_model=FridgeMealIngredientRead,
)
def update_fridge_meal_ingredient_route(
    db: DbSessionDep,
    fridge_id: int,
    meal_id: int,
    ingredient_id: int,
    ingredient_in: FridgeMealIngredientUpdate,
):
    return update_fridge_meal_ingredient(
        db, fridge_id, meal_id, ingredient_id, ingredient_in
    )


@router.delete(
    "/{fridge_id}/meals/{meal_id}/ingredients/{ingredient_id}",
    response_model=FridgeMealIngredientRead,
)
def delete_fridge_meal_ingredient_route(
    db: DbSessionDep, fridge_id: int, meal_id: int, ingredient_id: int
):
    return delete_fridge_meal_ingredient(db, fridge_id, meal_id, ingredient_id)
