import contextlib
from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

Base = declarative_base()

class DBSessionManager:
    def __init__(self, host: str):
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    async def close(self):
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        async with self._engine.begin() as conn:
            try:
                yield conn
            except RuntimeError:
                await conn.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        session = self._sessionmaker()
        try:
            yield session
        except RuntimeError:
            await session.rollback()
            raise
        finally:
            await session.close()


session_manager = DBSessionManager(settings.DATABASE_URL)

async def get_db():
    async with session_manager.session() as session:
        yield session


DbSessionDep = Annotated[AsyncSession, Depends(get_db)]
