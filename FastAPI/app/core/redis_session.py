from typing import Annotated

import redis.asyncio as aioredis
from fastapi import Depends
from redis.asyncio import Redis

from app.core.config import settings

redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)


def get_redis_client() -> Redis:
    return redis_client


RedisDep = Annotated[Redis, Depends(get_redis_client)]


async def close_redis_session():
    await redis_client.connection_pool.disconnect()
