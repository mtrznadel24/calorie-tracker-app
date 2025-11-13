from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.measurements.models import Measurement, Weight
from app.measurements.repositories import MeasurementRepository, WeightRepository
from app.measurements.schemas import MeasurementsCreate, WeightCreate


class MeasurementsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = MeasurementRepository(db)
        self.weight_repo = WeightRepository(db)


    async def create_measurements(
        self, user_id: int, data: MeasurementsCreate
    ) -> Measurement:
        weight_in = None
        if data.weight is not None:
            weight_in = Weight(**data.weight.model_dump(exclude_unset=True), user_id=user_id)
            self.weight_repo.add(weight_in)
            await self.repo.flush()
        measurements_in = Measurement(
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
        self.repo.add(measurements_in)
        try:
            await self.repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError(f"Measurements with date:{data.date} already exists")
        return await self.repo.refresh_and_return(measurements_in)


    async def get_measurements(
        self, user_id: int, measurement_id: int
    ) -> Measurement:
        return await self.repo.get_by_id_for_user(user_id, measurement_id)


    async def get_latest_measurements(self, user_id: int) -> Measurement:
        return await self.repo.get_latest_measurements(user_id)


    async def get_previous_measurements(self, user_id: int) -> Measurement:
        return await self.repo.get_previous_measurements(user_id)


    async def get_measurements_list(
        self, user_id: int, offset: int = 0, limit: int = 10
    ) -> Sequence[Measurement]:
        return await self.repo.get_measurements_list(user_id, offset, limit)


    async def delete_measurements(
        self, user_id: int, measurements_id: int
    ) -> Measurement:
        return await self.repo.delete_by_id_for_user(user_id, measurements_id)


class WeightService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = WeightRepository(db)

    async def create_weight(self, user_id: int, data: WeightCreate) -> Weight:
        weight = self.repo.get_weight_by_date(user_id, data.date)
        if weight is None:
            weight = Weight(**data.model_dump(exclude_unset=True), user_id=user_id)
            self.repo.add(weight)
        else:
            setattr(weight, "weight", data.weight)
        try:
            await self.repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError(f"Weight with date:{data.date} already exists")
        return await self.repo.refresh_and_return(weight)


    async def get_current_weight(self, user_id: int) -> Weight | None:
        return await self.repo.get_current_weight(user_id)


    async def get_previous_weight(self, user_id: int) -> Weight | None:
        return await self.repo.get_previous_weight(user_id)


    async def get_user_weight(
        self, user_id: int, weight_id: int
    ) -> Weight | None:
        return await self.repo.get_by_id_for_user(user_id, weight_id)


    async def get_user_weights(
        self, user_id: int, offset: int = 0, limit: int = 10
    ) -> Sequence[Weight | None]:
        return await self.repo.get_weights(user_id, offset, limit)


    async def delete_weight(self, user_id: int, weight_id: int) -> Weight:
        return await self.repo.delete_by_id_for_user(user_id, weight_id)
