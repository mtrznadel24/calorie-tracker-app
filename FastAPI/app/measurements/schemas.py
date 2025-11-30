import datetime as dt

from pydantic import BaseModel, ConfigDict, Field, model_validator


class WeightCreate(BaseModel):
    date: dt.date = Field(default_factory=dt.date.today)
    weight: float | None = Field(default=None, gt=0, lt=300)


class WeightRead(BaseModel):
    id: int
    date: dt.date
    weight: float

    model_config = ConfigDict(from_attributes=True)


class MeasurementsCreate(BaseModel):
    date: dt.date = Field(default_factory=dt.date.today)
    weight: WeightCreate | None = Field(default=None)
    neck: float | None = Field(default=None, gt=0, lt=80)
    biceps: float | None = Field(default=None, gt=0, lt=80)
    chest: float | None = Field(default=None, gt=0, lt=200)
    waist: float | None = Field(default=None, gt=0, lt=200)
    hips: float | None = Field(default=None, gt=0, lt=200)
    thighs: float | None = Field(default=None, gt=0, lt=150)
    calves: float | None = Field(default=None, gt=0, lt=80)

    @model_validator(mode="after")
    def check_at_least_one(cls, values):
        if not any(
            [
                values.weight,
                values.neck,
                values.biceps,
                values.chest,
                values.waist,
                values.hips,
                values.thighs,
                values.calves,
            ]
        ):
            raise ValueError("At least one measurement or weight must be provided")
        return values


class MeasurementsRead(BaseModel):
    id: int
    date: dt.date
    weight: WeightRead | None
    neck: float | None
    biceps: float | None
    chest: float | None
    waist: float | None
    hips: float | None
    thighs: float | None
    calves: float | None

    model_config = ConfigDict(from_attributes=True)
