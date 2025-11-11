from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.base_repository import BaseRepository, UserScopedRepository
from app.measurements.models import Measurement, Weight


class MeasurementRepository(UserScopedRepository[Measurement]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Measurement)

    async def get_latest_measurements(self, user_id: int) -> Measurement:
        result = await self.db.execute(
            select(Measurement)
            .where(Measurement.user_id == user_id)
            .order_by(Measurement.date.desc())
        )
        return result.scalars().first()

    async def get_previous_measurements(self, user_id: int) -> Measurement:
        result = await self.db.execute(
            select(Measurement)
            .where(Measurement.user_id == user_id)
            .order_by(Measurement.date.desc())
            .offset(1)
            .limit(1)
        )
        return result.scalars().first()

    async def get_measurements_list(
        self, user_id: int, offset: int = 0, limit: int = 10
    ):
        result = await self.db.execute(
            select(Measurement)
            .options(selectinload(Measurement.weight))
            .where(Measurement.user_id == user_id)
            .order_by(Measurement.date.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()



class WeightRepository(UserScopedRepository[Weight]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Weight)

    async def get_weight_by_date(self, user_id: int, date) -> Weight:
        result = await self.db.execute(
            select(Weight).where(Weight.user_id == user_id, Weight.date == date)
        )
        return result.scalar_one_or_none()

    async def get_current_weight(self, user_id: int) -> Weight | None:
        result = await self.db.execute(
            select(Weight).where(Weight.user_id == user_id).order_by(Weight.date.desc())
        )
        return result.scalars().first()

    async def get_previous_weight(self, user_id: int) -> Weight | None:
        result = await self.db.execute(
            select(Weight)
            .where(Weight.user_id == user_id)
            .order_by(Weight.date.desc())
            .offset(1)
            .limit(1)
        )
        return result.scalars().first()

    async def get_weights(self, user_id, offset: int = 0, limit: int = 10):
        result = await self.db.execute(
            select(Weight)
            .where(Weight.user_id == user_id)
            .order_by(Weight.date.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()