import datetime as dt

from pydantic import BaseModel, ConfigDict, Field

from app.meal.models import MealType


# Meal
class MealLogCreateBase(BaseModel):
    date: dt.date
    type: MealType
    weight: float


class MealLogQuickCreate(MealLogCreateBase):
    name: str
    calories: float = Field(default=0, ge=0)
    proteins: float = Field(default=0, ge=0)
    fats: float = Field(default=0, ge=0)
    carbs: float = Field(default=0, ge=0)


class MealLogFromProductCreate(MealLogCreateBase):
    fridge_product_id: int


class MealLogFromMealCreate(MealLogCreateBase):
    fridge_meal_id: int


class MealLogRead(BaseModel):
    id: int
    name: str
    type: MealType
    weight: float
    calories: float
    proteins: float
    fats: float
    carbs: float

    model_config = ConfigDict(from_attributes=True)


class MealLogUpdate(BaseModel):
    name: str
    weight: float


# Others


class WeightRequest(BaseModel):
    weight: float = Field(gt=0)
