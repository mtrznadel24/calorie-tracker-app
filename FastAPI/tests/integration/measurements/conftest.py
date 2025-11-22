from datetime import date

import pytest_asyncio

from app.measurements.models import Weight, Measurement


@pytest_asyncio.fixture
async def sample_weight(session, user):
    weight = Weight(user_id=user.id, date=date(2022, 1, 1), weight=80)
    session.add(weight)
    await session.commit()
    await session.refresh(weight)
    return weight

@pytest_asyncio.fixture
async def sample_weights(session, user):
    weights = [Weight(user_id=user.id, date=date(2022, 1, 1), weight=80),
               Weight(user_id=user.id, date=date(2022, 1, 2), weight=82),
               Weight(user_id=user.id, date=date(2022, 1, 3), weight=84)]
    session.add_all(weights)
    await session.commit()
    for w in weights:
        await session.refresh(w)
    return weights


@pytest_asyncio.fixture
async def sample_measurement(session, user, sample_weight):
    measurement = Measurement(
                        user_id=user.id,
                        date=date(2022, 1, 1),
                        weight_id=sample_weight.id,
                        neck=38.0,
                        biceps=32.5,
                        chest=100.0,
                        waist=85.0,
                        hips=95.0,
                        thighs=55.0,
                        calves=37.0,
                    )
    session.add(measurement)
    await session.commit()
    await session.refresh(measurement)
    return measurement

@pytest_asyncio.fixture
async def sample_measurements(session, user, sample_weights):
    measurements = [
        Measurement(
            user_id=user.id,
            date=date(2022, 1, 1),
            weight_id=sample_weights[0].id,
            neck=38.0,
            biceps=32.5,
            chest=100.0,
            waist=85.0,
            hips=95.0,
            thighs=55.0,
            calves=37.0,
        ),
        Measurement(
            user_id=user.id,
            date=date(2022, 1, 2),
            weight_id=sample_weights[1].id,
            neck=38.2,
            biceps=33.0,
            chest=101.0,
            waist=84.5,
            hips=95.5,
            thighs=55.5,
            calves=37.2,
        ),
        Measurement(
            user_id=user.id,
            date=date(2022, 1, 3),
            weight_id=sample_weights[2].id,
            neck=38.5,
            biceps=33.2,
            chest=102.0,
            waist=84.0,
            hips=96.0,
            thighs=56.0,
            calves=37.5,
        ),
    ]

    session.add_all(measurements)
    await session.commit()
    for m in measurements:
        await session.refresh(m)
    return measurements