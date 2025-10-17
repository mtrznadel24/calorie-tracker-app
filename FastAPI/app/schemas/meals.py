from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.meals import MealType


# Meal
class MealCreate(BaseModel):
    date: Optional[date] = None
    type: MealType


class MealRead(BaseModel):
    id: int
    user_id: int
    date: date
    type: MealType

    model_config = ConfigDict(from_attributes=True)


# Meal Ingredient Details


class MealIngredientProductCreate(BaseModel):
    product_name: str
    calories_100g: float
    proteins_100g: float
    fats_100g: float
    carbs_100g: float


class MealIngredientProductRead(BaseModel):
    id: int
    product_name: str
    calories_100g: float
    proteins_100g: float
    fats_100g: float
    carbs_100g: float

    model_config = ConfigDict(from_attributes=True)


class MealIngredientProductUpdate(BaseModel):
    product_name: str | None = None
    calories_100g: float | None = None
    proteins_100g: float | None = None
    fats_100g: float | None = None
    carbs_100g: float | None = None


# Meal ingredient


class MealIngredientCreate(BaseModel):
    weight: float
    details: MealIngredientProductCreate


class MealIngredientRead(BaseModel):
    id: int
    weight: float
    details: MealIngredientProductRead

    model_config = ConfigDict(from_attributes=True)


class MealIngredientUpdate(BaseModel):
    weight: float | None = None
    details: MealIngredientProductUpdate | None = None
