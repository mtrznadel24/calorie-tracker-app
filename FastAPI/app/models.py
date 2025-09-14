from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Enum, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date
from app.enums import MealType, FoodCategory


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    height = Column(Float)

    fridge = relationship("Fridge", back_populates="user", uselist=False)
    meals = relationship("Meal", back_populates="user")

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    type = Column(Enum(MealType, name="meal_type"), nullable=False)

    user = relationship("User", back_populates="meals")
    ingredients = relationship(
        "MealIngredient",
        back_populates="meal",
        cascade="all, delete-orphan"
    )

class MealIngredient(Base):
    __tablename__ = "meal_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float)
    meal_id = Column(Integer, ForeignKey("meals.id"))
    fridge_product_id = Column(Integer, ForeignKey("fridge_products.id"))

    meal = relationship("Meal", back_populates="ingredients")
    fridge_product = relationship("FridgeProduct", back_populates="meal_ingredient")

class Fridge(Base):
    __tablename__ = "fridges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="fridge")
    fridge_meals = relationship("FridgeMeal", back_populates="fridge")
    fridge_products = relationship("FridgeProduct", back_populates="fridge")

class FridgeMeal(Base):
    __tablename__ = "fridge_meals"
    id = Column(Integer, primary_key=True, index=True)
    fridge_id = Column(Integer, ForeignKey("fridges.id"))
    name = Column(String)
    is_favourite = Column(Boolean, nullable=False, default=False)

    fridge = relationship("Fridge", back_populates="fridge_meals")
    ingredients = relationship(
        "FridgeMealIngredient",
        back_populates="fridge_meal",
        cascade="all, delete-orphan"
    )

class FridgeProduct(Base):
    __tablename__ = "fridge_products"
    id = Column(Integer, primary_key=True, index=True)
    fridge_id = Column(Integer, ForeignKey("fridges.id"))
    product_name = Column(String)
    calories_100g = Column(Float)
    proteins_100g = Column(Float)
    fats_100g = Column(Float)
    carbs_100g = Column(Float)
    category = Column(Enum(FoodCategory, name="food_category"))
    is_favourite = Column(Boolean, nullable=False, default=False)

    fridge = relationship("Fridge", back_populates="fridge_products")
    fridge_meal_ingredient = relationship("FridgeMealIngredient", back_populates="fridge_product")
    meal_ingredient = relationship("MealIngredient", back_populates="fridge_product")

class FridgeMealIngredient(Base):
    __tablename__ = "fridge_meal_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float)
    fridge_meal_id = Column(Integer, ForeignKey("fridge_meals.id"))
    fridge_product_id = Column(Integer, ForeignKey("fridge_products.id"))

    fridge_meal = relationship("FridgeMeal", back_populates="ingredients")
    fridge_product = relationship("FridgeProduct", back_populates="fridge_meal_ingredient")

class Weight(Base):
    __tablename__ = "weights"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, default=date.today)
    weight = Column(Float)
    __table_args__ = (UniqueConstraint("user_id", "date", name="weight_user_date_uc"),)

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, default=date.today)
    weight_id = Column(Integer, ForeignKey("weights.id"))
    neck = Column(Float)
    biceps = Column(Float)
    chest = Column(Float)
    waist = Column(Float)
    hips = Column(Float)
    thighs = Column(Float)
    calves = Column(Float)
    __table_args__ = (UniqueConstraint("user_id", "date", name="measurement_user_date_uc"),)

