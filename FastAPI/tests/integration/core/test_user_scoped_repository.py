from datetime import date

import pytest

from app.core.exceptions import NotFoundError
from app.meal.models import Meal, MealType
from app.meal.repositories import MealRepository


@pytest.mark.integration
class TestUserScopeRepository:
    async def test_get_by_id_for_user(self, session, user):
        repo = MealRepository(session)
        meal = Meal(user_id=user.id, date=date(2022, 1, 1), type=MealType.BREAKFAST)
        session.add(meal)
        await session.commit()
        await session.refresh(meal)
        result = await repo.get_by_id_for_user(user.id, meal.id)

        assert result == meal

    async def test_get_by_id_for_user_wrong_user(self, session, user):
        repo = MealRepository(session)
        meal = Meal(user_id=user.id, date=date(2022, 1, 1), type=MealType.BREAKFAST)
        session.add(meal)
        await session.commit()
        await session.refresh(meal)

        with pytest.raises(NotFoundError):
            await repo.get_by_id_for_user(999, meal.id)

    async def test_get_by_id_for_user_wrong_meal_id(self, session, user):
        repo = MealRepository(session)
        meal = Meal(user_id=user.id, date=date(2022, 1, 1), type=MealType.BREAKFAST)
        session.add(meal)
        await session.commit()
        await session.refresh(meal)

        with pytest.raises(NotFoundError):
            await repo.get_by_id_for_user(user.id, 999)

    async def test_delete_by_id_for_user_success(self, session, user):
        repo = MealRepository(session)
        meal = Meal(user_id=user.id, date=date(2022, 1, 1), type=MealType.BREAKFAST)
        session.add(meal)
        await session.commit()
        await session.refresh(meal)

        await repo.delete_by_id_for_user(user.id, meal.id)

        with pytest.raises(NotFoundError):
            await repo.get_by_id_for_user(user.id, meal.id)

    async def test_delete_by_id_for_user_wrong_user(self, session, user):
        repo = MealRepository(session)
        meal = Meal(user_id=user.id, date=date(2022, 1, 1), type=MealType.BREAKFAST)
        session.add(meal)
        await session.commit()
        await session.refresh(meal)

        with pytest.raises(NotFoundError):
            await repo.delete_by_id_for_user(999, meal.id)

    async def test_delete_by_id_for_user_wrong_meal_id(self, session, user):
        repo = MealRepository(session)
        meal = Meal(user_id=user.id, date=date(2022, 1, 1), type=MealType.BREAKFAST)
        session.add(meal)
        await session.commit()
        await session.refresh(meal)

        with pytest.raises(NotFoundError):
            await repo.delete_by_id_for_user(user.id, 999)
