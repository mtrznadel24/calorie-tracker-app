import fakeredis
import pytest_asyncio

from app.auth.repositories import TokenRepository
from app.auth.services import AuthService


@pytest_asyncio.fixture
async def fake_redis():
    return fakeredis.aioredis.FakeRedis()


@pytest_asyncio.fixture
async def token_repo(fake_redis):
    return TokenRepository(fake_redis)  # type: ignore


@pytest_asyncio.fixture
async def auth_service(session, token_repo):
    return AuthService(session, token_repo)
