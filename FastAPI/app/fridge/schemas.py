from pydantic import BaseModel, ConfigDict, Field

from app.fridge.models import FoodCategory


# Fridge product
class FridgeProductCreate(BaseModel):
    product_name: str = Field(pattern=r"^[a-zA-Z0-9\s\-.]+$")
    calories_100g: float = Field(default=None, gt=0)
    proteins_100g: float = Field(default=None, gt=0)
    fats_100g: float = Field(default=None, gt=0)
    carbs_100g: float = Field(default=None, gt=0)
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
    product_name: str | None = Field(default=None, pattern=r"^[a-zA-Z0-9\s\-.]+$")
    calories_100g: float | None = Field(default=None, gt=0)
    proteins_100g: float | None = Field(default=None, gt=0)
    fats_100g: float | None = Field(default=None, gt=0)
    carbs_100g: float | None = Field(default=None, gt=0)
    category: FoodCategory | None = None
    is_favourite: bool | None = None


# Fridge meal ingredient
class FridgeMealIngredientCreate(BaseModel):
    weight: float = Field(gt=0)
    fridge_product_id: int


class FridgeMealIngredientSimpleRead(BaseModel):
    id: int
    weight: float
    fridge_product_id: int

    model_config = ConfigDict(from_attributes=True)


class FridgeMealIngredientRead(BaseModel):
    id: int
    weight: float
    fridge_product_id: int
    product_name: str
    calories: float

    model_config = ConfigDict(from_attributes=True)


class FridgeMealIngredientUpdate(BaseModel):
    weight: float | None = Field(gt=0)


# Fridge meal
class FridgeMealCreate(BaseModel):
    name: str = Field(pattern=r"^[a-zA-Z0-9\s\-.]+$")
    is_favourite: bool = False


class FridgeMealWithIngredientsCreate(BaseModel):
    name: str = Field(pattern=r"^[a-zA-Z0-9\s\-.]+$")
    is_favourite: bool = False
    ingredients: list[FridgeMealIngredientCreate]


class FridgeMealSimpleRead(BaseModel):
    id: int
    name: str = Field(pattern=r"^[a-zA-Z0-9\s\-.]+$")


class FridgeMealRead(BaseModel):
    id: int
    name: str = Field(pattern=r"^[a-zA-Z0-9\s\-.]+$")
    is_favourite: bool = False
    calories: float
    proteins: float
    fats: float
    carbs: float
    products_count: int
    weight: int

    model_config = ConfigDict(from_attributes=True)


class FridgeMealUpdate(BaseModel):
    name: str | None = Field(default=None, pattern=r"^[a-zA-Z0-9\s\-.]+$")
    is_favourite: bool | None = None
