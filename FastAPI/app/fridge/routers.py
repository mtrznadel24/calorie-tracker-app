from collections.abc import Sequence
from typing import Dict, List, Optional

from fastapi import APIRouter

from app.core.enums import NutrientType
from app.fridge.dependencies import FridgeServiceDep
from app.fridge.models import (
    FoodCategory,
    FridgeMeal,
    FridgeMealIngredient,
    FridgeProduct,
)
from app.fridge.schemas import (
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

router = APIRouter(prefix="/fridges", tags=["fridges"])

# Fridge products


@router.post("/{fridge_id}/products", response_model=FridgeProductRead)
async def add_fridge_product_route(
    fridge_service: FridgeServiceDep, fridge_id: int, product_in: FridgeProductCreate
) -> FridgeProduct:
    return await fridge_service.create_fridge_product(fridge_id, product_in)


@router.get("/{fridge_id}/products", response_model=List[FridgeProductRead])
async def read_fridge_products_route(
    fridge_service: FridgeServiceDep,
    fridge_id: int,
    is_favourite: bool = False,
    category: Optional[FoodCategory] = None,
    skip: int = 0,
    limit: int = 25,
) -> Sequence[FridgeProduct]:
    return await fridge_service.get_fridge_products(
        fridge_id, is_favourite, category, skip, limit
    )


@router.get("/{fridge_id}/products/{product_id}", response_model=FridgeProductRead)
async def read_fridge_product_route(
    fridge_service: FridgeServiceDep, fridge_id: int, product_id: int
) -> FridgeProduct:
    return await fridge_service.get_fridge_product(fridge_id, product_id)


@router.put("/{fridge_id}/products/{product_id}", response_model=FridgeProductRead)
async def update_fridge_product_route(
    fridge_service: FridgeServiceDep,
    fridge_id: int,
    product_id: int,
    product_in: FridgeProductUpdate,
) -> FridgeProduct:
    return await fridge_service.update_fridge_product(fridge_id, product_id, product_in)


@router.delete("/{fridge_id}/products/{product_id}", response_model=FridgeProductRead)
async def delete_fridge_product_route(
    fridge_service: FridgeServiceDep, fridge_id: int, product_id: int
):
    return await fridge_service.delete_fridge_product(fridge_id, product_id)


# Fridge meals


@router.post("/{fridge_id}/meals", response_model=FridgeMealRead)
async def add_fridge_meal_route(
    fridge_service: FridgeServiceDep, fridge_id: int, meal_in: FridgeMealCreate
) -> FridgeMeal:
    return await fridge_service.create_fridge_meal(fridge_id, meal_in)


@router.get("/{fridge_id}/meals", response_model=List[FridgeMealRead])
async def read_fridge_meals_route(
    fridge_service: FridgeServiceDep,
    fridge_id: int,
    is_favourite: bool = False,
    skip: int = 0,
    limit: int = 25,
) -> Sequence[FridgeMeal]:
    return await fridge_service.get_fridge_meals(fridge_id, is_favourite, skip, limit)


@router.get("/{fridge_id}/meals/{meal_id}", response_model=FridgeMealRead)
async def read_fridge_meal_route(
    fridge_service: FridgeServiceDep, fridge_id: int, meal_id: int
) -> FridgeMeal:
    return await fridge_service.get_fridge_meal(fridge_id, meal_id)


@router.put("/{fridge_id}/meals/{meal_id}", response_model=FridgeMealRead)
async def update_fridge_meal_route(
    fridge_service: FridgeServiceDep,
    fridge_id: int,
    meal_id: int,
    meal_in: FridgeMealUpdate,
) -> FridgeMeal:
    return await fridge_service.update_fridge_meal(fridge_id, meal_id, meal_in)


@router.delete("/{fridge_id}/meals/{meal_id}", response_model=FridgeMealRead)
async def delete_fridge_meal_route(
    fridge_service: FridgeServiceDep, fridge_id: int, meal_id: int
) -> FridgeMeal:
    return await fridge_service.delete_fridge_meal(fridge_id, meal_id)


@router.get(
    "/{fridge_id}/meals/{meal_id}/nutrients/{nutrient_type}", response_model=float
)
async def read_fridge_meal_nutrient_sum_route(
    fridge_service: FridgeServiceDep,
    fridge_id: int,
    meal_id: int,
    nutrient_type: NutrientType,
) -> float:
    return await fridge_service.get_fridge_meal_nutrient_sum(
        fridge_id, meal_id, nutrient_type
    )


@router.get("/{fridge_id}/meals/{meal_id}/macros", response_model=Dict[str, float])
async def read_fridge_meal_macro_route(
    fridge_service: FridgeServiceDep, fridge_id: int, meal_id: int
) -> Dict[str, float]:
    return await fridge_service.get_fridge_meal_macro(fridge_id, meal_id)


# Fridge meal ingredients


@router.post(
    "/{fridge_id}/meals/{meal_id}/ingredients", response_model=FridgeMealIngredientRead
)
async def add_fridge_meal_ingredient_route(
    fridge_service: FridgeServiceDep,
    fridge_id: int,
    meal_id: int,
    ingredient_in: FridgeMealIngredientCreate,
) -> FridgeMealIngredient:
    return await fridge_service.add_fridge_meal_ingredient(
        fridge_id, meal_id, ingredient_in
    )


@router.get(
    "/{fridge_id}/meals/{meal_id}/ingredients",
    response_model=List[FridgeMealIngredientRead],
)
async def read_fridge_meal_ingredients_route(
    fridge_service: FridgeServiceDep, fridge_id: int, meal_id: int
) -> Sequence[FridgeMealIngredient]:
    return await fridge_service.get_fridge_meal_ingredients(fridge_id, meal_id)


@router.get(
    "/{fridge_id}/meals/{meal_id}/ingredients/{ingredient_id}",
    response_model=FridgeMealIngredientRead,
)
async def read_fridge_meal_ingredient_route(
    fridge_service: FridgeServiceDep, fridge_id: int, meal_id: int, ingredient_id: int
) -> FridgeMealIngredient:
    return await fridge_service.get_fridge_meal_ingredient(
        fridge_id, meal_id, ingredient_id
    )


@router.put(
    "/{fridge_id}/meals/{meal_id}/ingredients/{ingredient_id}",
    response_model=FridgeMealIngredientRead,
)
async def update_fridge_meal_ingredient_route(
    fridge_service: FridgeServiceDep,
    fridge_id: int,
    meal_id: int,
    ingredient_id: int,
    ingredient_in: FridgeMealIngredientUpdate,
) -> FridgeMealIngredient:
    return await fridge_service.update_fridge_meal_ingredient(
        fridge_id, meal_id, ingredient_id, ingredient_in
    )


@router.delete(
    "/{fridge_id}/meals/{meal_id}/ingredients/{ingredient_id}",
    response_model=FridgeMealIngredientRead,
)
async def delete_fridge_meal_ingredient_route(
    fridge_service: FridgeServiceDep, fridge_id: int, meal_id: int, ingredient_id: int
) -> FridgeMealIngredient:
    return await fridge_service.delete_fridge_meal_ingredient(
        fridge_id, meal_id, ingredient_id
    )
