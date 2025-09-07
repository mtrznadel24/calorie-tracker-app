from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.enums import FoodCategory

# Fridge
class FridgeRead(BaseModel):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

# Fridge meal
class FridgeMealCreate(BaseModel):
    user_id: int
    fridge_id: int
    name: str
    is_favourite: bool

class FridgeMealRead(BaseModel):
    id: int
    user_id: int
    fridge_id: int
    name: str
    is_favourite: bool

class FridgeMealUpdate(BaseModel):
    name: str | None = None
    is_favourite: bool | None = None

# Fridge meal ingredient
class FridgeMealIngredientCreate(BaseModel):
    weight: float
    fridge_meal_id: int
    fridge_product_id: int

class FridgeMealIngredientRead(BaseModel):
    id: int
    weight: float
    fridge_meal_id: int
    fridge_product_id: int

class FridgeMealIngredientUpdate(BaseModel):
    weight: float | None = None

# Fridge product
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

class FridgeProductUpdate(BaseModel):
    weight: float | None = None
    calories_100g: float | None = None
    proteins_100g: float | None = None
    fats_100g: float | None = None
    carbs_100g: float | None = None
    category: FoodCategory | None = None
    is_favourite: bool | None = None
