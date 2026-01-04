from datetime import date

import pytest_asyncio

from app.fridge.models import FoodCategory, Fridge, FridgeMeal, FridgeProduct
from app.meal.models import MealLog, MealType
from app.meal.repositories import MealRepository
from app.meal.services import MealService


@pytest_asyncio.fixture
async def meal_repo(session):
    return MealRepository(session)


@pytest_asyncio.fixture
async def meal_service(session):
    return MealService(session)


@pytest_asyncio.fixture
def meal_log_factory(session, user):
    async def factory(weight, type, name, calories, proteins, fats, carbs):
        log = MealLog(
            user_id=user.id,
            date=date(2022, 1, 1),
            type=type,
            weight=weight,
            name=name,
            calories=calories,
            proteins=proteins,
            fats=fats,
            carbs=carbs,
        )
        session.add(log)
        await session.commit()
        await session.refresh(log)
        return log

    return factory


@pytest_asyncio.fixture
async def sample_meal_log(session, user):
    log = MealLog(
        user_id=user.id,
        date=date(2022, 1, 1),
        type=MealType.BREAKFAST,
        weight=80,
        name="meal_log_1",
        calories=150,
        proteins=15,
        fats=15,
        carbs=35,
    )
    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log


@pytest_asyncio.fixture
async def fridge(session, user):
    fridge = Fridge(user_id=user.id)
    session.add(fridge)
    await session.commit()
    await session.refresh(fridge)
    return fridge


@pytest_asyncio.fixture
def fridge_product_factory(session, fridge):
    async def factory(
        product_name,
        calories_100g,
        proteins_100g,
        fats_100g,
        carbs_100g,
        category: FoodCategory,
        is_favourite: bool,
    ):
        product = FridgeProduct(
            fridge_id=fridge.id,
            product_name=product_name,
            calories_100g=calories_100g,
            proteins_100g=proteins_100g,
            fats_100g=fats_100g,
            carbs_100g=carbs_100g,
            category=category,
            is_favourite=is_favourite,
        )
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

    return factory


@pytest_asyncio.fixture
def fridge_meal_factory(session, fridge):
    async def factory(meal_name):
        meal = FridgeMeal(fridge_id=fridge.id, name=meal_name, is_favourite=False)

        session.add(meal)
        await session.commit()
        await session.refresh(meal)
        return meal

    return factory
