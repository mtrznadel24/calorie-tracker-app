import os
import pathlib

import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession

from app import models  # noqa: F401
from app.auth.dependencies import get_current_user
from app.core.db import Base, DBSessionManager, DbSessionDep, get_db
from app.core.security import get_hashed_password
from app.user.models import User
from app.main import get_app

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env.test")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

test_session_manager = DBSessionManager(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    echo=False,
)


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

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client_no_user(session, user):
    async def override_get_db():
        yield session


    app = get_app()
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()
