import datetime as dt

import pytest

from app.core.exceptions import ConflictError
from app.measurements.schemas import MeasurementsCreate, WeightCreate


@pytest.mark.integration
class TestMeasurementService:

    async def test_create_measurements_no_weight(self, measurements_service, user):
        today = dt.date.today()

        data = MeasurementsCreate(biceps=35, chest=80, waist=80)

        result = await measurements_service.create_measurements(user.id, data)

        assert result.date == today
        assert result.biceps == 35
        assert result.chest == 80
        assert result.waist == 80
        assert result.weight_id is None
        assert result.neck is None

    async def test_create_measurements_with_weight(self, measurements_service, user):
        today = dt.date.today()

        data_weight = WeightCreate(weight=80)
        data = MeasurementsCreate(weight=data_weight, biceps=35, chest=80, waist=80)

        result = await measurements_service.create_measurements(user.id, data)
        weight = result.weight

        assert result.date == today
        assert result.biceps == 35
        assert result.chest == 80
        assert result.waist == 80
        assert result.weight_id == weight.id
        assert result.neck is None

    async def test_create_measurements_failure(
        self, measurements_service, user, sample_measurement
    ):
        data_weight = WeightCreate(weight=80)
        data = MeasurementsCreate(
            date=dt.date(2022, 1, 1), weight=data_weight, biceps=35, chest=80, waist=80
        )

        with pytest.raises(ConflictError):
            await measurements_service.create_measurements(user.id, data)

    async def test_create_weight_success(self, weight_service, user):
        today = dt.date.today()
        data = WeightCreate(weight=80)

        result = await weight_service.create_weight(user.id, data)

        assert result.date == today
        assert result.weight == 80
        assert result.user_id == user.id

    async def test_create_weight_weight_exists(
        self, weight_service, user, sample_weight
    ):
        data = WeightCreate(date=dt.date(2022, 1, 1), weight=85)

        result = await weight_service.create_weight(user.id, data)

        assert result.date == dt.date(2022, 1, 1)
        assert result.weight == 85
        assert result.user_id == user.id
