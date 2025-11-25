import asyncio
import uuid
from unittest.mock import AsyncMock

import pytest

from app.auth.repositories import TokenRepository


@pytest.mark.integration
class TestTokenRepository:

    async def test_is_refresh_token_valid_true(self):
        redis = AsyncMock()
        redis.exists.return_value = 1
        repo = TokenRepository(redis)

        assert await repo.is_refresh_token_valid("abc123") is True

    async def test_is_refresh_token_valid_false(self):
        redis = AsyncMock()
        redis.exists.return_value = 0
        repo = TokenRepository(redis)

        assert await repo.is_refresh_token_valid("abc123") is False

    async def test_add_refresh_token_to_redis(self, token_repo, user):
        jti = str(uuid.uuid4())
        await token_repo.add_refresh_token_to_redis(jti, user.id)
        assert await token_repo.is_refresh_token_valid(jti) is True

    async def test_token_expires_after_ttl(self, fake_redis, token_repo, user):
        jti = str(uuid.uuid4())

        await token_repo.add_refresh_token_to_redis(jti, user.id)
        await fake_redis.expire(f"refresh:{jti}", 1)

        await asyncio.sleep(1.1)
        assert await token_repo.is_refresh_token_valid(jti) is False

    async def test_delete_refresh_token_from_redis(self, token_repo, user):
        jti = str(uuid.uuid4())
        await token_repo.add_refresh_token_to_redis(jti, user.id)
        await token_repo.delete_refresh_token_from_redis(jti)
        assert await token_repo.is_refresh_token_valid(jti) is False
