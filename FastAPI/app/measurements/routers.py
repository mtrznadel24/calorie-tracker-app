from collections.abc import Sequence

from fastapi import APIRouter

from app.core.security import UserDep
from app.measurements.depedencies import MeasurementsServiceDep, WeightServiceDep
from app.measurements.models import Measurement, Weight
from app.measurements.schemas import (
    MeasurementsCreate,
    MeasurementsRead,
    WeightCreate,
    WeightRead,
)

measurements_router = APIRouter(prefix="/measurements", tags=["measurements"])
weights_router = APIRouter(prefix="/weights", tags=["weights"])


@measurements_router.post("", response_model=MeasurementsRead)
async def add_measurements(
    measurements_service: MeasurementsServiceDep, user: UserDep, measurements_in: MeasurementsCreate
) -> Measurement:
    return await measurements_service.create_measurements(user.id, measurements_in)


@measurements_router.get("/{measurements_id}", response_model=MeasurementsRead)
async def read_measurements(
    measurements_service: MeasurementsServiceDep, user: UserDep, measurements_id: int
) -> Measurement:
    return await measurements_service.get_measurements(user.id, measurements_id)


@measurements_router.get("/latest", response_model=MeasurementsRead)
async def read_latest_measurements(measurements_service: MeasurementsServiceDep, user: UserDep) -> Measurement:
    return await measurements_service.get_latest_measurements(user.id)


@measurements_router.get("/previous", response_model=MeasurementsRead)
async def read_previous_measurements(measurements_service: MeasurementsServiceDep, user: UserDep) -> Measurement:
    return await measurements_service.get_previous_measurements(user.id)


@measurements_router.get("", response_model=list[MeasurementsRead])
async def read_measurements_list(
    measurements_service: MeasurementsServiceDep, user: UserDep
) -> Sequence[Measurement]:
    return await measurements_service.get_measurements_list(user.id)


@measurements_router.delete("/{measurements_id}", response_model=MeasurementsRead)
async def delete_measurements_route(
    measurements_service: MeasurementsServiceDep, user: UserDep, measurements_id: int
) -> Measurement:
    return await measurements_service.delete_measurements(user.id, measurements_id)


@weights_router.post("", response_model=WeightRead)
async def add_weight(
    weight_service: WeightServiceDep, user: UserDep, weight_in: WeightCreate
) -> Weight:
    return await weight_service.create_weight(user.id, weight_in)


@weights_router.get("/current", response_model=WeightRead)
async def read_current_weight(weight_service: WeightServiceDep, user: UserDep) -> Weight:
    return await weight_service.get_current_weight(user.id)


@weights_router.get("/previous", response_model=WeightRead)
async def read_previous_weight(weight_service: WeightServiceDep, user: UserDep) -> Weight:
    return await weight_service.get_previous_weight(user.id)


@weights_router.get("/{weight_id}", response_model=WeightRead)
async def read_user_weight(
    weight_service: WeightServiceDep, user: UserDep, weight_id: int
) -> Weight | None:
    return await weight_service.get_user_weight(user.id, weight_id)


@weights_router.get("", response_model=list[WeightRead])
async def read_user_weights(weight_service: WeightServiceDep, user: UserDep) -> Sequence[Weight]:
    return await weight_service.get_user_weights(user.id)


@weights_router.delete("/{weight_id}", response_model=WeightRead)
async def delete_weight_route(
    weight_service: WeightServiceDep, user: UserDep, weight_id: int
) -> Weight:
    return await weight_service.delete_weight(user.id, weight_id)
