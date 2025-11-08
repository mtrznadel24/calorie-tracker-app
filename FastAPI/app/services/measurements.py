from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.models import User, Weight, Measurement
from app.schemas.measurements import MeasurementsCreate, WeightCreate, MeasurementsRead
from app.utils.crud import get_or_404, delete_by_id, create_instance
from app.utils.crud_user import delete_user_obj_or_404, get_user_obj_or_404, get_user_objects_or_404


async def create_measurements(db: AsyncSession, user_id: int, data: MeasurementsCreate, weight_data: WeightCreate):
    weight_in = None
    if weight_data.weight is not None:
        weight_in = Weight(user_id=user_id, date=data.date, weight=weight_data.weight)
        db.add(weight_in)
        await db.flush()

    obj = Measurement(user_id=user_id,
                      date=data.date,
                      weight_id=weight_in.id if weight_in else None,
                      neck=data.neck,
                      biceps=data.biceps,
                      chest=data.chest,
                      waist=data.waist,
                      hips=data.hips,
                      thighs=data.thighs,
                      calves=data.calves)
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

async def get_measurements(db: AsyncSession, user_id: int, measurement_id: int):
    measurements = await get_user_obj_or_404(db, user_id, Measurement, measurement_id)
    data = MeasurementsRead.model_validate(measurements)
    return data

async def get_latest_measurements(db: AsyncSession, user_id: int):
    result = await db.execute(select(Measurement).where(Measurement.user_id == user_id).order_by(Measurement.date.desc()))
    measurements = result.scalars().first()
    if measurements is None:
        return None
    data = MeasurementsRead.model_validate(measurements)
    return data

async def get_previous_measurements(db: AsyncSession, user_id: int):
    result = await db.execute(select(Measurement).where(Measurement.user_id == user_id).order_by(Measurement.date.desc()).offset(1).limit(1))
    measurements = result.scalars().first()
    if measurements is None:
        return None
    data = MeasurementsRead.model_validate(measurements)
    return data

async def get_measurements_list(db: AsyncSession, user_id: int, offset: int = 0, limit: int = 10):
    result = await db.execute(select(Measurement).where(Measurement.user_id == user_id).order_by(Measurement.date.desc()).offset(offset).limit(limit))
    measurements_list = result.scalars().all()
    data = [MeasurementsRead.model_validate(measurements) for measurements in measurements_list]
    return data

async def delete_measurements(db: AsyncSession, user_id: int, measurements_id: int):
    return await delete_user_obj_or_404(db, user_id, Measurement, measurements_id)

async def create_weight(db: AsyncSession, data: WeightCreate):
    return await create_instance(db, Weight, data.model_dump())
    # TODO: improve exception messages for constraint violations (unique date, FK errors, etc.)


async def delete_weight(db: AsyncSession, user_id: int, weight_id: int):
    return await delete_user_obj_or_404(db, user_id, Weight, weight_id)


async def get_current_weight(db: AsyncSession, user_id: int) -> Weight | None:
    result = await db.execute(select(Weight).where(Weight.user_id == user_id).order_by(Weight.date.desc()))
    return result.scalars().first()

async def get_previous_weight(db: AsyncSession, user_id: int) -> Weight | None:
    result = await db.execute(select(Weight).where(Weight.user_id == user_id).order_by(Weight.date.desc()).offset(1).limit(1))
    return result.scalars().first()

async def get_user_weight(db: AsyncSession, user_id: int, weights_id: int) -> Weight | None:
    return await get_user_obj_or_404(db, user_id, Weight, weights_id)

async def get_user_weights(db: AsyncSession, user_id: int, offset: int = 0, limit: int = 10) -> Sequence[Weight | None]:
    result = await db.execute(select(Weight).where(Weight.user_id == user_id).order_by(Weight.date.desc()).offset(offset).limit(limit))
    return result.scalars().all()
