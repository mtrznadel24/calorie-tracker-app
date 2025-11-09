from collections.abc import Sequence

from fastapi import APIRouter

from app.core.db import DbSessionDep
from app.core.security import UserDep
from app.models import Weight, Measurement
from app.schemas.measurements import MeasurementsRead, MeasurementsCreate, WeightRead, WeightCreate
from app.services.measurements import create_measurements, get_latest_measurements, get_measurements, \
    get_previous_measurements, get_measurements_list, delete_measurements, create_weight, get_current_weight, \
    get_previous_weight, get_user_weights, get_user_weight, delete_weight


measurements_router = APIRouter(prefix="/measurements", tags=["measurements"])
weights_router = APIRouter(prefix="/weights", tags=["weights"])

@measurements_router.post("", response_model=MeasurementsRead)
async def add_measurements(db: DbSessionDep, user: UserDep, measurements_in: MeasurementsCreate) -> Measurement:
    return await create_measurements(db, user.id, measurements_in)


@measurements_router.get("/{measurements_id}", response_model=MeasurementsRead)
async def read_measurements(db: DbSessionDep, user: UserDep, measurements_id: int) -> Measurement:
    return await get_measurements(db, user.id, measurements_id)


@measurements_router.get("/latest", response_model=MeasurementsRead)
async def read_latest_measurements(db: DbSessionDep, user: UserDep) -> Measurement:
    return await get_latest_measurements(db, user.id)


@measurements_router.get("/previous", response_model=MeasurementsRead)
async def read_previous_measurements(db: DbSessionDep, user: UserDep) -> Measurement:
    return await get_previous_measurements(db, user.id)


@measurements_router.get("", response_model=list[MeasurementsRead])
async def read_measurements_list(db: DbSessionDep, user: UserDep) -> Sequence[Measurement]:
    return await get_measurements_list(db, user.id)


@measurements_router.delete("/{measurements_id}", response_model=MeasurementsRead)
async def delete_measurements_route(db: DbSessionDep, user: UserDep, measurements_id: int) -> Measurement:
    return await delete_measurements(db, user.id, measurements_id)


@weights_router.post("", response_model=WeightRead)
async def add_weight(db: DbSessionDep, user: UserDep, weight_in: WeightCreate) -> Weight:
    return await create_weight(db, user.id, weight_in)


@weights_router.get("/current", response_model=WeightRead)
async def read_current_weight(db: DbSessionDep, user: UserDep) -> Weight:
    return await get_current_weight(db, user.id)


@weights_router.get("/previous", response_model=WeightRead)
async def read_previous_weight(db: DbSessionDep, user: UserDep) -> Weight:
    return await get_previous_weight(db, user.id)


@weights_router.get("/{weight_id}", response_model=WeightRead)
async def read_user_weight(db: DbSessionDep, user: UserDep, weight_id: int) -> Weight | None:
    return await get_user_weight(db, user.id, weight_id)


@weights_router.get("", response_model=list[WeightRead])
async def read_user_weights(db: DbSessionDep, user: UserDep) -> Sequence[Weight]:
    return await get_user_weights(db, user.id)


@weights_router.delete("/{weight_id}", response_model=WeightRead)
async def delete_weight_route(db: DbSessionDep, user: UserDep, weight_id: int) -> Weight:
    return await delete_weight(db, user.id, weight_id)