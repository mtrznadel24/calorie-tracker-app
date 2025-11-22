from datetime import date

import pytest

from app.measurements.repositories import WeightRepository


@pytest.mark.integration
class TestWeightRepository:

    async def test_get_weight_by_date_success(self, session, user, sample_weight):
        repo = WeightRepository(session)

        result = await repo.get_weight_by_date(user.id, date(2022, 1, 1))

        assert result == sample_weight

    async def test_get_weight_by_date_wrong_date(self, session, user, sample_weight):
        repo = WeightRepository(session)

        result = await repo.get_weight_by_date(user.id, date(2022, 1, 4))

        assert result is None


    async def test_get_current_weight(self, session, user, sample_weights):
        repo = WeightRepository(session)

        result = await repo.get_current_weight(user.id)

        assert result == sample_weights[2]

    async def test_get_current_weight_no_weights(self, session, user):
        repo = WeightRepository(session)

        result = await repo.get_current_weight(user.id)

        assert result is None


    async def test_get_previous_weight(self, session, user, sample_weights):
        repo = WeightRepository(session)

        result = await repo.get_previous_weight(user.id)

        assert result == sample_weights[1]

    async def test_get_previous_weight_no_weights(self, session, user):
        repo = WeightRepository(session)

        result = await repo.get_previous_weight(user.id)

        assert result is None

    async def test_get_weights(self, session, user, sample_weights):
        repo = WeightRepository(session)

        result = await repo.get_weights(user.id, 0, 10)

        assert result == sorted(sample_weights, key=lambda w: w.date, reverse=True)

    async def test_get_weights_offset(self, session, user, sample_weights):
        repo = WeightRepository(session)

        result = await repo.get_weights(user.id, 1, 10)

        assert result == sorted(sample_weights, key=lambda w: w.date, reverse=True)[1:]


    async def test_get_weights_limit(self, session, user, sample_weights):
        repo = WeightRepository(session)

        result = await repo.get_weights(user.id, 0, 2)

        assert result == sorted(sample_weights, key=lambda w: w.date, reverse=True)[:2]

    async def test_get_weights_no_weights(self, session, user):
        repo = WeightRepository(session)

        result = await repo.get_weights(user.id, 0, 10)

        assert result == []



