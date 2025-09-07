from app.models import *
from sqlalchemy.orm import Session
from app.schemas.fridge import *

#Fridge products

def create_fridge_product(db: Session, data: FridgeProductCreate):
    product_in = FridgeProduct(**data.model_dump())
    db.add(product_in)
    db.commit()
    db.refresh(product_in)
    return product_in

def get_fridge_products(db: Session):
    return db.query(FridgeProduct).all()

def get_fridge_product(db: Session, product_id: int):
    return db.query(FridgeProduct).filter(FridgeProduct.id == product_id).first()

def delete_fridge_product(db: Session, product_id: int):
    product = db.query(FridgeProduct).filter(FridgeProduct.id == product_id).first()
    if not product:
        raise ValueError("Fridge product not found")
    db.delete(product)
    db.commit()
    return product

#Fridge meals

def create_fridge_meal(db: Session, data: FridgeMealCreate):
    fridge_meal_in = FridgeMeal(**data.model_dump())
    db.add(fridge_meal_in)
    db.commit()
    db.refresh(fridge_meal_in)
    return fridge_meal_in

def get_fridge_meals(db: Session):
    return db.query(FridgeMeal).all()

def get_fridge_meal(db: Session, meal_id: int):
    return db.query(FridgeMeal).filter(FridgeMeal.id == meal_id).first()

def delete_fridge_meal(db: Session, meal_id: int):
    meal = db.query(FridgeMeal).filter(FridgeMeal.id == meal_id).first()
    if not meal:
        raise ValueError("Meal not found")
    db.delete(meal)
    db.commit()
    return meal

#Fridge meal ingredients

def add_product_to_fridge_meal(db: Session, data: FridgeMealIngredientCreate):
    meal = db.query(FridgeMeal).filter(FridgeMeal.id == data.fridge_meal_id).first()
    if not meal:
        raise ValueError("Fridge meal not found")
    fridge_meal_ingredient_in = FridgeMealIngredient(**data.model_dump())
    db.add(fridge_meal_ingredient_in)
    db.commit()
    db.refresh(fridge_meal_ingredient_in)
    return fridge_meal_ingredient_in

def get_fridge_meal_ingredients(db: Session):
    return db.query(FridgeMealIngredient).all()

def get_fridge_meal_ingredient(db: Session, meal_id: int):
    return db.query(FridgeMeal).filter(FridgeMeal.id == meal_id).first()

def delete_product_from_fridge_meal(db: Session, product_id: int):
    product = db.query(FridgeMealIngredient).filter(FridgeMealIngredient.id == product_id).first()
    if not product:
        raise ValueError("Product not found")
    db.delete(product)
    db.commit()
    return product