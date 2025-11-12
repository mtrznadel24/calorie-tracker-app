from collections.abc import Sequence
from typing import Type, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.core.exceptions import ConflictError, NotFoundError

T = TypeVar("T", bound=Base)

#TODO delete after MealRepository Implementation
async def get_user_obj_or_404(
    db: AsyncSession, user_id: int, model: Type[T], object_id: int
) -> T:
    if not hasattr(model, "user_id"):
        raise ValueError(f"{model.__name__} does not have a user_id column")
    result = await db.execute(
        select(model).where(model.id == object_id, model.user_id == user_id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise NotFoundError(f"{model.__name__} not found")
    return obj


async def get_user_objects_or_404(
    db: AsyncSession, user_id: int, model: Type[T]
) -> Sequence[T]:
    if not hasattr(model, "user_id"):
        raise ValueError(f"{model.__name__} does not have a user_id column")
    result = await db.execute(select(model).where(model.user_id == user_id))
    objects = result.scalars().all()
    if not objects:
        raise NotFoundError(f"{model.__name__} not found")
    return objects


async def create_user_object_or_404(
    db: AsyncSession, user_id: int, model: Type[T], data: dict
) -> T:
    if not hasattr(model, "user_id"):
        raise ValueError(f"{model.__name__} does not have a user_id column")
    obj = model(**data, user_id=user_id)
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


async def update_user_obj_or_404(
    db: AsyncSession, user_id: int, model: Type[T], object_id: int, data: dict
) -> T:

    obj = await get_user_obj_or_404(db, user_id, model, object_id)

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


async def delete_user_obj_or_404(
    db: AsyncSession, user_id: int, model: Type[T], object_id: int
) -> T:

    obj = await get_user_obj_or_404(db, user_id, model, object_id)

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
