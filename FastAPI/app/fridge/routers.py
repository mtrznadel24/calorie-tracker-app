from collections.abc import Sequence

from fastapi import APIRouter

from app.fridge.dependencies import FridgeDep, FridgeServiceDep
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
from app.utils.enums import NutrientType

router = APIRouter(prefix="/fridge", tags=["fridge"])

# Fridge products


@router.post("/products", response_model=FridgeProductRead)
async def add_fridge_product(
    fridge_service: FridgeServiceDep, fridge: FridgeDep, product_in: FridgeProductCreate
) -> FridgeProduct:
    return await fridge_service.create_fridge_product(fridge.id, product_in)


@router.get("/products", response_model=list[FridgeProductRead])
async def read_fridge_products(
    fridge_service: FridgeServiceDep,
    fridge: FridgeDep,
    is_favourite: bool = False,
    category: FoodCategory | None = None,
    skip: int = 0,
    limit: int = 25,
) -> Sequence[FridgeProduct]:
    return await fridge_service.get_fridge_products(
        fridge.id, is_favourite, category, skip, limit
    )


@router.get("/products/{product_id}", response_model=FridgeProductRead)
async def read_fridge_product(
    fridge_service: FridgeServiceDep, fridge: FridgeDep, product_id: int
) -> FridgeProduct:
    return await fridge_service.get_fridge_product(fridge.id, product_id)


@router.put("/products/{product_id}", response_model=FridgeProductRead)
async def update_fridge_product(
    fridge_service: FridgeServiceDep,
    fridge: FridgeDep,
    product_id: int,
    product_in: FridgeProductUpdate,
) -> FridgeProduct:
    return await fridge_service.update_fridge_product(fridge.id, product_id, product_in)


@router.delete("/products/{product_id}", response_model=FridgeProductRead)
async def delete_fridge_product(
    fridge_service: FridgeServiceDep, fridge: FridgeDep, product_id: int
):
    return await fridge_service.delete_fridge_product(fridge.id, product_id)


# Fridge meals


@router.post("/meals", response_model=FridgeMealRead)
async def add_fridge_meal(
    fridge_service: FridgeServiceDep, fridge: FridgeDep, meal_in: FridgeMealCreate
) -> FridgeMeal:
    return await fridge_service.create_fridge_meal(fridge.id, meal_in)


@router.get("/meals", response_model=list[FridgeMealRead])
async def read_fridge_meals(
    fridge_service: FridgeServiceDep,
    fridge: FridgeDep,
    is_favourite: bool = False,
    skip: int = 0,
    limit: int = 25,
) -> Sequence[FridgeMeal]:
    return await fridge_service.get_fridge_meals(fridge.id, is_favourite, skip, limit)


@router.get("/meals/{meal_id}", response_model=FridgeMealRead)
async def read_fridge_meal(
    fridge_service: FridgeServiceDep, fridge: FridgeDep, meal_id: int
) -> FridgeMeal:
    return await fridge_service.get_fridge_meal(fridge.id, meal_id)


@router.put("/meals/{meal_id}", response_model=FridgeMealRead)
async def update_fridge_meal(
    fridge_service: FridgeServiceDep,
    fridge: FridgeDep,
    meal_id: int,
    meal_in: FridgeMealUpdate,
) -> FridgeMeal:
    return await fridge_service.update_fridge_meal(fridge.id, meal_id, meal_in)


@router.delete("/meals/{meal_id}", response_model=FridgeMealRead)
async def delete_fridge_meal(
    fridge_service: FridgeServiceDep, fridge: FridgeDep, meal_id: int
) -> FridgeMeal:
    return await fridge_service.delete_fridge_meal(fridge.id, meal_id)


@router.get("/meals/{meal_id}/nutrients/{nutrient_type}", response_model=float)
async def read_fridge_meal_nutrient_sum(
    fridge_service: FridgeServiceDep,
    fridge: FridgeDep,
    meal_id: int,
    nutrient_type: NutrientType,
) -> float:
    return await fridge_service.get_fridge_meal_nutrient_sum(
        fridge.id, meal_id, nutrient_type
    )


@router.get("/meals/{meal_id}/macros", response_model=dict[str, float])
async def read_fridge_meal_macro(
    fridge_service: FridgeServiceDep, fridge: FridgeDep, meal_id: int
) -> dict[str, float]:
    return await fridge_service.get_fridge_meal_macro(fridge.id, meal_id)


# Fridge meal ingredients


@router.post("/meals/{meal_id}/ingredients", response_model=FridgeMealIngredientRead)
async def add_fridge_meal_ingredient(
    fridge_service: FridgeServiceDep,
    fridge: FridgeDep,
    meal_id: int,
    ingredient_in: FridgeMealIngredientCreate,
) -> FridgeMealIngredient:
    return await fridge_service.add_fridge_meal_ingredient(
        fridge.id, meal_id, ingredient_in
    )


@router.get(
    "/meals/{meal_id}/ingredients",
    response_model=list[FridgeMealIngredientRead],
)
async def read_fridge_meal_ingredients(
    fridge_service: FridgeServiceDep, fridge: FridgeDep, meal_id: int
) -> Sequence[FridgeMealIngredient]:
    return await fridge_service.get_fridge_meal_ingredients(fridge.id, meal_id)


@router.get(
    "/meals/{meal_id}/ingredients/{ingredient_id}",
    response_model=FridgeMealIngredientRead,
)
async def read_fridge_meal_ingredient(
    fridge_service: FridgeServiceDep,
    fridge: FridgeDep,
    meal_id: int,
    ingredient_id: int,
) -> FridgeMealIngredient:
    return await fridge_service.get_fridge_meal_ingredient(
        fridge.id, meal_id, ingredient_id
    )


@router.put(
    "/meals/{meal_id}/ingredients/{ingredient_id}",
    response_model=FridgeMealIngredientRead,
)
async def update_fridge_meal_ingredient(
    fridge_service: FridgeServiceDep,
    fridge: FridgeDep,
    meal_id: int,
    ingredient_id: int,
    ingredient_in: FridgeMealIngredientUpdate,
) -> FridgeMealIngredient:
    return await fridge_service.update_fridge_meal_ingredient(
        fridge.id, meal_id, ingredient_id, ingredient_in
    )


@router.delete(
    "/meals/{meal_id}/ingredients/{ingredient_id}",
    response_model=FridgeMealIngredientRead,
)
async def delete_fridge_meal_ingredient(
    fridge_service: FridgeServiceDep,
    fridge: FridgeDep,
    meal_id: int,
    ingredient_id: int,
) -> FridgeMealIngredient:
    return await fridge_service.delete_fridge_meal_ingredient(
        fridge.id, meal_id, ingredient_id
    )
