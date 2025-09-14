from app.models import *
from sqlalchemy.orm import Session
from app.schemas.meals import *
from app.utils.crud_fridge import *
from app.enums import MealType
from datetime import date

#Meal

def create_meal(db: Session, data: MealCreate):
    return create_instance(db, Meal, data)

def get_meal(db: Session, user_id: int, meal_date: datetime, meal_type: MealType):
    return (
        db.query(Meal)
        .filter(Meal.user_id == user_id)
        .filter(Meal.date == meal_date)
        .filter(Meal.type == meal_type)
        .all()
    )

def get_meal_by_id(db: Session, meal_id: int):
    return db.query(Meal).filter(Meal.id == meal_id).first()

def delete_meal(db: Session, meal_id: int):
    return delete_fridge_object(db, Meal, meal_id)

def get_meal_nutrient_sum(db: Session, meal_id: int, nutrient_type: str):
    ingredients = get_meal_ingredients(db, meal_id)
    total = 0.0
    return sum(
        (getattr(ing.fridge_product, nutrient_type, 0) * ing.weight) / 100
        for ing in ingredients
    )

def get_meal_macro(db: Session, meal_id: int):
    fields = ["calories_100g", "proteins_100g", "fats_100g", "carbs_100g"]
    return {
        field.replace("_100g", ""): get_meal_nutrient_sum(db, meal_id, field)
        for field in fields
    }

def get_meals_nutrient_sum_for_day(db: Session, user_id: int, meal_date: date, nutrient_type: str):
    meals = db.query(Meal).filter(Meal.user_id == user_id).filter(Meal.date == meal_date).all()
    return sum(get_meal_nutrient_sum(db, meal.id, nutrient_type) for meal in meals)

def get_macro_for_day(db: Session, user_id: int, meal_date: date):
    fields = ["calories_100g", "proteins_100g", "fats_100g", "carbs_100g"]
    return {
        field.replace("_100g", ""): get_meals_nutrient_sum_for_day(db, user_id, meal_date, field)
        for field in fields
    }

# Meal ingredient

def add_ingredient_to_meal(db: Session, data: MealIngredientCreate):
    get_fridge_object_or_404(db, Meal, data.meal_id)
    return create_instance(db, MealIngredient, data)

def get_meal_ingredients(db: Session, meal_id: int):
    return db.query(MealIngredient).filter(MealIngredient.meal_id == meal_id).all()

def get_meal_ingredient_by_id(db: Session, ingredient_id: int):
    return db.query(MealIngredient).filter(MealIngredient.id == ingredient_id).first()

def update_meal_ingredient(db: Session, ingredient_id: int, data: MealIngredientUpdate):
    return update_fridge_object(db, MealIngredient, ingredient_id, data)

def delete_meal_ingredient(db: Session, ingredient_id: int):
    return delete_fridge_object(db, MealIngredient, ingredient_id)
