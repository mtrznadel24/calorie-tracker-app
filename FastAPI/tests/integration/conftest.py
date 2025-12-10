import logging
import os
import pathlib

import fakeredis.aioredis
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession

from app import models  # noqa: F401
from app.auth.dependencies import get_current_user
from app.core.db import Base, DBSessionManager, get_db
from app.core.redis_session import get_redis_client
from app.core.security import get_hashed_password
from app.fridge.dependencies import get_fridge
from app.fridge.models import (
    FoodCategory,
    Fridge,
    FridgeMeal,
    FridgeMealIngredient,
    FridgeProduct,
)
from app.main import get_app
from app.user.models import User

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env.test")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL is not set in .env.test")

test_session_manager = DBSessionManager(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    echo=False,
)


@pytest.fixture(autouse=True, scope="session")
def configure_logs():
    logging.basicConfig(level=logging.CRITICAL)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    # CREATE TABLES
    async with test_session_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # DROP TABLES
    async with test_session_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_session_manager.close()


@pytest_asyncio.fixture
async def session():
    async with test_session_manager.connect() as conn:
        trans = await conn.begin()

        async_session = AsyncSession(bind=conn, expire_on_commit=False)

        try:
            yield async_session
        finally:
            await async_session.close()
            if trans.is_active:
                await trans.rollback()


@pytest_asyncio.fixture
async def fake_redis():
    return fakeredis.aioredis.FakeRedis(decode_responses=True)


@pytest_asyncio.fixture
async def user(session):
    hashed_password = get_hashed_password("password1")
    u = User(
        username="testuser", email="test@example.com", hashed_password=hashed_password
    )
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u


@pytest_asyncio.fixture
async def other_user(session):
    hashed_password = get_hashed_password("password2")
    u = User(
        username="testuser2", email="test2@example.com", hashed_password=hashed_password
    )
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u


@pytest_asyncio.fixture
async def client(session, user):
    async def override_get_db():
        yield session

    async def override_get_current_user():
        return user

    app = get_app()
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client_with_redis(session, user, fake_redis):
    async def override_get_db():
        yield session

    async def override_get_redis_client():
        yield fake_redis

    async def override_get_current_user():
        return user

    app = get_app()
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_redis_client] = override_get_redis_client

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client_no_user(session, user):
    async def override_get_db():
        yield session

    app = get_app()
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def fridge(session, user):
    fridge = Fridge(user_id=user.id)
    session.add(fridge)
    await session.commit()
    await session.refresh(fridge)
    return fridge


@pytest_asyncio.fixture
async def client_with_fridge(session, user, fridge):
    async def override_get_db():
        yield session

    async def override_get_current_user():
        return user

    async def override_get_fridge():
        return fridge

    app = get_app()
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_fridge] = override_get_fridge

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client

    app.dependency_overrides.clear()


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
