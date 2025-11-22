from enum import Enum


class NutrientType(str, Enum):
    CALORIES = "calories"
    PROTEINS = "proteins"
    FATS = "fats"
    CARBS = "carbs"


nutrient_type_list = [
    NutrientType.CALORIES,
    NutrientType.PROTEINS,
    NutrientType.FATS,
    NutrientType.CARBS,
]
 