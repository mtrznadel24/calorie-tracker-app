from enum import Enum

from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
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


class MealLog(Base):
    __tablename__ = "meal_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    date = Column(Date, index=True, nullable=False)
    type = Column(SqlEnum(MealType, name="meal_type"), index=True, nullable=False)
    weight = Column(Float, nullable=False)
    name = Column(String, index=True, nullable=False)
    calories = Column(Float, nullable=False, default=0)
    proteins = Column(Float, nullable=False, default=0)
    fats = Column(Float, nullable=False, default=0)
    carbs = Column(Float, nullable=False, default=0)

    user = relationship("User", back_populates="meal_logs")
