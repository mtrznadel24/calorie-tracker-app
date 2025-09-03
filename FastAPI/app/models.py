from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Enum, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base
import enum
from datetime import datetime

class MealType(enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    SUPPER = "supper"

class FoodCategory(enum.Enum):
    FRUIT = "fruits"
    VEGETABLE = "vegetables"
    GRAINS = "grains"
    DAIRY = "dairy"
    MEAT_FISH = "meat and fish"
    PLANT_PROTEIN = "plant protein"
    FATS = "fats"
    DRINKS = "drinks"
    SNACKS = "snacks"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    height = Column(Float)

    fridge = relationship("Fridge", back_populates="user", uselist=False)
    meal = relationship("Meal", back_populates="user", uselist=False)

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    fridge_meal_id = Column(Integer, ForeignKey("fridge_meals.id"))
    date = Column(DateTime, default=datetime.utcnow)
    type = Column(Enum(MealType), nullable=False)

    user = relationship("User", back_populates="meals")
    ingredients = relationship(
        "MealIngredient",
        back_populates="meal",
        cascade="all, delete-orphan"
    )

class Fridge(Base):
    __tablename__ = "fridges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="fridge")
    fridge_meal = relationship("FridgeMeal", back_populates="fridge")
    fridge_product = relationship("FridgeProduct", back_populates="fridge")

class FridgeMeal(Base):
    __tablename__ = "fridge_meals"
    id = Column(Integer, primary_key=True, index=True)
    fridge_id = Column(Integer, ForeignKey("fridges.id"))
    name = Column(String)
    is_favourite = Column(Boolean, nullable=False, default=False)

    fridge = relationship("Fridge", back_populates="fridge_meal")

class FridgeProduct(Base):
    __tablename__ = "fridge_products"
    id = Column(Integer, primary_key=True, index=True)
    fridge_id = Column(Integer, ForeignKey("fridges.id"))
    product_name = Column(String)
    calories_100g = Column(Float)
    proteins_100g = Column(Float)
    fats_100g = Column(Float)
    carbs_100g = Column(Float)
    category = Column(Enum(FoodCategory))
    is_favourite = Column(Boolean, nullable=False, default=False)

    fridge = relationship("Fridge", back_populates="fridge_product")

class MealIngredient(Base):
    __tablename__ = "meal_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float)
    meal_id = Column(Integer, ForeignKey("meals.id"))
    fridge_product_id = Column(Integer, ForeignKey("fridge_products.id"))

    meal = relationship("Meal", back_populates="ingredients")

class Weight(Base):
    __tablename__ = "weights"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)
    weight = Column(Float)
    __table_args__ = (UniqueConstraint("user_id", "date", name="weight_user_date_uc"),)

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)
    weight_id = Column(Integer, ForeignKey("weights.id"))
    neck = Column(Float)
    biceps = Column(Float)
    chest = Column(Float)
    waist = Column(Float)
    hips = Column(Float)
    thighs = Column(Float)
    calves = Column(Float)
    __table_args__ = (UniqueConstraint("user_id", "date", name="measurement_user_date_uc"),)

