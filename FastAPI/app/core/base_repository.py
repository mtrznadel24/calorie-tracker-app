
from typing import TypeVar, Type, Generic

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model

    async def commit(self) -> None:
        await self.db.commit()

    async def rollback(self) -> None:
        await self.db.rollback()

    async def flush(self) -> None:
        await self.db.flush()

    async def refresh_and_return(self, instance: T) -> T:
        await self.db.refresh(instance)
        return instance

    def add(self, instance: T):
        self.db.add(instance)

    async def commit_or_conflict(self) -> None:
        try:
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()
            raise e
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_by_id(self, object_id: int) -> T:
        result = await self.db.execute(select(self.model).where(self.model.id == object_id))
        return result.scalar_one_or_none()
