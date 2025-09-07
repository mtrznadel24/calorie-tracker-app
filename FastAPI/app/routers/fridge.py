from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.fridge import *
from app.services.fridge import *
from typing import List

from app.routers import meals

router = APIRouter(prefix="/fridge", tags=["fridge"])

@router.post("/products", response_model=FridgeProductRead)
def add_fridge_product(product_in: FridgeProductCreate, db: Session = Depends(get_db)):
    return create_fridge_product(db, product_in)

@router.get("/products", response_model=List[FridgeProductRead])
def read_fridge_products(db: Session = Depends(get_db)):
    return get_fridge_products(db)

@router.get("/products/{product_id}", response_model=FridgeProductRead)
def read_fridge_product(product_id: int, db: Session = Depends(get_db)):
    result = get_fridge_product(db, product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Fridge product not found")
    return result

@router.post("/meals", response_model=FridgeMealRead)
def add_fridge_meal(meal_in: FridgeMealCreate, db: Session = Depends(get_db)):
    return create_fridge_meal(db, meal_in)

@router.delete("/meals/{meal_id}", response_model=FridgeMealRead)
def delete_fridge_meal(meal_id: int, db: Session = Depends(get_db)):
    return delete_fridge_meal(db, meal_id)

@router.post("/meals/products", response_model=FridgeProductRead)
def add_product_to_fridge_meal(product_in: FridgeMealIngredientCreate, db: Session = Depends(get_db)):
    return add_product_to_fridge_meal(db, product_in)

@router.delete("meals/products/{product_id}", response_model=FridgeProductRead)
def delete_product_from_fridge_meal(product_id: int, db: Session = Depends(get_db)):
    return delete_product_from_fridge_meal(db, product_id)

