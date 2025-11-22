from datetime import date

import pytest

from app.measurements.repositories import MeasurementRepository

@pytest.mark.integration
class TestMeasurementRepository:

    async def test_get_latest_measurements(self, session, user, sample_measurements):
        repo = MeasurementRepository(session)

        result = await repo.get_latest_measurements(user.id)

        assert result == sample_measurements[2]

    async def test_get_latest_measurements_no_measurements(self, session, user):
        repo = MeasurementRepository(session)

        result = await repo.get_latest_measurements(user.id)

        assert result is None

    async def test_get_previous_measurements(self, session, user, sample_measurements):
        repo = MeasurementRepository(session)

        result = await repo.get_previous_measurements(user.id)

        assert result == sample_measurements[1]

    async def test_get_previous_measurements_no_measurements(self, session, user):
        repo = MeasurementRepository(session)

        result = await repo.get_previous_measurements(user.id)

        assert result is None

    async def test_get_measurements_list(self, session, user, sample_measurements):
        repo = MeasurementRepository(session)

        result = await repo.get_measurements_list(user.id, 0, 10)

        assert result == sorted(sample_measurements, key=lambda w: w.date, reverse=True)

    async def test_get_measurements_list_offset(self, session, user, sample_measurements):
        repo = MeasurementRepository(session)

        result = await repo.get_measurements_list(user.id, 1, 10)

        assert result == sorted(sample_measurements, key=lambda w: w.date, reverse=True)[1:]

    async def test_get_measurements_list_limit(self, session, user, sample_measurements):
        repo = MeasurementRepository(session)

        result = await repo.get_measurements_list(user.id, 0, 2)

        assert result == sorted(sample_measurements, key=lambda w: w.date, reverse=True)[:2]

    async def test_get_measurements_list_no_weights(self, session, user):
        repo = MeasurementRepository(session)

        result = await repo.get_measurements_list(user.id, 0, 10)

        assert result == []
