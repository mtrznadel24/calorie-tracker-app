from datetime import date

import pytest

from app.fridge.models import FoodCategory
from app.meal.models import MealType
from app.meal.schemas import (
    MealLogFromProductCreate,
    MealLogQuickCreate,
)


@pytest.mark.integration
class TestMealService:
    async def test_create_meal_log_quick_success(self, meal_service, user):
        data = MealLogQuickCreate(
            date=date(2022, 1, 1),
            type=MealType.BREAKFAST,
            weight=80,
            name="Manual Entry",
            calories=150,
            proteins=15,
            fats=15,
            carbs=35,
        )
        result = await meal_service.create_meal_log_quick(user.id, data)

        assert result.id is not None
        assert result.user_id == user.id
        assert result.name == "Manual Entry"
        assert result.calories == 150
        assert result.type == MealType.BREAKFAST

    async def test_create_meal_log_from_fridge_product_calculations(
        self, meal_service, user, fridge, fridge_product_factory
    ):
        product = await fridge_product_factory(
            product_name="Golden Apple",
            calories_100g=50,
            proteins_100g=1.5,
            fats_100g=0.5,
            carbs_100g=12.0,
            category=FoodCategory.FRUIT,
            is_favourite=False,
        )

        data = MealLogFromProductCreate(
            fridge_product_id=product.id,
            date=date(2022, 1, 1),
            type=MealType.SNACK,
            weight=200.0,  # 200g
        )

        result = await meal_service.create_meal_log_from_fridge_product(
            user.id, fridge.id, data
        )

        assert result.id is not None
        assert result.name == "Golden Apple"
        assert result.calories == 100.0
        assert result.proteins == 3.0
        assert result.carbs == 24.0

    async def test_create_meal_log_from_fridge_product_rounding(
        self, meal_service, user, fridge, fridge_product_factory
    ):
        with pytest.raises(AttributeError):
            await fridge_product_factory(
                product_name="Tricky Food",
                calories_100g=333,
                proteins_100g=33.3,
                fats_100g=10,
                carbs_100g=10,
                category=FoodCategory.OTHER,
                is_favourite=False,
            )
