from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError


async def get_or_404(db: AsyncSession, model, object_id: int):
    result = await db.execute(select(model).where(model.id == object_id))
    obj = result.scalars().first()
    if not obj:
        raise NotFoundError(f"{model.__name__} not found")
    return obj


async def create_instance(db: AsyncSession, model, data: dict):
    obj = model(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def update_by_id(db: AsyncSession, model, object_id: int, data: dict):
    obj = await get_or_404(db, model, object_id)

    for field, value in data.items():
        setattr(obj, field, value)

    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_by_id(db: AsyncSession, model, object_id: int):
    obj = await get_or_404(db, model, object_id)
    await db.delete(obj)
    await db.commit()
    return obj
