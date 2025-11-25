from datetime import date

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.db import Base


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
    measurements = relationship("Measurement", back_populates="weight")


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
    weight = relationship("Weight", back_populates="measurements", lazy="joined")
