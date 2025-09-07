from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.enums import MealType
from datetime import datetime

# Meal
class MealCreate(BaseModel):
    user_id: int
    date: Optional[datetime] = None
    type: MealType

class MealRead(BaseModel):
    id: int
    user_id: int
    date: datetime
    type: MealType

    model_config = ConfigDict(from_attributes=True)

# Meal ingredient
class MealIngredientCreate(BaseModel):
    weight: float
    meal_id: int
    fridge_product_id: int

class MealIngredientRead(BaseModel):
    id: int
    weight: float
    meal_id: int
    fridge_product_id: int

    model_config = ConfigDict(from_attributes=True)

class MealIngredientUpdate(BaseModel):
    weight: float | None = None


