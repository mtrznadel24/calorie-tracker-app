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
    ingredient1 = MealIngredient(weight=50, meal_id=meal.id)
    ingredient1.details = MealIngredientDetails(
        product_name="Banana",
        calories_100g=89,
        proteins_100g=1,
        fats_100g=0.3,
        carbs_100g=23,
    )
    ingredient2 = MealIngredient(weight=100, meal_id=meal.id)
    ingredient2.details = MealIngredientDetails(
        product_name="product2",
        calories_100g=110,
        proteins_100g=20.5,
        fats_100g=6,
        carbs_100g=44,
    )
    ingredient3 = MealIngredient(weight=50, meal_id=meal.id)
    ingredient3.details = MealIngredientDetails(
        product_name="product3",
        calories_100g=100,
        proteins_100g=2,
        fats_100g=4,
        carbs_100g=28.2,
    )
    session.add_all([ingredient1, ingredient2, ingredient3])
    await session.commit()
    await session.refresh(meal, attribute_names=["ingredients"])
    return meal


async def create_meals_with_ingredients(meal_factory, ingredient_factory):
    meal1 = await meal_factory(date(2022, 1, 1), MealType.BREAKFAST)

    await ingredient_factory(meal1, 50, "Banana", 89, 1.1, 0.2, 23)
    await ingredient_factory(meal1, 100, "Chicken breast", 157, 32, 3.2, 0)
    await ingredient_factory(meal1, 200, "Rice", 130, 2.7, 0.2, 28)
    await ingredient_factory(meal1, 20, "Egg", 155, 13, 11, 1.1)

    meal2 = await meal_factory(date(2022, 1, 1), MealType.DINNER)

    await ingredient_factory(meal2, 100, "product1", 89, 1.1, 0.2, 23)
    await ingredient_factory(meal2, 200, "product2", 157, 32, 3.2, 0)
    await ingredient_factory(meal2, 400, "product3", 130, 2.7, 0.2, 28)
    await ingredient_factory(meal2, 40, "product4", 155, 13, 11, 1.1)