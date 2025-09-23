from sqlalchemy.orm import Session
from app.models import Meal, MealIngredient, User, MealIngredientDetails
from app.schemas.meals import MealCreate, MealIngredientCreate, MealIngredientUpdate
from app.utils.crud import get_or_404, create_instance, delete_by_id, update_by_id
from app.enums import MealType, NutrientType
from app.exceptions import NotFoundError
from datetime import date


#Meal Utils

def get_user_meal_or_404(db: Session, user_id: int, meal_id: int):
    meal = db.query(Meal).filter(Meal.id == meal_id, Meal.user_id == user_id).first()
    if not meal:
        raise NotFoundError("Meal not found")
    return meal

#Meal

def create_meal(db: Session, user_id: int, data: MealCreate):
    user = get_or_404(db, User, user_id)
    return create_instance(db, Meal, data.model_dump())

def get_meal(db: Session, user_id: int, meal_date: date, meal_type: MealType):
    return (
        db.query(Meal)
        .filter(Meal.user_id == user_id)
        .filter(Meal.date == meal_date)
        .filter(Meal.type == meal_type)
        .all()
    )

def get_meal_by_id(db: Session, user_id: int, meal_id: int):
    user = get_or_404(db, User, user_id)
    return get_or_404(db, Meal, meal_id)

def delete_meal(db: Session, user_id: int, meal_id: int):
    user = get_or_404(db, User, user_id)
    return delete_by_id(db, Meal, meal_id)

def get_meal_nutrient_sum(db: Session, user_id: int, meal_id: int, nutrient_type: NutrientType):
    ingredients = get_meal_ingredients(db, user_id=user_id, meal_id=meal_id)
    return sum(
        (getattr(ing.details, nutrient_type.value, 0) * ing.weight) / 100
        for ing in ingredients
    )

def get_meal_macro(db: Session, user_id: int, meal_id: int):
    fields = [
        NutrientType.CALORIES,
        NutrientType.PROTEINS,
        NutrientType.FATS,
        NutrientType.CARBS
    ]
    return {
        field.value.replace("_100g", ""): get_meal_nutrient_sum(db, user_id, meal_id, field)
        for field in fields
    }

def get_meals_nutrient_sum_for_day(db: Session, user_id: int, meal_date: date, nutrient_type: NutrientType):
    meals = db.query(Meal).filter(Meal.user_id == user_id).filter(Meal.date == meal_date).all()
    return sum(get_meal_nutrient_sum(db, user_id, meal.id, nutrient_type) for meal in meals)

def get_macro_for_day(db: Session, user_id: int, meal_date: date):
    fields = [
        NutrientType.CALORIES,
        NutrientType.PROTEINS,
        NutrientType.FATS,
        NutrientType.CARBS
    ]
    return {
        field.value.replace("_100g", ""): get_meals_nutrient_sum_for_day(db, user_id, meal_date, field)
        for field in fields
    }

# Meal ingredient

def add_ingredient_to_meal(db: Session, user_id: int, meal_id: int, data: MealIngredientCreate):
    meal = get_user_meal_or_404(db, user_id, meal_id)
    ingredient = MealIngredient(
        weight=data.weight,
        meal_id=meal_id
    )
    db.add(ingredient)
    db.flush()

    details = MealIngredientDetails(
        id=ingredient.id,
        **data.details.model_dump()
    )
    db.add(details)

    db.commit()
    db.refresh(ingredient)
    return ingredient

def get_meal_ingredients(db: Session, user_id: int, meal_id: int):
    get_user_meal_or_404(db, user_id, meal_id)
    return db.query(MealIngredient).filter(MealIngredient.meal_id == meal_id).all()

def get_meal_ingredient_by_id(db: Session, user_id: int, meal_id, ingredient_id: int):
    get_user_meal_or_404(db, user_id, meal_id)
    return db.query(MealIngredient).filter(MealIngredient.id == ingredient_id, MealIngredient.meal_id == meal_id).first()

def update_meal_ingredient(db: Session, user_id: int, meal_id, ingredient_id: int, data: MealIngredientUpdate):
    get_user_meal_or_404(db, user_id, meal_id)
    ingredient = get_or_404(db, MealIngredient, ingredient_id)

    if data.weight:
        update_by_id(db, MealIngredient, ingredient_id, {"weight": data.weight})

    if data.details:
        update_by_id(db, MealIngredientDetails, ingredient.details.id, data.details.model_dump())

    return ingredient

def delete_meal_ingredient(db: Session, user_id: int, meal_id, ingredient_id: int):
    get_user_meal_or_404(db, user_id, meal_id)
    return delete_by_id(db, MealIngredient, ingredient_id)

def get_ingredient_details(db: Session, user_id: int, meal_id, ingredient_id: int):
    get_user_meal_or_404(db, user_id, meal_id)
    ingredient = get_or_404(db, MealIngredient, ingredient_id)
    return ingredient.details


