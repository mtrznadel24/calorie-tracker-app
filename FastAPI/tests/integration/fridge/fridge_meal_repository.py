import pytest

from app.core.exceptions import NotFoundError
from app.utils.enums import NutrientType


@pytest.mark.integration
class TestFridgeMealRepository:
    async def test_get_fridge_meal_list_no_meals(self, fridge_meal_repo, fridge):
        result = await fridge_meal_repo.get_fridge_meal_list(fridge.id, False, 0, 10)
        assert result == []

    async def test_get_fridge_meal_list_one_meal(
        self, fridge_meal_repo, fridge, fridge_meal_factory
    ):
        meal = await fridge_meal_factory("toast")

        result = await fridge_meal_repo.get_fridge_meal_list(fridge.id, False, 0, 10)
        assert result != []
        assert result[0] == meal

    async def test_get_fridge_meal_list_many_meals(
        self, fridge_meal_repo, fridge, fridge_meal_factory
    ):
        meals = [
            await fridge_meal_factory(name) for name in ["meal1", "meal2", "meal3"]
        ]

        result = await fridge_meal_repo.get_fridge_meal_list(fridge.id, False, 0, 10)
        assert result == meals

    async def test_get_fridge_meal_list_is_favourite(
        self, fridge_meal_repo, session, fridge, fridge_meal_factory
    ):
        meals = [
            await fridge_meal_factory(name)
            for name in ["meal1", "meal2", "meal3", "meal4"]
        ]
        meals[0].is_favourite = True
        meals[2].is_favourite = True
        await session.commit()

        result = await fridge_meal_repo.get_fridge_meal_list(fridge.id, True, 0, 10)
        assert len(result) == 2
        assert result[0] == meals[0]
        assert result[1] == meals[2]

    async def test_get_fridge_meal_success(
        self, fridge_meal_repo, fridge, sample_fridge_meal
    ):
        result = await fridge_meal_repo.get_fridge_meal(
            fridge.id, sample_fridge_meal.id
        )
        assert result == sample_fridge_meal

    async def test_get_fridge_meal_wrong_meal_id(self, fridge_meal_repo, fridge):
        with pytest.raises(NotFoundError):
            await fridge_meal_repo.get_fridge_meal(fridge.id, 999)

    async def test_delete_fridge_meal_success(
        self, fridge_meal_repo, fridge, sample_fridge_meal
    ):
        await fridge_meal_repo.delete_fridge_meal(fridge.id, sample_fridge_meal.id)

        with pytest.raises(NotFoundError):
            await fridge_meal_repo.get_fridge_meal(fridge.id, sample_fridge_meal.id)

    async def test_delete_fridge_meal_wrong_meal(self, fridge_meal_repo, fridge):
        with pytest.raises(NotFoundError):
            await fridge_meal_repo.delete_fridge_meal(fridge.id, 999)

    async def test_get_fridge_meal_nutrient_sum_wrong_meal_id(
        self, fridge_meal_repo, fridge
    ):
        result = await fridge_meal_repo.get_fridge_meal_nutrient_sum(
            fridge.id, 999, NutrientType.CALORIES
        )
        assert result == 0.0

    async def test_get_fridge_meal_nutrient_sum_no_ingredients(
        self, fridge_meal_repo, fridge, sample_fridge_meal
    ):
        result = await fridge_meal_repo.get_fridge_meal_nutrient_sum(
            fridge.id, sample_fridge_meal.id, NutrientType.CALORIES
        )
        assert result == 0.0

    async def test_get_fridge_meal_nutrient_sum_many_ingredients(
        self, fridge_meal_repo, fridge, sample_fridge_meal_with_ingredients
    ):
        result = await fridge_meal_repo.get_fridge_meal_nutrient_sum(
            fridge.id, sample_fridge_meal_with_ingredients.id, NutrientType.CALORIES
        )
        assert result == 50 * 100 / 100 + 50 * 100 / 100 + 50 * 100 / 100

    async def test_get_fridge_meal_macro_wrong_meal_id(self, fridge_meal_repo, fridge):
        result = await fridge_meal_repo.get_fridge_meal_macro(fridge.id, 999)
        assert result == {"calories": 0.0, "proteins": 0.0, "fats": 0.0, "carbs": 0.0}

    async def test_get_fridge_meal_macro_no_ingredients(
        self, fridge_meal_repo, fridge, sample_fridge_meal
    ):
        result = await fridge_meal_repo.get_fridge_meal_macro(
            fridge.id, sample_fridge_meal.id
        )
        assert result == {"calories": 0.0, "proteins": 0.0, "fats": 0.0, "carbs": 0.0}

    async def test_get_fridge_meal_macro_many_ingredients(
        self, fridge_meal_repo, fridge, sample_fridge_meal_with_ingredients
    ):
        result = await fridge_meal_repo.get_fridge_meal_macro(
            fridge.id, sample_fridge_meal_with_ingredients.id
        )
        assert result == {
            "calories": 150.0,
            "proteins": 15.0,
            "fats": 7.5,
            "carbs": 30.0,
        }

    async def test_get_fridge_meal_weight_success(
        self, fridge_meal_repo, fridge, sample_fridge_meal_with_ingredients
    ):
        result = await fridge_meal_repo.get_fridge_meal_weight(
            fridge.id, sample_fridge_meal_with_ingredients.id
        )
        assert result == 150

    async def test_get_fridge_meal_weight_no_ingredients(
        self, fridge_meal_repo, fridge, sample_fridge_meal
    ):
        result = await fridge_meal_repo.get_fridge_meal_weight(
            fridge.id, sample_fridge_meal.id
        )
        assert result == 0.0

    async def test_add_meal_ingredient(
        self,
        fridge_meal_repo,
        fridge,
        fridge_meal_ingredient_factory,
        sample_fridge_meal,
        sample_fridge_product,
    ):
        ingredient = await fridge_meal_ingredient_factory(
            sample_fridge_meal, 50, sample_fridge_product
        )
        await fridge_meal_repo.add_meal_ingredient(ingredient)
        expected = await fridge_meal_repo.get_fridge_meal_ingredient(
            fridge.id, sample_fridge_meal.id, ingredient.id
        )
        assert ingredient == expected

    async def test_get_fridge_meal_ingredients_wrong_meal_id(
        self, fridge_meal_repo, fridge
    ):
        result = await fridge_meal_repo.get_fridge_meal_ingredients(fridge.id, 999)
        assert result == []

    async def test_get_fridge_meal_ingredients_no_ingredients(
        self, fridge_meal_repo, fridge, sample_fridge_meal
    ):
        result = await fridge_meal_repo.get_fridge_meal_ingredients(
            fridge.id, sample_fridge_meal.id
        )
        assert result == []

    async def test_get_fridge_meal_ingredients_many_ingredients(
        self, fridge_meal_repo, fridge, sample_fridge_meal_with_ingredients
    ):
        ingredients = sample_fridge_meal_with_ingredients.ingredients
        result = await fridge_meal_repo.get_fridge_meal_ingredients(
            fridge.id, sample_fridge_meal_with_ingredients.id
        )
        assert len(result) == 3
        assert result == ingredients

    async def test_get_fridge_meal_ingredient_wrong_ingredient_id(
        self,
        fridge_meal_repo,
        fridge,
        sample_fridge_meal,
        sample_fridge_product,
        fridge_meal_ingredient_factory,
    ):
        ingredient = await fridge_meal_ingredient_factory(
            sample_fridge_meal, 50, sample_fridge_product
        )
        await fridge_meal_repo.add_meal_ingredient(ingredient)

        with pytest.raises(NotFoundError):
            await fridge_meal_repo.get_fridge_meal_ingredient(
                fridge.id, sample_fridge_meal.id, 999
            )

    async def test_get_fridge_meal_ingredient_success(
        self,
        fridge_meal_repo,
        fridge,
        sample_fridge_meal,
        sample_fridge_product,
        fridge_meal_ingredient_factory,
    ):
        ingredient = await fridge_meal_ingredient_factory(
            sample_fridge_meal, 50, sample_fridge_product
        )
        await fridge_meal_repo.add_meal_ingredient(ingredient)
        result = await fridge_meal_repo.get_fridge_meal_ingredient(
            fridge.id, sample_fridge_meal.id, ingredient.id
        )
        assert result == ingredient

    async def test_delete_ingredient_wrong_ingredient_id(
        self,
        fridge_meal_repo,
        fridge,
        sample_fridge_meal,
        sample_fridge_product,
        fridge_meal_ingredient_factory,
    ):
        ingredient = await fridge_meal_ingredient_factory(
            sample_fridge_meal, 50, sample_fridge_product
        )
        await fridge_meal_repo.add_meal_ingredient(ingredient)

        with pytest.raises(NotFoundError):
            await fridge_meal_repo.delete_ingredient(
                fridge.id, sample_fridge_meal.id, 999
            )

    async def test_delete_ingredient_success(
        self,
        fridge_meal_repo,
        fridge,
        sample_fridge_meal,
        sample_fridge_product,
        fridge_meal_ingredient_factory,
    ):
        ingredient = await fridge_meal_ingredient_factory(
            sample_fridge_meal, 50, sample_fridge_product
        )
        await fridge_meal_repo.add_meal_ingredient(ingredient)
        await fridge_meal_repo.delete_ingredient(
            fridge.id, sample_fridge_meal.id, ingredient.id
        )

        with pytest.raises(NotFoundError):
            await fridge_meal_repo.get_fridge_meal_ingredient(
                fridge.id, sample_fridge_meal.id, ingredient.id
            )
