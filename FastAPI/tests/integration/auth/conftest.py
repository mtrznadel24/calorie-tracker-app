import fakeredis.aioredis
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.auth.repositories import TokenRepository
from app.auth.services import AuthService
from app.core.db import get_db
from app.core.redis_session import get_redis_client
from app.core.security import create_refresh_token, get_token_payload
from app.main import get_app


@pytest_asyncio.fixture
async def fake_redis():
    return fakeredis.aioredis.FakeRedis()


@pytest_asyncio.fixture
async def token_repo(fake_redis):
    return TokenRepository(fake_redis)  # type: ignore


@pytest_asyncio.fixture
async def auth_service(session, token_repo):
    return AuthService(session, token_repo)

@pytest_asyncio.fixture
async def client_with_redis(session, user, fake_redis):
    async def override_get_db():
        yield session

    async def override_get_redis_client():
        yield fake_redis

    app = get_app()
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis_client] = override_get_redis_client

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()

@pytest_asyncio.fixture
def test_refresh_token():
    username = "testuser"
    user_id = 1
    token, jti = create_refresh_token(username, user_id)
    return token

@pytest_asyncio.fixture
async def client_with_refresh_token(session, fake_redis, test_refresh_token):
    async def override_get_db():
        yield session

    async def override_get_redis_client():
        yield fake_redis

    app = get_app()
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis_client] = override_get_redis_client

    payload = get_token_payload(test_refresh_token)
    jti = payload["jti"]
    user_id = payload["id"]
    await fake_redis.set(f"refresh:{jti}", user_id)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        cookies={"refresh_token": test_refresh_token}
    ) as client:
        yield client

    app.dependency_overrides.clear()