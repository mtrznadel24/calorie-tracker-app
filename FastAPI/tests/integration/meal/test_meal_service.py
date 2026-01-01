from datetime import date

import pytest

from app.meal.models import MealType
from app.meal.schemas import (
    MealLogQuickCreate,
)


@pytest.mark.integration
class TestMealService:
    async def test_create_meal_log_success(self, meal_service, user):
        data = MealLogQuickCreate(
            date=date(2022, 1, 1),
            type=MealType.BREAKFAST,
            weight=80,
            name="meal_log_1",
            calories=150,
            proteins=15,
            fats=15,
            carbs=35,
        )
        result = await meal_service.create_meal_log_quick(user.id, data)
        assert result.user_id == user.id
        assert result.date == date(2022, 1, 1)
        assert result.type == MealType.BREAKFAST

    # TODO fix later
    # async def test_add_fridge_meal_to_meal_success(
    #     self,
    #     meal_service,
    #     user,
    #     fridge,
    #     fridge_product_factory,
    #     fridge_meal_factory,
    #     fridge_meal_ingredient_factory,
    # ):
    #     weight = WeightRequest(weight=50)
    #     fridge_meal = await fridge_meal_factory(meal_name="Meal1")
    #     fridge_products = [
    #         await fridge_product_factory(
    #             product_name=name,
    #             calories_100g=150,
    #             proteins_100g=25,
    #             fats_100g=10,
    #             carbs_100g=40,
    #             category=FoodCategory.FRUIT,
    #             is_favourite=False,
    #         )
    #         for name in ["Product1", "Product2", "Product3"]
    #     ]
    #     [
    #         await fridge_meal_ingredient_factory(fridge_meal, weight.weight, prod)
    #         for prod in fridge_products
    #     ]
    #
    #     result = await meal_service.add_fridge_meal_to_meal(
    #         user.id,
    #         fridge.id,
    #         fridge_meal.id,
    #         date(2022, 1, 1),
    #         MealType.BREAKFAST,
    #         weight=weight,
    #     )
    #     assert len(result) == 3
    #     assert set([ing.details.product_name for ing in result]) == {
    #         "Product1",
    #         "Product2",
    #         "Product3",
    #     }
    #     ingredient = result[0]
    #     assert ingredient.weight == 17
    #     meal = await meal_service.get_meal(
    #         user.id, date(2022, 1, 1), MealType.BREAKFAST
    #     )
    #     assert ingredient.meal_id == meal.id
