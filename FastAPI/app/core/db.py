import contextlib
from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


class DBSessionManager:
    def __init__(self, host: str, **kwargs):
        self._engine = create_async_engine(host, **kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

    async def close(self):
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """Połączenie BEZ automatycznej transakcji - dla testów"""
        async with self._engine.connect() as conn:
            try:
                yield conn
            except Exception:
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @property
    def engine(self):
        return self._engine


session_manager = DBSessionManager(settings.DATABASE_URL)


async def get_db():
    async with session_manager.session() as session:
        yield session


DbSessionDep = Annotated[AsyncSession, Depends(get_db)]
