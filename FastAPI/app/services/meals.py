from app.models import *
from sqlalchemy.orm import Session
from app.schemas.meals import *


#Meal

def create_meal(db: Session, data: MealCreate):
    meal_in = Meal(**data.model_dump())
    db.add(meal_in)
    db.commit()
    db.refresh(meal_in)
    return meal_in

def get_meals(db: Session):
    return db.query(Meal).all()

def get_meal(db: Session, meal_id: int):
    return db.query(Meal).filter(Meal.id == meal_id).first()

def add_product_to_meal(db: Session, product: MealIngredient):
    meal = db.query(Meal).filter(Meal.id == product.meal_id).first()
    if not meal:
        raise ValueError('Meal not found')

# Meal ingredient

def add_ingredient_to_meal(db: Session, data: MealIngredientCreate):
    ingredient_in = MealIngredient(**data.model_dump())
    db.add(ingredient_in)
    db.commit()
    db.refresh(ingredient_in)
    return ingredient_in

def get_meal_ingredients(db: Session):
    return db.query(MealIngredient).all()

def get_meal_ingredient(db: Session, meal_id: int):
    return db.query(MealIngredient).filter(MealIngredient.meal_id == meal_id).first()