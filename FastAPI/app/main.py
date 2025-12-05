import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.auth.routers import router as auth_router
from app.core.config import settings
from app.core.db import session_manager
from app.core.exception_handler import register_exception_handlers
from app.core.logging_config import setup_logging
from app.core.redis_session import close_redis_session
from app.fridge.routers import router as fridge_router
from app.meal.routers import router as meal_router
from app.measurements.routers import measurements_router, weights_router
from app.user.routers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application lifespan started")
    try:
        yield
    finally:
        if session_manager._engine:
            logger.info("Closing database session manager")
            await session_manager.close()
        logger.info("Closing Redis session")
        await close_redis_session()
        logger.info("Application lifespan finished")

app = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME, docs_url="/docs")
register_exception_handlers(app)

setup_logging()
logger = logging.getLogger(__name__)

app.include_router(user_router)
app.include_router(meal_router)
app.include_router(fridge_router)
app.include_router(auth_router)
app.include_router(measurements_router)
app.include_router(weights_router)


def get_app():
    return app


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
