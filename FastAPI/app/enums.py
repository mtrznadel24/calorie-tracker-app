import enum


class MealType(enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    SUPPER = "supper"

class FoodCategory(enum.Enum):
    FRUIT = "fruits"
    VEGETABLE = "vegetables"
    GRAINS = "grains"
    DAIRY = "dairy"
    MEAT_FISH = "meat and fish"
    PLANT_PROTEIN = "plant protein"
    FATS = "fats"
    DRINKS = "drinks"
    SNACKS = "snacks"

class NutrientType(enum.Enum):
    CALORIES = "calories_100g"
    PROTEINS = "proteins_100g"
    FATS = "fats_100g"
    CARBS = "carbs_100g"
