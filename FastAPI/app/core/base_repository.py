from typing import Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.core.exceptions import ConflictError, NotFoundError

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
        result = await self.db.execute(
            select(self.model).where(self.model.id == object_id)
        )
        obj = result.scalar_one_or_none()
        if obj is None:
            raise NotFoundError(f"{self.model.__name__} not found")
        return obj

    async def delete_by_id(self, object_id: int) -> T:
        obj = await self.get_by_id(object_id)
        await self.db.delete(obj)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise ConflictError(f"Could not delete {self.model.__name__}")
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return obj


class UserScopedRepository(BaseRepository[T]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        super().__init__(db, model)
        if not hasattr(model, "user_id"):
            raise ValueError(f"{model.__name__} does not have a user_id column")

    async def get_by_id_for_user(self, user_id: int, object_id: int) -> T:
        result = await self.db.execute(
            select(self.model).where(
                self.model.user_id == user_id, self.model.id == object_id
            )
        )
        obj = result.scalar_one_or_none()
        if obj is None:
            raise NotFoundError(f"{self.model.__name__} not found")
        return obj

    async def delete_by_id_for_user(self, user_id: int, object_id: int) -> T:
        obj = await self.get_by_id_for_user(user_id, object_id)
        await self.db.delete(obj)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise ConflictError(f"Could not delete {self.model.__name__}")
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return obj
