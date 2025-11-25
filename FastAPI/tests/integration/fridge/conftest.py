import pytest_asyncio

from app.fridge.models import (
    FoodCategory,
    Fridge,
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
def fridge_meal_factory(session, fridge):
    async def factory(meal_name):
        meal = FridgeMeal(fridge_id=fridge.id, name=meal_name, is_favourite=False)

        session.add(meal)
        await session.commit()
        await session.refresh(meal)
        return meal

    return factory


@pytest_asyncio.fixture
def fridge_meal_ingredient_factory(session, fridge):
    async def factory(meal, weight, product):
        ingredient = FridgeMealIngredient(
            fridge_meal_id=meal.id, weight=weight, fridge_product_id=product.id
        )
        session.add(ingredient)
        await session.commit()
        await session.refresh(ingredient)
        return ingredient

    return factory


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
