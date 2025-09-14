from fastapi import FastAPI

from app.exception_handler import register_exception_handlers
from app.routers import user, meals, fridge

app = FastAPI()
register_exception_handlers(app)

app.include_router(user.router)
app.include_router(meals.router)
app.include_router(fridge.router)