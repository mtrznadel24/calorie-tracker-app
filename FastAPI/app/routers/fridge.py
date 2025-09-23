from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.enums import NutrientType, FoodCategory
from app.schemas.fridge import (
    FridgeProductCreate, FridgeProductRead, FridgeProductUpdate,
    FridgeMealCreate, FridgeMealRead, FridgeMealUpdate,
    FridgeMealIngredientCreate, FridgeMealIngredientRead, FridgeMealIngredientUpdate
)
from app.services.fridge import (
    create_fridge_product, get_fridge_products, get_fridge_product,
    update_fridge_product, delete_fridge_product,
    create_fridge_meal, get_fridge_meals, get_fridge_meal,
    update_fridge_meal, delete_fridge_meal,
    get_fridge_meal_nutrient_sum, get_fridge_meal_macro,
    add_fridge_meal_ingredient, get_fridge_meal_ingredients,
    get_fridge_meal_ingredient, update_fridge_meal_ingredient,
    delete_fridge_meal_ingredient
)
from typing import List, Dict

router = APIRouter(prefix="/fridges", tags=["fridges"])

#Fridge products

@router.post("/{fridge_id}/products", response_model=FridgeProductRead)
def add_fridge_product_route(fridge_id: int, product_in: FridgeProductCreate, db: Session = Depends(get_db)):
    return create_fridge_product(db, fridge_id, product_in)

@router.get("/{fridge_id}/products", response_model=List[FridgeProductRead])
def read_fridge_products_route(
        fridge_id: int,
        is_favourite: bool = False,
        category: FoodCategory = None,
        skip: int = 0, limit: int = 25,
        db: Session = Depends(get_db)
):
    return get_fridge_products(db, fridge_id, is_favourite, category, skip, limit)

@router.get("/{fridge_id}/products/{product_id}", response_model=FridgeProductRead)
def read_fridge_product_route(fridge_id: int, product_id: int, db: Session = Depends(get_db)):
    return get_fridge_product(db, fridge_id, product_id)

@router.put("/{fridge_id}/products/{product_id}", response_model=FridgeProductRead)
def update_fridge_product_route(fridge_id: int, product_id: int, product_in: FridgeProductUpdate, db: Session = Depends(get_db)):
    return update_fridge_product(db, fridge_id, product_id, product_in)

@router.delete("/{fridge_id}/products/{product_id}", response_model=FridgeProductRead)
def delete_fridge_product_route(fridge_id: int, product_id: int, db: Session = Depends(get_db)):
    return delete_fridge_product(db, fridge_id, product_id)

#Fridge meals

@router.post("/{fridge_id}/meals", response_model=FridgeMealRead)
def add_fridge_meal_route(fridge_id: int, meal_in: FridgeMealCreate, db: Session = Depends(get_db)):
    return create_fridge_meal(db, fridge_id, meal_in)

@router.get("/{fridge_id}/meals", response_model=List[FridgeMealRead])
def read_fridge_meals_route(
        fridge_id: int,
        is_favourite: bool = False,
        skip: int = 0, limit: int = 25,
        db: Session = Depends(get_db)
):
    return get_fridge_meals(db, fridge_id, is_favourite, skip, limit)

@router.get("/{fridge_id}/meals/{meal_id}", response_model=FridgeMealRead)
def read_fridge_meal_route(fridge_id: int, meal_id: int, db: Session = Depends(get_db)):
    return get_fridge_meal(db, fridge_id, meal_id)

@router.put("/{fridge_id}/meals/{meal_id}", response_model=FridgeMealRead)
def update_fridge_meal_route(fridge_id: int, meal_id: int, meal_in: FridgeMealUpdate, db: Session = Depends(get_db)):
    return update_fridge_meal(db, fridge_id, meal_id, meal_in)
@router.delete("/{fridge_id}/meals/{meal_id}", response_model=FridgeMealRead)
def delete_fridge_meal_route(fridge_id: int, meal_id: int, db: Session = Depends(get_db)):
    return delete_fridge_meal(db, fridge_id, meal_id)

@router.get("/{fridge_id}/meals/{meal_id}/nutrients/{nutrient_type}", response_model=float)
def read_fridge_meal_nutrient_sum_route(fridge_id: int, meal_id: int, nutrient_type: NutrientType, db: Session = Depends(get_db)):
    return get_fridge_meal_nutrient_sum(db, fridge_id, meal_id, nutrient_type)

@router.get("/{fridge_id}/meals/{meal_id}/macros", response_model=Dict[str, float])
def read_fridge_meal_macros_route(fridge_id: int, meal_id: int, db: Session = Depends(get_db)):
    return get_fridge_meal_macro(db, fridge_id, meal_id)

#Fridge meal ingredients

@router.post("/{fridge_id}/meals/{meal_id}/ingredients", response_model=FridgeMealIngredientRead)
def add_fridge_meal_ingredient_route(fridge_id: int, meal_id: int, ingredient_in: FridgeMealIngredientCreate, db: Session = Depends(get_db)):
    return add_fridge_meal_ingredient(db, fridge_id, meal_id, ingredient_in)

@router.get("/{fridge_id}/meals/{meal_id}/ingredients", response_model=List[FridgeMealIngredientRead])
def read_fridge_meal_ingredients_route(fridge_id: int, meal_id: int, db: Session = Depends(get_db)):
    return get_fridge_meal_ingredients(db, fridge_id, meal_id)

@router.get("/{fridge_id}/meals/{meal_id}/ingredients/{ingredient_id}", response_model=FridgeMealIngredientRead)
def read_fridge_meal_ingredient_route(fridge_id: int, meal_id: int, ingredient_id: int, db: Session = Depends(get_db)):
    return get_fridge_meal_ingredient(db, fridge_id, meal_id, ingredient_id)

@router.put("/{fridge_id}/meals/{meal_id}/ingredients/{ingredient_id}", response_model=FridgeMealIngredientRead)
def update_fridge_meal_ingredient_route(fridge_id: int, meal_id: int, ingredient_id: int, ingredient_in: FridgeMealIngredientUpdate, db: Session = Depends(get_db)):
    return update_fridge_meal_ingredient(db, fridge_id, meal_id, ingredient_id, ingredient_in)

@router.delete("/{fridge_id}/meals/{meal_id}/ingredients/{ingredient_id}", response_model=FridgeMealIngredientRead)
def delete_fridge_meal_ingredient_route(fridge_id: int, meal_id: int, ingredient_id: int, db: Session = Depends(get_db)):
    return delete_fridge_meal_ingredient(db, fridge_id, meal_id, ingredient_id)

