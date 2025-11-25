import pytest

from app.core.exceptions import NotFoundError


@pytest.mark.integration
class TestMealIngredientRepository:

    async def test_get_meal_ingredients(
        self, meal_ingredient_repo, user, sample_meal, ingredient_factory
    ):
        ingredient1 = await ingredient_factory(
            sample_meal, 50, "Banana", 89, 1.1, 0.3, 23
        )
        ingredient2 = await ingredient_factory(
            sample_meal, 100, "Chicken breast", 157, 32, 3.2, 0
        )
        ingredient3 = await ingredient_factory(
            sample_meal, 200, "Rice", 130, 2.7, 0.3, 28
        )

        result = await meal_ingredient_repo.get_meal_ingredients(sample_meal.id)

        assert len(result) == 3
        assert result[0] == ingredient1
        assert result[1] == ingredient2
        assert result[2] == ingredient3

    async def test_get_meal_ingredients_wrong_meal_id(
        self, meal_ingredient_repo, user, sample_meal, ingredient_factory
    ):
        await ingredient_factory(sample_meal, 50, "Banana", 89, 1.1, 0.3, 23)
        await ingredient_factory(sample_meal, 100, "Chicken breast", 157, 32, 3.2, 0)
        await ingredient_factory(sample_meal, 200, "Rice", 130, 2.7, 0.3, 28)

        result = await meal_ingredient_repo.get_meal_ingredients(meal_id=999)

        assert result == []

    async def test_get_meal_ingredients_meal_no_ingredients(
        self, meal_ingredient_repo, user, sample_meal, ingredient_factory
    ):

        result = await meal_ingredient_repo.get_meal_ingredients(sample_meal.id)

        assert result == []

    async def test_get_meal_ingredient_by_id(
        self, meal_ingredient_repo, user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]

        result = await meal_ingredient_repo.get_meal_ingredient_by_id(
            sample_meal_with_ingredient.id, ingredient.id
        )

        assert result == ingredient

    async def test_get_meal_ingredient_by_id_wrong_meal_id(
        self, meal_ingredient_repo, user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]

        with pytest.raises(NotFoundError):
            await meal_ingredient_repo.get_meal_ingredient_by_id(999, ingredient.id)

    async def test_get_meal_ingredient_by_id_wrong_ingredient_id(
        self, meal_ingredient_repo, user, sample_meal_with_ingredient
    ):
        with pytest.raises(NotFoundError):
            await meal_ingredient_repo.get_meal_ingredient_by_id(
                sample_meal_with_ingredient.id, 999
            )
