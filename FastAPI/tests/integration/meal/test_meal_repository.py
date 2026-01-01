from datetime import date

import pytest

from app.meal.models import MealType


@pytest.mark.integration
class TestMealRepository:
    async def test_get_meal_logs_success(self, user, meal_repo, meal_log_factory):
        await meal_log_factory(
            type=MealType.BREAKFAST,
            weight=80,
            name="meal_log_1",
            calories=150,
            proteins=15,
            fats=15,
            carbs=35,
        )
        await meal_log_factory(
            type=MealType.DINNER,
            weight=80,
            name="meal_log_2",
            calories=150,
            proteins=15,
            fats=15,
            carbs=35,
        )
        await meal_log_factory(
            type=MealType.BREAKFAST,
            weight=80,
            name="meal_log_3",
            calories=150,
            proteins=15,
            fats=15,
            carbs=35,
        )

        result = await meal_repo.get_meal_logs(user.id, date(2022, 1, 1))
        assert len(result) == 3
        assert result[0].name == "meal_log_1"
        assert result[1].name == "meal_log_2"
        assert result[2].name == "meal_log_3"
