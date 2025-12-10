import logging

from fastapi import HTTPException, Request
from fastapi_limiter.depends import RateLimiter
from redis.asyncio import Redis

from app.core.config import settings

logger = logging.getLogger(__name__)


async def check_and_record_login_attempt(
    username: str, redis: Redis, max_attempts: int = 5, window_seconds: int = 600
):
    key = f"login_attempt:{username}"

    try:
        current = await redis.get(key)

        if current and int(current) >= max_attempts:
            ttl = await redis.ttl(key)
            minutes = max(1, ttl // 60)
            raise HTTPException(
                status_code=429,
                detail=f"Too many attempts. Retry in {minutes} minutes.",
            )
        attempts = await redis.incr(key)

        if attempts == 1:
            await redis.expire(key, window_seconds)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Redis error in rate limiting for {username}: {e}")


async def clear_login_attempts(
    username: str,
    redis: Redis,
):
    key = f"login_attempt:{username}"
    try:
        await redis.delete(key)
    except Exception as e:
        logger.warning(f"Failed to clear login attempts for {username}: {e}")


def rate_limiter(times: int, seconds: int):
    if settings.ENVIRONMENT == "test":

        class MockLimiter:
            async def __call__(self, request: Request):
                return 0

        return MockLimiter()
    return RateLimiter(times=times, seconds=seconds)
