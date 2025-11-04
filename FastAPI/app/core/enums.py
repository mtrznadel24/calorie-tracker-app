from enum import Enum


class NutrientType(str, Enum):
    CALORIES = "calories"
    PROTEINS = "proteins"
    FATS = "fats"
    CARBS = "carbs"
