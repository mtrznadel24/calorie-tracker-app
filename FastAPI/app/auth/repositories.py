from redis.asyncio import Redis

from app.core.config import settings


class TokenRepository:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600

    async def add_refresh_token_to_redis(self, jti: str, user_id: int):
        ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
        await self.redis.set(f"refresh:{jti}", user_id, ex=ttl)

    async def is_refresh_token_valid(self, jti: str) -> bool:
        return await self.redis.exists(f"refresh:{jti}") == 1

    async def delete_refresh_token_from_redis(self, jti: str):
        await self.redis.delete(f"refresh:{jti}")
