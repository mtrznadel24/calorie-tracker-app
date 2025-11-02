import redis.asyncio as aioredis
from app.core.config import settings

redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

async def add_refresh_token_to_redis(jti: str, user_id: int):
    ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
    await redis_client.set(f"refresh:{jti}", user_id, ex=ttl)

async def is_refresh_token_valid(jti: str) -> bool:
    return await redis_client.exists(f"refresh:{jti}") == 1

async def delete_refresh_token_from_redis(jti: str):
    await redis_client.delete(f"refresh:{jti}")

async def close_redis_session():
    await redis_client.close()