from typing import Annotated

from fastapi import Depends

from app.core.db import DbSessionDep
from app.measurements.services import WeightService, MeasurementsService


def get_weight_service(db: DbSessionDep):
    return WeightService(db)

WeightServiceDep = Annotated[WeightService, Depends(get_weight_service)]

def get_measurements_service(db: DbSessionDep):
    return MeasurementsService(db)

MeasurementsServiceDep = Annotated[MeasurementsService, Depends(get_measurements_service)]