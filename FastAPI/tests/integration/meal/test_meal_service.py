from datetime import date

import pytest

from app.core.exceptions import NotFoundError
from app.fridge.models import FoodCategory
from app.meal.models import MealIngredient, MealType
from app.meal.schemas import (
    MealCreate,
    MealIngredientCreate,
    MealIngredientProductCreate,
    MealIngredientProductUpdate,
    MealIngredientUpdate,
    WeightRequest,
)


@pytest.mark.integration
class TestMealCreate:
    async def test_create_meal_success(self, meal_service, user):
        data = MealCreate(date=date(2022, 1, 1), type=MealType.BREAKFAST)
        result = await meal_service.create_meal(user.id, data)
        assert result.user_id == user.id
        assert result.date == date(2022, 1, 1)
        assert result.type == MealType.BREAKFAST

    async def test_create_meal_already_exists(self, meal_service, user, sample_meal):
        data = MealCreate(date=date(2022, 1, 1), type=MealType.BREAKFAST)
        result = await meal_service.create_meal(user.id, data)
        assert result.user_id == user.id
        assert result.date == date(2022, 1, 1)
        assert result.type == MealType.BREAKFAST

    async def test_get_or_create_meal_meal_exists(
        self, meal_service, user, sample_meal
    ):
        result = await meal_service.get_or_create_meal(
            user.id, sample_meal.date, sample_meal.type
        )
        assert result.user_id == user.id
        assert result.id == sample_meal.id
        assert result.date == sample_meal.date
        assert result.type == sample_meal.type

    async def test_get_or_create_meal_meal_not_exists(self, meal_service, user):
        result = await meal_service.get_or_create_meal(
            user.id, date(2022, 1, 1), MealType.BREAKFAST
        )
        assert result.user_id == user.id
        assert result.date == date(2022, 1, 1)
        assert result.type == MealType.BREAKFAST

    async def test_add_ingredient_to_meal_success_meal_exists(
        self, meal_service, user, sample_meal
    ):
        data_details = MealIngredientProductCreate(
            product_name="product1",
            calories_100g=100,
            proteins_100g=20,
            fats_100g=5,
            carbs_100g=15,
        )
        data = MealIngredientCreate(weight=50, details=data_details)

        result = await meal_service.add_ingredient_to_meal(
            user.id, sample_meal.date, sample_meal.type, data
        )
        details = result.details

        assert result.weight == 50
        assert details.calories_100g == 100
        assert details.proteins_100g == 20
        assert details.fats_100g == 5
        assert details.carbs_100g == 15

    async def test_add_ingredient_to_meal_success_meal_not_exists(
        self, meal_service, user
    ):
        data_details = MealIngredientProductCreate(
            product_name="product1",
            calories_100g=100,
            proteins_100g=20,
            fats_100g=5,
            carbs_100g=15,
        )
        data = MealIngredientCreate(weight=50, details=data_details)

        result = await meal_service.add_ingredient_to_meal(
            user.id, date(2022, 1, 1), MealType.BREAKFAST, data
        )
        details = result.details

        assert result.weight == 50
        assert details.calories_100g == 100
        assert details.proteins_100g == 20
        assert details.fats_100g == 5
        assert details.carbs_100g == 15

    async def test_get_meal_ingredients_success(
        self, meal_service, user, sample_meal_with_ingredients
    ):
        ingredients = sample_meal_with_ingredients.ingredients
        result = await meal_service.get_meal_ingredients(
            user.id, sample_meal_with_ingredients.id
        )
        assert result == ingredients

    async def test_get_meal_ingredients_wrong_user(
        self, meal_service, user, sample_meal_with_ingredients
    ):
        ingredients = sample_meal_with_ingredients.ingredients
        result = await meal_service.get_meal_ingredients(
            user.id, sample_meal_with_ingredients.id
        )
        assert result == ingredients

    async def test_get_meal_ingredients_wrong_meal_id(
        self, meal_service, user, sample_meal_with_ingredients
    ):
        ingredients = sample_meal_with_ingredients.ingredients
        result = await meal_service.get_meal_ingredients(
            user.id, sample_meal_with_ingredients.id
        )
        assert result == ingredients

    async def test_get_meal_ingredient_by_id_success(
        self, meal_service, user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        result = await meal_service.get_meal_ingredient_by_id(
            user.id, sample_meal_with_ingredient.id, ingredient.id
        )
        assert result == ingredient

    async def test_get_meal_ingredient_by_id_wrong_user(
        self, meal_service, other_user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        with pytest.raises(NotFoundError):
            await meal_service.get_meal_ingredient_by_id(
                other_user.id, sample_meal_with_ingredient.id, ingredient.id
            )

    async def test_get_meal_ingredient_by_id_wrong_meal_id(
        self, meal_service, user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        with pytest.raises(NotFoundError):
            await meal_service.get_meal_ingredient_by_id(user.id, 999, ingredient.id)

    async def test_get_meal_ingredient_by_id_wrong_ingredient_id(
        self, meal_service, user, sample_meal_with_ingredient
    ):
        sample_meal_with_ingredient.ingredients[0]
        with pytest.raises(NotFoundError):
            await meal_service.get_meal_ingredient_by_id(
                user.id, sample_meal_with_ingredient.id, 999
            )

    async def test_update_meal_ingredient_update_weight(
        self, meal_service, user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        data_details = MealIngredientProductUpdate()
        data = MealIngredientUpdate(weight=75, details=data_details)

        result = await meal_service.update_meal_ingredient(
            user.id, sample_meal_with_ingredient.id, ingredient.id, data
        )
        assert result.weight == 75
        assert result.details == ingredient.details

    async def test_update_meal_ingredient_update_details(
        self, meal_service, user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        data_details = MealIngredientProductUpdate(
            product_name="Product1",
            calories_100g=150,
            proteins_100g=100,
            fats_100g=25,
            carbs_100g=40,
        )
        data = MealIngredientUpdate(weight=None, details=data_details)

        result = await meal_service.update_meal_ingredient(
            user.id, sample_meal_with_ingredient.id, ingredient.id, data
        )
        assert result.weight == ingredient.weight
        assert result.details.product_name == "Product1"
        assert result.details.calories_100g == 150
        assert result.details.proteins_100g == 100
        assert result.details.fats_100g == 25
        assert result.details.carbs_100g == 40

    async def test_update_meal_ingredient_failed(
        self, meal_service, user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        data_details = MealIngredientProductUpdate(
            product_name="Product1",
            calories_100g=150,
            proteins_100g=100,
            fats_100g=25,
            carbs_100g=40,
        )
        data = MealIngredientUpdate(weight=None, details=data_details)

        result = await meal_service.update_meal_ingredient(
            user.id, sample_meal_with_ingredient.id, ingredient.id, data
        )
        assert result.weight == ingredient.weight
        assert result.details.product_name == "Product1"
        assert result.details.calories_100g == 150
        assert result.details.proteins_100g == 100
        assert result.details.fats_100g == 25
        assert result.details.carbs_100g == 40

    async def test_delete_meal_ingredient_success(
        self, meal_service, user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        result = await meal_service.delete_meal_ingredient(
            user.id, sample_meal_with_ingredient.id, ingredient.id
        )
        assert result.id == ingredient.id

    async def test_delete_meal_ingredient_wrong_user(
        self, meal_service, other_user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        with pytest.raises(NotFoundError):
            await meal_service.delete_meal_ingredient(
                other_user.id, sample_meal_with_ingredient.id, ingredient.id
            )

    async def test_get_ingredient_details_success(
        self, meal_service, user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        result = await meal_service.get_ingredient_details(
            user.id, sample_meal_with_ingredient.id, ingredient.id
        )
        assert result.product_name == ingredient.details.product_name
        assert result.calories_100g == ingredient.details.calories_100g

    async def test_get_ingredient_details_wrong_user(
        self, meal_service, other_user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        with pytest.raises(NotFoundError):
            await meal_service.get_ingredient_details(
                other_user.id, sample_meal_with_ingredient.id, ingredient.id
            )

    async def test_get_ingredient_details_wrong_meal_id(
        self, meal_service, user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        with pytest.raises(NotFoundError):
            await meal_service.get_ingredient_details(user.id, 9999, ingredient.id)

    async def test_get_ingredient_details_wrong_ingredient_id(
        self, meal_service, user, sample_meal_with_ingredient
    ):
        with pytest.raises(NotFoundError):
            await meal_service.get_ingredient_details(
                user.id, sample_meal_with_ingredient.id, 9999
            )

    async def test_get_ingredient_details_no_details(
        self, meal_service, session, user, sample_meal
    ):
        ingredient = MealIngredient(weight=10, meal_id=sample_meal.id)
        session.add(ingredient)
        await session.commit()
        await session.refresh(ingredient)

        result = await meal_service.get_ingredient_details(
            user.id, sample_meal.id, ingredient.id
        )
        assert result is None

    async def test_add_fridge_product_to_meal_success(
        self, meal_service, user, fridge, fridge_product_factory
    ):
        product = await fridge_product_factory(
            product_name="Product1",
            calories_100g=150,
            proteins_100g=25,
            fats_100g=10,
            carbs_100g=40,
            category=FoodCategory.FRUIT,
            is_favourite=False,
        )
        weight = WeightRequest(weight=50)
        result = await meal_service.add_fridge_product_to_meal(
            user.id,
            fridge.id,
            product.id,
            date(2022, 1, 1),
            MealType.BREAKFAST,
            weight=weight,
        )
        assert result.weight == weight.weight

        details = result.details
        assert details.product_name == product.product_name
        assert details.calories_100g == product.calories_100g

        meal = await meal_service.get_meal(
            user.id, date(2022, 1, 1), MealType.BREAKFAST
        )
        assert result.meal_id == meal.id

    async def test_add_fridge_meal_to_meal_success(
        self,
        meal_service,
        user,
        fridge,
        fridge_product_factory,
        fridge_meal_factory,
        fridge_meal_ingredient_factory,
    ):
        weight = WeightRequest(weight=50)
        fridge_meal = await fridge_meal_factory(meal_name="Meal1")
        fridge_products = [
            await fridge_product_factory(
                product_name=name,
                calories_100g=150,
                proteins_100g=25,
                fats_100g=10,
                carbs_100g=40,
                category=FoodCategory.FRUIT,
                is_favourite=False,
            )
            for name in ["Product1", "Product2", "Product3"]
        ]
        [
            await fridge_meal_ingredient_factory(fridge_meal, weight.weight, prod)
            for prod in fridge_products
        ]

        result = await meal_service.add_fridge_meal_to_meal(
            user.id,
            fridge.id,
            fridge_meal.id,
            date(2022, 1, 1),
            MealType.BREAKFAST,
            weight=weight,
        )
        assert len(result) == 3
        assert set([ing.details.product_name for ing in result]) == {
            "Product1",
            "Product2",
            "Product3",
        }
        ingredient = result[0]
        assert ingredient.weight == 17
        meal = await meal_service.get_meal(
            user.id, date(2022, 1, 1), MealType.BREAKFAST
        )
        assert ingredient.meal_id == meal.id
