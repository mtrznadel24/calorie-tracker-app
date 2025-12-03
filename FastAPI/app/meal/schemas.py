import datetime as dt

from pydantic import BaseModel, ConfigDict, Field

from app.meal.models import MealType


# Meal
class MealCreate(BaseModel):
    date: dt.date
    type: MealType


class MealRead(BaseModel):
    id: int
    user_id: int
    date: dt.date
    type: MealType

    model_config = ConfigDict(from_attributes=True)


# Meal Ingredient Details


class MealIngredientProductCreate(BaseModel):
    product_name: str = Field(pattern=r"^[a-zA-Z0-9\s\-.]+$")
    calories_100g: float = Field(gt=0)
    proteins_100g: float = Field(gt=0)
    fats_100g: float = Field(gt=0)
    carbs_100g: float = Field(gt=0)


class MealIngredientProductRead(BaseModel):
    id: int
    product_name: str
    calories_100g: float
    proteins_100g: float
    fats_100g: float
    carbs_100g: float

    model_config = ConfigDict(from_attributes=True)


class MealIngredientProductUpdate(BaseModel):
    product_name: str | None = Field(default=None, pattern=r"^[a-zA-Z0-9\s\-.]+$")
    calories_100g: float | None = Field(default=None, gt=0)
    proteins_100g: float | None = Field(default=None, gt=0)
    fats_100g: float | None = Field(default=None, gt=0)
    carbs_100g: float | None = Field(default=None, gt=0)


# Meal ingredient


class MealIngredientCreate(BaseModel):
    weight: float = Field(gt=0)
    details: MealIngredientProductCreate


class MealIngredientRead(BaseModel):
    id: int
    weight: float
    details: MealIngredientProductRead

    model_config = ConfigDict(from_attributes=True)


class MealIngredientUpdate(BaseModel):
    weight: float | None = None
    details: MealIngredientProductUpdate | None = None


# Others


class WeightRequest(BaseModel):
    weight: float = Field(gt=0)
