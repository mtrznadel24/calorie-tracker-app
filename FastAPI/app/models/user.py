from enum import Enum
from datetime import date, datetime, timezone

from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    Boolean,
    Enum as SqlEnum, DateTime
)
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
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

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


class Weight(Base):
    __tablename__ = "weights"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    date = Column(Date, default=date.today, index=True, nullable=False)
    weight = Column(Float, nullable=False)
    __table_args__ = (UniqueConstraint("user_id", "date", name="weight_user_date_uc"),)

    user = relationship("User", back_populates="weights")


class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    date = Column(Date, default=date.today, index=True, nullable=False)
    weight_id = Column(
        Integer, ForeignKey("weights.id", ondelete="SET NULL"), nullable=True
    )
    neck = Column(Float)
    biceps = Column(Float)
    chest = Column(Float)
    waist = Column(Float)
    hips = Column(Float)
    thighs = Column(Float)
    calves = Column(Float)
    __table_args__ = (
        UniqueConstraint("user_id", "date", name="measurement_user_date_uc"),
    )

    user = relationship("User", back_populates="measurements")
