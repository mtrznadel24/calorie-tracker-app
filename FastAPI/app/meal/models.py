from enum import Enum

from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from app.core.db import Base


class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    SUPPER = "supper"


class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    date = Column(Date, index=True, nullable=False)
    type = Column(SqlEnum(MealType, name="meal_type"), index=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "date", "type", name="uq_user_meal_per_day_type"),
    )

    user = relationship("User", back_populates="meals")
    ingredients = relationship(
        "MealIngredient",
        back_populates="meal",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class MealIngredient(Base):
    __tablename__ = "meal_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, nullable=False)
    meal_id = Column(
        Integer, ForeignKey("meals.id", ondelete="CASCADE"), index=True, nullable=False
    )

    meal = relationship("Meal", back_populates="ingredients")
    details = relationship(
        "MealIngredientDetails",
        back_populates="meal_ingredient",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )


class MealIngredientDetails(Base):
    __tablename__ = "meal_ingredients_details"
    id = Column(
        Integer, ForeignKey("meal_ingredients.id", ondelete="CASCADE"), primary_key=True
    )
    product_name = Column(String, index=True, nullable=False)
    calories_100g = Column(Float, nullable=False, default=0)
    proteins_100g = Column(Float, nullable=False, default=0)
    fats_100g = Column(Float, nullable=False, default=0)
    carbs_100g = Column(Float, nullable=False, default=0)

    meal_ingredient = relationship("MealIngredient", back_populates="details")
