import pytest

from app.meal.repositories import MealIngredientRepository


@pytest.mark.integration
class TestMealIngredientRepository:

    async def test_get_meal_ingredients(self, session, user, sample_meal, ingredient_factory):
        repo = MealIngredientRepository(session)

        ingredient1 = await ingredient_factory(sample_meal, 50, "Banana", 89, 1.1, 0.3, 23)
        ingredient2 = await ingredient_factory(sample_meal, 100, "Chicken breast", 157, 32, 3.2, 0)
        ingredient3 = await ingredient_factory(sample_meal, 200, "Rice", 130, 2.7, 0.3, 28)

        result = await repo.get_meal_ingredients(sample_meal.id)

        assert len(result) == 3
        assert result[0] == ingredient1
        assert result[1] == ingredient2
        assert result[2] == ingredient3

    async def test_get_meal_ingredients_wrong_meal_id(self, session, user, sample_meal, ingredient_factory):
        repo = MealIngredientRepository(session)

        ingredient1 = await ingredient_factory(sample_meal, 50, "Banana", 89, 1.1, 0.3, 23)
        ingredient2 = await ingredient_factory(sample_meal, 100, "Chicken breast", 157, 32, 3.2, 0)
        ingredient3 = await ingredient_factory(sample_meal, 200, "Rice", 130, 2.7, 0.3, 28)

        result = await repo.get_meal_ingredients(meal_id=999)

        assert result == []

    async def test_get_meal_ingredients_meal_no_ingredients(self, session, user, sample_meal, ingredient_factory):
        repo = MealIngredientRepository(session)

        result = await repo.get_meal_ingredients(sample_meal.id)

        assert result == []

    async def test_get_meal_ingredient_by_id(self, session, user, sample_meal_with_ingredient):
        repo = MealIngredientRepository(session)
        ingredient = sample_meal_with_ingredient.ingredients[0]

        result = await repo.get_meal_ingredient_by_id(sample_meal_with_ingredient.id,
                                                      ingredient.id)

        assert result == ingredient

    async def test_get_meal_ingredient_by_id_wrong_meal_id(self, session, user, sample_meal_with_ingredient):
        repo = MealIngredientRepository(session)
        ingredient = sample_meal_with_ingredient.ingredients[0]

        result = await repo.get_meal_ingredient_by_id(999, ingredient.id)

        assert result is None

    async def test_get_meal_ingredient_by_id_wrong_ingredient_id(self, session, user, sample_meal_with_ingredient):
        repo = MealIngredientRepository(session)

        result = await repo.get_meal_ingredient_by_id(sample_meal_with_ingredient.id,999)

        assert result is None

