import pytest_asyncio

from app.fridge.models import (
    FoodCategory,
    FridgeMeal,
    FridgeMealIngredient,
    FridgeProduct,
)
from app.fridge.repositories import FridgeMealRepository, FridgeProductRepository
from app.fridge.services import FridgeService


@pytest_asyncio.fixture
async def fridge_meal_repo(session):
    return FridgeMealRepository(session)


@pytest_asyncio.fixture
async def fridge_product_repo(session):
    return FridgeProductRepository(session)


@pytest_asyncio.fixture
async def fridge_service(session):
    return FridgeService(session)


@pytest_asyncio.fixture
async def sample_fridge_product(session, fridge):
    product = FridgeProduct(
        fridge_id=fridge.id,
        product_name="Banana",
        calories_100g=89,
        proteins_100g=1.1,
        fats_100g=0.3,
        carbs_100g=23,
        category=FoodCategory.FRUIT,
        is_favourite=False,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@pytest_asyncio.fixture
async def sample_fridge_meal(session, fridge):
    meal = FridgeMeal(fridge_id=fridge.id, name="toast", is_favourite=False)

    session.add(meal)
    await session.commit()
    await session.refresh(meal)
    return meal


@pytest_asyncio.fixture
async def sample_fridge_meal_with_ingredient(session, fridge, sample_fridge_product):
    meal = FridgeMeal(fridge_id=fridge.id, name="toast", is_favourite=False)
    session.add(meal)
    await session.flush()
    ingredient = FridgeMealIngredient(
        weight=50, fridge_meal_id=meal.id, fridge_product_id=sample_fridge_product.id
    )

    session.add(ingredient)
    await session.commit()
    await session.refresh(meal, attribute_names=["ingredients"])
    return meal


@pytest_asyncio.fixture
async def sample_fridge_meal_with_ingredients(session, fridge):
    meal = FridgeMeal(
        fridge_id=fridge.id,
        name="meal1",
        is_favourite=False,
    )
    session.add(meal)
    await session.flush()

    products = []
    for name in ["product1", "product2", "product3"]:
        product = FridgeProduct(
            fridge_id=fridge.id,
            product_name=name,
            calories_100g=100,
            proteins_100g=10,
            fats_100g=5,
            carbs_100g=20,
            category=FoodCategory.FRUIT,
            is_favourite=False,
        )
        session.add(product)
        products.append(product)
    await session.flush()

    ingredients = [
        FridgeMealIngredient(weight=50, fridge_meal_id=meal.id, fridge_product_id=p.id)
        for p in products
    ]
    session.add_all(ingredients)

    await session.commit()
    await session.refresh(meal, attribute_names=["ingredients"])
    return meal
