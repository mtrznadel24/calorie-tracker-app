from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.core.config import settings
from app.user.models import User
from redis.asyncio import Redis

class AuthRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)


    async def get_user_by_email(self, email) -> User:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()


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