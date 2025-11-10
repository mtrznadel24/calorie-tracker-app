from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ConflictError
from app.measurements.models import Measurement, Weight
from app.measurements.schemas import MeasurementsCreate, WeightCreate
from app.utils.crud_user_scoped import (
    create_user_object_or_404,
    delete_user_obj_or_404,
    get_user_obj_or_404,
)


async def create_measurements(
    db: AsyncSession, user_id: int, data: MeasurementsCreate
) -> Measurement:
    weight_in = None
    if data.weight is not None:
        weight_in = await create_weight(
            db, user_id, data.weight
        )  # NOTE Weight is commited immediately, will be fixed with repositories

    obj = Measurement(
        user_id=user_id,
        date=data.date,
        weight_id=weight_in.id if weight_in else None,
        neck=data.neck,
        biceps=data.biceps,
        chest=data.chest,
        waist=data.waist,
        hips=data.hips,
        thighs=data.thighs,
        calves=data.calves,
    )
    db.add(obj)
    try:
        await db.commit()
    except IntegrityError:
        raise ConflictError(f"Measurements with date:{data.date} already exists")
    except SQLAlchemyError:
        await db.rollback()
        raise
    await db.refresh(obj)
    return obj


async def get_measurements(
    db: AsyncSession, user_id: int, measurement_id: int
) -> Measurement:
    return await get_user_obj_or_404(db, user_id, Measurement, measurement_id)


async def get_latest_measurements(db: AsyncSession, user_id: int) -> Measurement:
    result = await db.execute(
        select(Measurement)
        .where(Measurement.user_id == user_id)
        .order_by(Measurement.date.desc())
    )
    return result.scalars().first()


async def get_previous_measurements(db: AsyncSession, user_id: int) -> Measurement:
    result = await db.execute(
        select(Measurement)
        .where(Measurement.user_id == user_id)
        .order_by(Measurement.date.desc())
        .offset(1)
        .limit(1)
    )
    return result.scalars().first()


async def get_measurements_list(
    db: AsyncSession, user_id: int, offset: int = 0, limit: int = 10
):
    result = await db.execute(
        select(Measurement)
        .options(selectinload(Measurement.weight_rel))
        .where(Measurement.user_id == user_id)
        .order_by(Measurement.date.desc())
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def delete_measurements(
    db: AsyncSession, user_id: int, measurements_id: int
) -> Measurement:
    return await delete_user_obj_or_404(db, user_id, Measurement, measurements_id)


async def create_weight(db: AsyncSession, user_id: int, data: WeightCreate) -> Weight:
    result = await db.execute(
        select(Weight).where(Weight.user_id == user_id, Weight.date == data.date)
    )
    weight = result.scalar_one_or_none()
    if weight is None:
        weight = await create_user_object_or_404(db, user_id, Weight, data.model_dump())
    else:
        setattr(weight, "weight", data.weight)
        try:
            await db.commit()
        except SQLAlchemyError:
            await db.rollback()
            raise
        await db.refresh(weight)
    return weight
    # TODO: improve exception messages for constraint violations (unique date, FK errors, etc.)


async def get_current_weight(db: AsyncSession, user_id: int) -> Weight | None:
    result = await db.execute(
        select(Weight).where(Weight.user_id == user_id).order_by(Weight.date.desc())
    )
    return result.scalars().first()


async def get_previous_weight(db: AsyncSession, user_id: int) -> Weight | None:
    result = await db.execute(
        select(Weight)
        .where(Weight.user_id == user_id)
        .order_by(Weight.date.desc())
        .offset(1)
        .limit(1)
    )
    return result.scalars().first()


async def get_user_weight(
    db: AsyncSession, user_id: int, weight_id: int
) -> Weight | None:
    return await get_user_obj_or_404(db, user_id, Weight, weight_id)


async def get_user_weights(
    db: AsyncSession, user_id: int, offset: int = 0, limit: int = 10
) -> Sequence[Weight | None]:
    result = await db.execute(
        select(Weight)
        .where(Weight.user_id == user_id)
        .order_by(Weight.date.desc())
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def delete_weight(db: AsyncSession, user_id: int, weight_id: int) -> Weight:
    return await delete_user_obj_or_404(db, user_id, Weight, weight_id)
