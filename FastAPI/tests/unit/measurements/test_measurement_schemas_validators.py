import pytest

from app.measurements.schemas import MeasurementsCreate


class TestMeasurementSchemas:

    def test_check_at_least_one_success(self):
        data = MeasurementsCreate(
            neck=32,
            waist=80
        )
        assert data.neck == 32
        assert data.waist == 80

    def test_check_at_least_one_no_measurements(self):
        with pytest.raises(ValueError):
            data = MeasurementsCreate()
