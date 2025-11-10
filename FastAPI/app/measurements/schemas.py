from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class WeightCreate(BaseModel):
    date: date = Field(default_factory=date.today)
    weight: float | None = Field(default=None, gt=0, lt=300)


class WeightRead(BaseModel):
    id: int
    date: date
    weight: float


class MeasurementsCreate(BaseModel):
    date: date = Field(default_factory=date.today)
    weight: WeightCreate | None
    neck: float | None = Field(default=None, gt=0, lt=80)
    biceps: float | None = Field(default=None, gt=0, lt=80)
    chest: float | None = Field(default=None, gt=0, lt=200)
    waist: float | None = Field(default=None, gt=0, lt=200)
    hips: float | None = Field(default=None, gt=0, lt=200)
    thighs: float | None = Field(default=None, gt=0, lt=150)
    calves: float | None = Field(default=None, gt=0, lt=80)


class MeasurementsRead(BaseModel):
    id: int
    date: date
    weight: WeightRead | None
    neck: float | None
    biceps: float | None
    chest: float | None
    waist: float | None
    hips: float | None
    thighs: float | None
    calves: float | None

    model_config = ConfigDict(from_attributes=True)
