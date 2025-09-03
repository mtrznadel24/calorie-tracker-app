from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.models import MealType, FoodCategory
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    height: Optional[float] = None

class UserRead(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    height: float | None = None

class MealCreate(BaseModel):
    user_id: int
    fridge_meal_id: Optional[int] = None
    date: Optional[datetime] = None
    type: MealType

class MealRead(BaseModel):
    id: int
    user_id: int
    fridge_meal_id: Optional[int] = None
    date: datetime
    type: MealType

    model_config = ConfigDict(from_attributes=True)

class MealUpdate(BaseModel):
    fridge_meal_id: Optional[int] = None

class FridgeProductCreate(BaseModel):
    product_name: str
    calories_100g: float
    proteins_100g: float
    fats_100g: float
    carbs_100g: float
    category: FoodCategory
    is_favourite: bool = False

class FridgeProductRead(BaseModel):
    id: int
    product_name: str
    calories_100g: float
    proteins_100g: float
    fats_100g: float
    carbs_100g: float
    category: FoodCategory
    is_favourite: bool = False

    model_config = ConfigDict(from_attributes=True)