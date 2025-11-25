from app.user.models import Gender


def calculate_bmr(weight: float, height: float, age: int, gender: Gender) -> int:
    if gender == Gender.MALE:
        return int((10 * weight) + (6.25 * height) - (5 * age) + 5)
    elif gender == Gender.FEMALE:
        return int((10 * weight) + (6.25 * height) - (5 * age) - 161)
    else:
        raise ValueError("Unknown gender")


def calculate_tdee(bmr: int, activity_level: float) -> int:
    return int(bmr * activity_level)


def calculate_bmi(weight: float, height: float) -> float:
    height /= 100
    return round(weight / (height**2), 1)
