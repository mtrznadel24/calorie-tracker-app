from datetime import date

import pytest

from app.meal.models import MealType
from app.utils.enums import NutrientType
from tests.integration.meal.conftest import create_meals_with_ingredients


@pytest.mark.integration
class TestMealRepository:
    async def test_get_meal_by_date_and_type_valid(self, meal_repo, user, sample_meal):
        result = await meal_repo.get_meal_by_date_and_type(
            user.id, date(2022, 1, 1), MealType.BREAKFAST
        )
        assert result is not None
        assert result.user_id == user.id
        assert result.date == date(2022, 1, 1)
        assert result.type == MealType.BREAKFAST

    async def test_get_meal_by_date_and_type_wrong_date(
        self, meal_repo, user, sample_meal
    ):
        result = await meal_repo.get_meal_by_date_and_type(
            user.id, date(2022, 1, 2), MealType.BREAKFAST
        )
        assert result is None

    async def test_get_meal_by_date_and_type_wrong_meal_type(
        self, meal_repo, user, sample_meal
    ):
        result = await meal_repo.get_meal_by_date_and_type(
            user.id, date(2022, 1, 1), MealType.DINNER
        )
        assert result is None

    async def test_get_meal_by_date_and_type_wrong_user(
        self, meal_repo, user, sample_meal
    ):
        result = await meal_repo.get_meal_by_date_and_type(
            2, date(2022, 1, 1), MealType.BREAKFAST
        )
        assert result is None

    async def test_meal_nutrient_sum_no_ingredients(self, meal_repo, user, sample_meal):
        result = await meal_repo.get_meal_nutrient_sum(
            user.id, sample_meal.id, NutrientType.CALORIES
        )
        assert result is not None
        assert result == 0.0

    async def test_meal_nutrient_sum_one_ingredient(
        self, meal_repo, user, sample_meal_with_ingredient
    ):
        result = await meal_repo.get_meal_nutrient_sum(
            user.id, sample_meal_with_ingredient.id, NutrientType.CALORIES
        )
        assert result is not None
        assert result == 44.5

    async def test_meal_nutrient_sum_with_many_ingredients(
        self, meal_repo, user, sample_meal, ingredient_factory
    ):
        await ingredient_factory(sample_meal, 50, "Banana", 89, 1.1, 0.3, 23)
        await ingredient_factory(sample_meal, 100, "Chicken breast", 157, 32, 3.2, 0)
        await ingredient_factory(sample_meal, 200, "Rice", 130, 2.7, 0.3, 28)
        await ingredient_factory(sample_meal, 20, "Egg", 155, 13, 11, 1.1)

        result = await meal_repo.get_meal_nutrient_sum(
            user.id, sample_meal.id, NutrientType.CALORIES
        )
        assert result == 44.5 + 157 + 260 + 31

    async def test_get_meal_macro_no_ingredients(self, meal_repo, user, sample_meal):
        result = await meal_repo.get_meal_macro(user.id, sample_meal.id)
        assert result == {"calories": 0.0, "proteins": 0.0, "fats": 0.0, "carbs": 0.0}

    async def test_get_meal_macro_with_ingredient(
        self, meal_repo, user, sample_meal_with_ingredient
    ):
        result = await meal_repo.get_meal_macro(user.id, sample_meal_with_ingredient.id)
        assert result == {
            "calories": 44.5,
            "proteins": 0.55,
            "fats": 0.15,
            "carbs": 11.5,
        }

    async def test_get_meal_macro_with_many_ingredients(
        self, meal_repo, user, sample_meal, ingredient_factory
    ):
        await ingredient_factory(sample_meal, 50, "Banana", 89, 1.1, 0.3, 23)
        await ingredient_factory(sample_meal, 100, "Chicken breast", 157, 32, 3.2, 0)
        await ingredient_factory(sample_meal, 200, "Rice", 130, 2.7, 0.3, 28)
        await ingredient_factory(sample_meal, 20, "Egg", 155, 13, 11, 1.1)

        result = await meal_repo.get_meal_macro(user.id, sample_meal.id)
        assert result == {
            "calories": (50 * 89 + 100 * 157 + 200 * 130 + 20 * 155) / 100,
            "proteins": (50 * 1.1 + 100 * 32 + 200 * 2.7 + 20 * 13) / 100,
            "fats": (50 * 0.3 + 100 * 3.2 + 200 * 0.3 + 20 * 11) / 100,
            "carbs": (50 * 23 + 100 * 0 + 200 * 28 + 20 * 1.1) / 100,
        }

    async def test_get_meals_nutrient_sum_for_day_no_meals(self, meal_repo, user):
        result = await meal_repo.get_meals_nutrient_sum_for_day(
            user.id, date(2022, 1, 1), NutrientType.CALORIES
        )
        assert result == 0.0

    async def test_get_meals_nutrient_sum_for_day_one_meal(
        self, meal_repo, user, meal_factory, ingredient_factory
    ):
        meal1 = await meal_factory(date(2022, 1, 1), MealType.BREAKFAST)

        await ingredient_factory(meal1, 50, "Banana", 89, 1.1, 0.3, 23)
        await ingredient_factory(meal1, 100, "Chicken breast", 157, 32, 3.2, 0)
        await ingredient_factory(meal1, 200, "Rice", 130, 2.7, 0.3, 28)
        await ingredient_factory(meal1, 20, "Egg", 155, 13, 11, 1.1)

        result = await meal_repo.get_meals_nutrient_sum_for_day(
            user.id, date(2022, 1, 1), NutrientType.CALORIES
        )
        expected = (50 * 89 + 100 * 157 + 200 * 130 + 20 * 155) / 100
        assert result == expected

    async def test_get_meals_nutrient_sum_for_day_many_meals(
        self, meal_repo, user, meal_factory, ingredient_factory
    ):
        await create_meals_with_ingredients(meal_factory, ingredient_factory)

        result = await meal_repo.get_meals_nutrient_sum_for_day(
            user.id, date(2022, 1, 1), NutrientType.CALORIES
        )
        expected = (
            (50 * 89 + 100 * 157 + 200 * 130 + 20 * 155)
            + (100 * 89 + 200 * 157 + 400 * 130 + 40 * 155)
        ) / 100
        assert result == expected

    async def test_get_macro_for_a_day_no_meals(self, meal_repo, user):
        result = await meal_repo.get_macro_for_day(user.id, date(2022, 1, 1))
        assert result == {"calories": 0.0, "proteins": 0.0, "fats": 0.0, "carbs": 0.0}

    async def test_get_macro_for_a_day_many_meals(
        self, meal_repo, user, meal_factory, ingredient_factory
    ):
        await create_meals_with_ingredients(meal_factory, ingredient_factory)

        result = await meal_repo.get_macro_for_day(user.id, date(2022, 1, 1))

        expected = {
            "calories": round(
                (
                    (50 * 89 + 100 * 157 + 200 * 130 + 20 * 155)
                    + (100 * 89 + 200 * 157 + 400 * 130 + 40 * 155)
                )
                / 100,
                1,
            ),
            "proteins": round(
                (
                    (50 * 1.1 + 100 * 32 + 200 * 2.7 + 20 * 13)
                    + (100 * 1.1 + 200 * 32 + 400 * 2.7 + 40 * 13)
                )
                / 100,
                1,
            ),
            "fats": round(
                (
                    (50 * 0.2 + 100 * 3.2 + 200 * 0.2 + 20 * 11)
                    + (100 * 0.2 + 200 * 3.2 + 400 * 0.2 + 40 * 11)
                )
                / 100,
                1,
            ),
            "carbs": round(
                (
                    (50 * 23 + 100 * 0 + 200 * 28 + 20 * 1.1)
                    + (100 * 23 + 200 * 0 + 400 * 28 + 40 * 1.1)
                )
                / 100,
                1,
            ),
        }

        assert result == expected
