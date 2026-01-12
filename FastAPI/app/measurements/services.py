import logging
from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.measurements.models import Measurement, Weight
from app.measurements.repositories import MeasurementRepository, WeightRepository
from app.measurements.schemas import MeasurementsCreate, WeightCreate

logger = logging.getLogger(__name__)


class MeasurementsService:
    def __init__(self, db: AsyncSession):
        self.repo = MeasurementRepository(db)
        self.weight_repo = WeightRepository(db)
        self.weight_service = WeightService(db)

    async def create_measurements(
        self, user_id: int, data: MeasurementsCreate
    ) -> Measurement:
        weight_in = None
        if data.weight is not None:
            weight_in = await self.weight_service.get_and_update_or_create_weight(
                user_id, data.weight
            )
            await self.repo.flush()

        measurement = await self.repo.get_measurement_by_date(user_id, data.date)
        if measurement is None:
            measurement = Measurement(
                user_id=user_id,
                date=data.date,
                weight_id=weight_in.id if weight_in else None,
                **data.model_dump(exclude={"weight", "date"}),
            )
            self.repo.add(measurement)
        else:
            if weight_in:
                measurement.weight_id = weight_in.id
            update_data = data.model_dump(
                exclude={"weight", "date"}, exclude_unset=True
            )
            for key, value in update_data.items():
                setattr(measurement, key, value)

        await self.repo.commit_or_conflict()
        return await self.repo.refresh_and_return(measurement)

    async def get_measurements(self, user_id: int, measurement_id: int) -> Measurement:
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

    async def get_and_update_or_create_weight(
        self, user_id: int, data: WeightCreate
    ) -> Weight:
        weight = await self.repo.get_weight_by_date(user_id, data.date)
        if weight is None:
            weight = Weight(**data.model_dump(exclude_unset=True), user_id=user_id)
            self.repo.add(weight)
        else:
            weight.weight = data.weight
        return weight

    async def create_weight(self, user_id: int, data: WeightCreate) -> Weight:
        weight = await self.get_and_update_or_create_weight(user_id, data)
        try:
            await self.repo.commit_or_conflict()
        except IntegrityError:
            logger.warning(
                "Duplicate weight entry for user_id=%s date=%s", user_id, data.date
            )
            raise ConflictError(
                f"Weight with date:{data.date} already exists"
            ) from None
        return await self.repo.refresh_and_return(weight)

    async def get_current_weight(self, user_id: int) -> Weight | None:
        return await self.repo.get_current_weight(user_id)

    async def get_previous_weight(self, user_id: int) -> Weight | None:
        return await self.repo.get_previous_weight(user_id)

    async def get_user_weight(self, user_id: int, weight_id: int) -> Weight | None:
        return await self.repo.get_by_id_for_user(user_id, weight_id)

    async def get_user_weights(
        self, user_id: int, offset: int = 0, limit: int = 10
    ) -> Sequence[Weight | None]:
        return await self.repo.get_weights(user_id, offset, limit)

    async def delete_weight(self, user_id: int, weight_id: int) -> Weight:
        return await self.repo.delete_by_id_for_user(user_id, weight_id)
