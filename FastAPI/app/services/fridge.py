from sqlalchemy.orm import Session
from app.models import FridgeMeal, FridgeProduct, FridgeMealIngredient
from app.schemas.fridge import FridgeProductCreate, FridgeProductUpdate, FridgeMealCreate, FridgeMealIngredientCreate, FridgeMealIngredientUpdate, FridgeMealUpdate
from app.utils.crud_fridge import create_fridge_instance, get_fridge_object_or_404, update_fridge_object, delete_fridge_object
from app.utils.crud import create_instance, update_by_id, delete_by_id
from app.enums import FoodCategory, NutrientType


#Fridge products

def create_fridge_product(db: Session, fridge_id: int, data: FridgeProductCreate):
    return create_fridge_instance(db, FridgeProduct, fridge_id, {**data.model_dump(), "fridge_id" : fridge_id})

def get_fridge_products(db: Session, fridge_id: int, is_favourite: bool = False, category: FoodCategory = None, skip: int = 0, limit: int = 25):
    query = db.query(FridgeProduct).filter(FridgeProduct.fridge_id == fridge_id)
    if is_favourite:
        query = query.filter(FridgeProduct.is_favourite == True)
    if category is not None:
        query = query.filter(FridgeProduct.category == category)
    return query.offset(skip).limit(limit).all()

def get_fridge_product(db: Session, fridge_id: int, product_id: int):
    return get_fridge_object_or_404(db, FridgeProduct, fridge_id, product_id)

def update_fridge_product(db: Session, fridge_id: int, product_id: int, data: FridgeProductUpdate):
    return update_fridge_object(db, FridgeProduct, fridge_id, product_id, data.model_dump(exclude_unset=True))

def delete_fridge_product(db: Session, fridge_id: int, product_id: int):
    return delete_fridge_object(db, FridgeProduct, fridge_id, product_id)

#Fridge meals

def create_fridge_meal(db: Session, fridge_id: int, data: FridgeMealCreate):
    return create_fridge_instance(db, FridgeMeal, fridge_id, {**data.model_dump(), "fridge_id" : fridge_id})

def get_fridge_meals(db: Session, fridge_id: int, is_favourite: bool = False, skip: int = 0, limit: int = 25):
    query = db.query(FridgeMeal).filter(FridgeMeal.fridge_id == fridge_id)
    if is_favourite:
        query = query.filter(FridgeMeal.is_favourite == True)
    return query.offset(skip).limit(limit).all()

def get_fridge_meal(db: Session, fridge_id: int, meal_id: int):
    return get_fridge_object_or_404(db, FridgeMeal, fridge_id, meal_id)

def update_fridge_meal(db: Session, fridge_id: int, meal_id: int, data: FridgeMealUpdate):
    return update_fridge_object(db, FridgeMeal, fridge_id, meal_id, data.model_dump(exclude_unset=True))

def delete_fridge_meal(db: Session, fridge_id: int, meal_id: int):
    return delete_fridge_object(db, FridgeMeal, fridge_id, meal_id)

def get_fridge_meal_nutrient_sum(db: Session, fridge_id: int, meal_id: int, nutrient_type: NutrientType):
    ingredients = get_fridge_meal_ingredients(db, fridge_id, meal_id)
    return sum(
        (getattr(ing.fridge_product, nutrient_type.value, 0) * ing.weight) / 100
        for ing in ingredients
    )

def get_fridge_meal_macro(db: Session, fridge_id: int, meal_id: int):
    fields = [
        NutrientType.CALORIES,
        NutrientType.PROTEINS,
        NutrientType.FATS,
        NutrientType.CARBS
    ]
    return {
        field.value.replace("_100g", ""): get_fridge_meal_nutrient_sum(db, fridge_id, meal_id, field)
        for field in fields
    }

#Fridge meal ingredients

def add_fridge_meal_ingredient(db: Session, fridge_id: int, meal_id: int, data: FridgeMealIngredientCreate):
    get_fridge_object_or_404(db, FridgeMeal, fridge_id, meal_id)
    return create_instance(db, FridgeMealIngredient, {**data.model_dump(), "fridge_meal_id": meal_id})

def get_fridge_meal_ingredients(db: Session, fridge_id: int, meal_id: int):
    return (
        db.query(FridgeMealIngredient)
        .join(FridgeMeal)
        .filter(
            FridgeMeal.id == meal_id,
            FridgeMeal.fridge_id == fridge_id
        )
        .all()
    )

def get_fridge_meal_ingredient(db: Session, fridge_id: int, meal_id: int, ingredient_id: int):
    return (
        db.query(FridgeMealIngredient)
        .join(FridgeMeal)
        .filter(
            FridgeMealIngredient.id == ingredient_id,
            FridgeMeal.id == meal_id,
            FridgeMeal.fridge_id == fridge_id
        )
        .first()
    )

def update_fridge_meal_ingredient(db: Session, fridge_id: int, meal_id: int, ingredient_id: int, data: FridgeMealIngredientUpdate):
    get_fridge_object_or_404(db, FridgeMeal, fridge_id, meal_id)
    return update_by_id(db, FridgeMealIngredient, ingredient_id, data.model_dump(exclude_unset=True))

def delete_fridge_meal_ingredient(db: Session, fridge_id: int, meal_id: int, ingredient_id: int):
    get_fridge_object_or_404(db, FridgeMeal, fridge_id, meal_id)
    return delete_by_id(db, FridgeMealIngredient, ingredient_id)