from fastapi import FastAPI
from app.routers import users, meals, fridge

app = FastAPI()


app.include_router(users.router)
app.include_router(meals.router)
app.include_router(fridge.router)