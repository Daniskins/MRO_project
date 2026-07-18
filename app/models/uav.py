from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Integer

from app.models.base import Base


class Uav(Base):
    uav_model: Mapped[str] = mapped_column(String(50))  # Например, Орлан-10, ZALA 421-16E, Суперкам S350
    serial_number: Mapped[str] = mapped_column(String(32), unique=True)
    tail_number: Mapped[str] = mapped_column(String(32), unique=True)
    base_location: Mapped[str] = mapped_column(String(100))  # Пункт базирования / управления
    operator: Mapped[str] = mapped_column(String(100))  # Эксплуатант (принадлежность)
    status: Mapped[str] = mapped_column(String(20), default="active", server_default="active")
    total_operating_time: Mapped[int] = mapped_column(Integer, default=0, server_default="0")  # Суммарная наработка, ч
    manufacture_date: Mapped[date | None] = mapped_column(Date, nullable=True)  # Дата выпуска БПЛА
