from typing import Type, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.core.exceptions import ConflictError, NotFoundError

T = TypeVar("T", bound=Base)


async def get_or_404(db: AsyncSession, model: Type[T], object_id: int) -> T:
    result = await db.execute(select(model).where(model.id == object_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise NotFoundError(f"{model.__name__} not found")
    return obj


async def create_instance(db: AsyncSession, model: Type[T], data: dict) -> T:
    obj = model(**data)
    db.add(obj)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictError(f"{model.__name__} already exists")
    except SQLAlchemyError:
        await db.rollback()
        raise
    await db.refresh(obj)
    return obj


async def update_by_id(
    db: AsyncSession, model: Type[T], object_id: int, data: dict
) -> T:
    obj = await get_or_404(db, model, object_id)

    for field, value in data.items():
        setattr(obj, field, value)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictError(f"{model.__name__} already exists")
    except SQLAlchemyError:
        await db.rollback()
        raise
    await db.refresh(obj)
    return obj


async def delete_by_id(db: AsyncSession, model: Type[T], object_id: int) -> T:
    obj = await get_or_404(db, model, object_id)
    await db.delete(obj)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictError(
            f"Cannot delete {model.__name__} because it is still referenced"
        )
    except SQLAlchemyError:
        await db.rollback()
        raise
    return obj
