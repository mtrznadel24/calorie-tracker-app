from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, Integer, String
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
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    height = Column(Float)
    age = Column(Integer)
    gender = Column(SqlEnum(Gender, name="gender"))
    activity_level = Column(Float)

    fridge = relationship(
        "Fridge", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")
    weights = relationship(
        "Weight", back_populates="user", cascade="all, delete-orphan"
    )
    measurements = relationship(
        "Measurement", back_populates="user", cascade="all, delete-orphan"
    )
