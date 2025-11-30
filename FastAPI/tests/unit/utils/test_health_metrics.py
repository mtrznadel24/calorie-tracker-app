import pytest

from app.user.models import Gender
from app.utils.health_metrics import calculate_bmi, calculate_bmr, calculate_tdee


@pytest.mark.unit
class TestHealthMetrics:
    def test_calculate_bmr_male(self):
        result = calculate_bmr(80, 170, 25, Gender.MALE)
        assert result == 1742

    def test_calculate_bmr_female(self):
        result = calculate_bmr(60, 160, 25, Gender.FEMALE)
        assert result == 1314

    def test_calculate_bmr_unknown_gender(self):
        with pytest.raises(ValueError):
            calculate_bmr(77, 176, 25, "unknown")

    def test_calculate_tdee_sedentary(self):
        result = calculate_tdee(1700, 1.2)
        assert result == 2040

    def test_calculate_tdee_active(self):
        result = calculate_tdee(1700, 1.725)
        assert result == 2932

    def test_calculate_bmi_normal(self):
        result = calculate_bmi(70, 175)
        assert result == 22.9

    def test_calculate_bmi_overweight(self):
        result = calculate_bmi(85, 170)
        assert result == 29.4

    def test_calculate_bmi_underweight(self):
        result = calculate_bmi(50, 175)
        assert result == 16.3
