from app.models import *
from sqlalchemy.orm import Session
from app.schemas import *

def create_user(db: Session, data: UserCreate):
    # TODO: Add password hashing
    user_instance = User(**data.model_dump())
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance

def create_meal(db: Session, data: MealCreate):
    meal_instance = Meal(**data.model_dump())
    db.add(meal_instance)
    db.commit()
    db.refresh(meal_instance)
    return meal_instance

def create_fridge_product(data: FridgeProductCreate, db: Session):
    item_in = FridgeProduct(**data.model_dump())
    db.add(item_in)
    db.commit()
    db.refresh(item_in)
    return item_in

def get_fridge_products(db: Session):
    return db.query(FridgeProduct).all()

def get_fridge_product(product_id: int, db: Session):
    return db.query(FridgeProduct).filter(FridgeProduct.id == product_id).first()