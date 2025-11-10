import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.auth.routers import router as auth_router
from app.core.config import settings
from app.core.db import session_manager
from app.core.exception_handler import register_exception_handlers
from app.core.redis_session import close_redis_session
from app.fridge.routers import router as fridge_router
from app.meal.routers import router as meal_router
from app.measurements.routers import measurements_router, weights_router
from app.user.routers import router as user_router

logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG if settings.DEBUG_LOGS else logging.INFO
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        if session_manager._engine:
            await session_manager.close()
        await close_redis_session()


app = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME, docs_url="/docs")
register_exception_handlers(app)

app.include_router(user_router)
app.include_router(meal_router)
app.include_router(fridge_router)
app.include_router(auth_router)
app.include_router(measurements_router)
app.include_router(weights_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
