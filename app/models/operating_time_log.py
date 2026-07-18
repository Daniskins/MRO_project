from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date, Float, ForeignKey, Integer, String

from app.models.base import Base


class OperatingTimeLog(Base):
    """Запись о наработке БПЛА за один вылет/сессию."""

    uav_id: Mapped[int] = mapped_column(ForeignKey("uavs.id", ondelete="CASCADE"))
    flight_date: Mapped[date] = mapped_column(Date)
    duration_hours: Mapped[float] = mapped_column(Float)  # Наработка за вылет, часы
    cycles: Mapped[int] = mapped_column(Integer, default=1, server_default="1")  # Кол-во взлётов/посадок
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
