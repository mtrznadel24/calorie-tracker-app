from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from app.core.db import Base


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    height = Column(Float)
    age = Column(Integer)
    gender = Column(SqlEnum(Gender, name="gender"))
    activity_level = Column(Float)
    target_weekly_gain = Column(Float, default=0, nullable=False)

    fridge = relationship(
        "Fridge",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )
    meal_logs = relationship(
        "MealLog", back_populates="user", cascade="all, delete-orphan"
    )
    weights = relationship(
        "Weight", back_populates="user", cascade="all, delete-orphan"
    )
    measurements = relationship(
        "Measurement", back_populates="user", cascade="all, delete-orphan"
    )
