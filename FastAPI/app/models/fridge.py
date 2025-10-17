from enum import Enum

from sqlalchemy import Boolean, Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.db import Base


class FoodCategory(Enum):
    FRUIT = "fruits"
    VEGETABLE = "vegetables"
    GRAINS = "grains"
    DAIRY = "dairy"
    MEAT_FISH = "meat and fish"
    PLANT_PROTEIN = "plant protein"
    FATS = "fats"
    DRINKS = "drinks"
    SNACKS = "snacks"


class Fridge(Base):
    __tablename__ = "fridges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )

    user = relationship("User", back_populates="fridge")
    fridge_meals = relationship(
        "FridgeMeal", back_populates="fridge", cascade="all, delete-orphan"
    )
    fridge_products = relationship(
        "FridgeProduct", back_populates="fridge", cascade="all, delete-orphan"
    )


class FridgeMeal(Base):
    __tablename__ = "fridge_meals"
    id = Column(Integer, primary_key=True, index=True)
    fridge_id = Column(
        Integer,
        ForeignKey("fridges.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    name = Column(String, index=True, nullable=False)
    is_favourite = Column(Boolean, index=True, nullable=False, default=False)
    __table_args__ = (
        UniqueConstraint("fridge_id", "name", name="un_fridge_meal_name"),
    )

    fridge = relationship("Fridge", back_populates="fridge_meals")
    ingredients = relationship(
        "FridgeMealIngredient",
        back_populates="fridge_meal",
        cascade="all, delete-orphan",
    )


class FridgeProduct(Base):
    __tablename__ = "fridge_products"
    id = Column(Integer, primary_key=True, index=True)
    fridge_id = Column(
        Integer,
        ForeignKey("fridges.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    product_name = Column(String, index=True, nullable=False)
    calories_100g = Column(Float, nullable=False, default=0)
    proteins_100g = Column(Float, nullable=False, default=0)
    fats_100g = Column(Float, nullable=False, default=0)
    carbs_100g = Column(Float, nullable=False, default=0)
    category = Column(SqlEnum(FoodCategory, index=True, name="food_category"))
    is_favourite = Column(Boolean, index=True, nullable=False, default=False)
    __table_args__ = (
        UniqueConstraint("fridge_id", "product_name", name="un_fridge_product_name"),
    )

    fridge = relationship("Fridge", back_populates="fridge_products")
    fridge_meal_ingredient = relationship(
        "FridgeMealIngredient",
        back_populates="fridge_product",
        cascade="all, delete-orphan",
    )


class FridgeMealIngredient(Base):
    __tablename__ = "fridge_meal_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, nullable=False)
    fridge_meal_id = Column(
        Integer,
        ForeignKey("fridge_meals.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    fridge_product_id = Column(
        Integer, ForeignKey("fridge_products.id", ondelete="CASCADE"), nullable=False
    )

    fridge_meal = relationship("FridgeMeal", back_populates="ingredients")
    fridge_product = relationship(
        "FridgeProduct", back_populates="fridge_meal_ingredient"
    )
