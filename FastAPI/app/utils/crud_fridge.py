from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.fridge import Fridge
from app.utils.crud import get_or_404


async def get_fridge_object_or_404(db: AsyncSession, model, fridge_id: int, object_id: int):
    result = await db.execute(select(model)
                           .where(model.id == object_id, model.fridge_id == fridge_id))
    obj = result.scalars().first()
    if not obj:
        raise NotFoundError(f"{model.__name__} not found")
    return obj


async def create_fridge_instance(db: AsyncSession, model, fridge_id: int, data: dict):
    await get_or_404(
        db, Fridge, fridge_id
    )  # If fridge does not exist, it will raise an exception
    obj = model(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def update_fridge_object(
    db: AsyncSession, model, fridge_id: int, object_id: int, data: dict
):
    obj = await get_fridge_object_or_404(db, model, fridge_id, object_id)

    for field, value in data.items():
        setattr(obj, field, value)

    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_fridge_object(db: AsyncSession, model, fridge_id: int, object_id: int):
    obj = await get_fridge_object_or_404(db, model, fridge_id, object_id)
    await db.delete(obj)
    await db.commit()
    return obj
