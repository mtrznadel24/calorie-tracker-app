from fastapi import FastAPI
from app.routers import user, meals, fridge

app = FastAPI()


app.include_router(user.router)
app.include_router(meals.router)
app.include_router(fridge.router)