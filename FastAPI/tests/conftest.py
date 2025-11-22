import os
import pathlib

import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import DBSessionManager, Base
from app import models  # noqa: F401
from app.user.models import User



BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env.test")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

test_session_manager = DBSessionManager(TEST_DATABASE_URL,
                                        poolclass=NullPool,
                                        echo=False,
                                        )


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    # CREATE tables
    async with test_session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # DROP tables
    async with test_session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_session_manager.close()


@pytest_asyncio.fixture
async def session():
    async with test_session_manager.connect() as conn:
        async_session = AsyncSession(bind=conn, expire_on_commit=False)
        try:
            yield async_session
        finally:
            await async_session.rollback()
            await async_session.close()


@pytest_asyncio.fixture
async def user(session):
    u = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hash_password"
    )
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u
