from datetime import date

import pytest_asyncio

from app.meal.models import Meal, MealIngredient, MealIngredientDetails, MealType
from app.meal.repositories import MealIngredientRepository, MealRepository
from app.meal.services import MealService


@pytest_asyncio.fixture
async def meal_repo(session):
    return MealRepository(session)


@pytest_asyncio.fixture
async def meal_ingredient_repo(session):
    return MealIngredientRepository(session)


@pytest_asyncio.fixture
async def meal_service(session):
    return MealService(session)


@pytest_asyncio.fixture
def meal_factory(session, user):
    async def factory(meal_date, meal_type):
        meal = Meal(user_id=user.id, date=meal_date, type=meal_type)
        session.add(meal)
        await session.commit()
        await session.refresh(meal)
        return meal

    return factory


@pytest_asyncio.fixture
def ingredient_factory(session):
    async def factory(
        meal, weight, product_name, calories_100g, proteins_100g, fats_100g, carbs_100g
    ):
        ingredient = MealIngredient(weight=weight, meal_id=meal.id)
        ingredient.details = MealIngredientDetails(
            product_name=product_name,
            calories_100g=calories_100g,
            proteins_100g=proteins_100g,
            fats_100g=fats_100g,
            carbs_100g=carbs_100g,
        )
        session.add(ingredient)
        await session.commit()
        await session.refresh(ingredient)
        return ingredient

    return factory


@pytest_asyncio.fixture
async def sample_meal(session, user):
    meal = Meal(user_id=user.id, date=date(2022, 1, 1), type=MealType.BREAKFAST)
    session.add(meal)
    await session.commit()
    await session.refresh(meal)
    return meal


@pytest_asyncio.fixture
async def sample_meal_with_ingredient(session, user):
    meal = Meal(user_id=user.id, date=date(2022, 1, 1), type=MealType.BREAKFAST)
    session.add(meal)
    await session.flush()
    ingredient = MealIngredient(weight=50, meal_id=meal.id)
    ingredient.details = MealIngredientDetails(
        product_name="Banana",
        calories_100g=89,
        proteins_100g=1.1,
        fats_100g=0.3,
        carbs_100g=23,
    )
    session.add(ingredient)
    await session.commit()
    await session.refresh(meal, attribute_names=["ingredients"])
    return meal


@pytest_asyncio.fixture
async def sample_meal_with_ingredients(session, user):
    meal = Meal(user_id=user.id, date=date(2022, 1, 1), type=MealType.BREAKFAST)
    session.add(meal)
    await session.flush()
    ingredient = MealIngredient(weight=50, meal_id=meal.id)
    ingredient.details = MealIngredientDetails(
        product_name="Banana",
        calories_100g=89,
        proteins_100g=1.1,
        fats_100g=0.3,
        carbs_100g=23,
    )
    session.add(ingredient)
    await session.commit()
    await session.refresh(meal)
    return meal
