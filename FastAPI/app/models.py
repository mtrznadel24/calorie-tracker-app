from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Enum, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date
from app.enums import MealType, FoodCategory


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    height = Column(Float)

    fridge = relationship("Fridge", back_populates="user", uselist=False, cascade="all, delete-orphan")
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")
    weights = relationship("Weight", back_populates="user", cascade="all, delete-orphan")
    measurements = relationship("Measurement", back_populates="user", cascade="all, delete-orphan")

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    type = Column(Enum(MealType, name="meal_type"), index=True, nullable=False)

    user = relationship("User", back_populates="meals")
    ingredients = relationship(
        "MealIngredient",
        back_populates="meal",
        cascade="all, delete-orphan"
    )

class MealIngredient(Base):
    __tablename__ = "meal_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, nullable=False)
    meal_id = Column(Integer, ForeignKey("meals.id", ondelete="CASCADE"), index=True, nullable=False)

    meal = relationship("Meal", back_populates="ingredients")
    details = relationship("MealIngredientDetails", back_populates="meal_ingredient", uselist=False, cascade="all, delete-orphan")

class MealIngredientDetails(Base):
    __tablename__ = "meal_ingredients_details"
    id = Column(Integer, ForeignKey("meal_ingredients.id", ondelete="CASCADE"), primary_key=True)
    product_name = Column(String, index=True, nullable=False)
    calories_100g = Column(Float, nullable=False, default=0)
    proteins_100g = Column(Float, nullable=False, default=0)
    fats_100g = Column(Float, nullable=False, default=0)
    carbs_100g = Column(Float, nullable=False, default=0)

    meal_ingredient = relationship("MealIngredient", back_populates="details")

class Fridge(Base):
    __tablename__ = "fridges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    user = relationship("User", back_populates="fridge")
    fridge_meals = relationship("FridgeMeal", back_populates="fridge", cascade="all, delete-orphan")
    fridge_products = relationship("FridgeProduct", back_populates="fridge", cascade="all, delete-orphan")

class FridgeMeal(Base):
    __tablename__ = "fridge_meals"
    id = Column(Integer, primary_key=True, index=True)
    fridge_id = Column(Integer, ForeignKey("fridges.id", ondelete="CASCADE"), index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    is_favourite = Column(Boolean, index=True, nullable=False, default=False)
    __table_args__ = (
        UniqueConstraint("fridge_id", "name", name="un_fridge_meal_name"),
    )

    fridge = relationship("Fridge", back_populates="fridge_meals")
    ingredients = relationship(
        "FridgeMealIngredient",
        back_populates="fridge_meal",
        cascade="all, delete-orphan"
    )

class FridgeProduct(Base):
    __tablename__ = "fridge_products"
    id = Column(Integer, primary_key=True, index=True)
    fridge_id = Column(Integer, ForeignKey("fridges.id", ondelete="CASCADE"), index=True, nullable=False)
    product_name = Column(String, index=True, nullable=False)
    calories_100g = Column(Float, nullable=False, default=0)
    proteins_100g = Column(Float, nullable=False, default=0)
    fats_100g = Column(Float, nullable=False, default=0)
    carbs_100g = Column(Float, nullable=False, default=0)
    category = Column(Enum(FoodCategory, index=True, name="food_category"))
    is_favourite = Column(Boolean, index=True, nullable=False, default=False)
    __table_args__ = (
        UniqueConstraint("fridge_id", "product_name", name="un_fridge_product_name"),
    )

    fridge = relationship("Fridge", back_populates="fridge_products")
    fridge_meal_ingredient = relationship("FridgeMealIngredient", back_populates="fridge_product", cascade="all, delete-orphan")

class FridgeMealIngredient(Base):
    __tablename__ = "fridge_meal_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, nullable=False)
    fridge_meal_id = Column(Integer, ForeignKey("fridge_meals.id", ondelete="CASCADE"), index=True, nullable=False)
    fridge_product_id = Column(Integer, ForeignKey("fridge_products.id", ondelete="CASCADE"), nullable=False)

    fridge_meal = relationship("FridgeMeal", back_populates="ingredients")
    fridge_product = relationship("FridgeProduct", back_populates="fridge_meal_ingredient")

class Weight(Base):
    __tablename__ = "weights"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    date = Column(Date, default=date.today, index=True, nullable=False)
    weight = Column(Float, nullable=False)
    __table_args__ = (UniqueConstraint("user_id", "date", name="weight_user_date_uc"),)

    user = relationship("User", back_populates="weights")

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    date = Column(Date, default=date.today, index=True, nullable=False)
    weight_id = Column(Integer, ForeignKey("weights.id", ondelete="SET NULL"), nullable=True)
    neck = Column(Float)
    biceps = Column(Float)
    chest = Column(Float)
    waist = Column(Float)
    hips = Column(Float)
    thighs = Column(Float)
    calves = Column(Float)
    __table_args__ = (UniqueConstraint("user_id", "date", name="measurement_user_date_uc"),)

    user = relationship("User", back_populates="measurements")