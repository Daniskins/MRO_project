from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Integer

from app.core.models.base import Base

class Plane(Base):
    type_plane: Mapped[str] = mapped_column(String(10)) #Например, Су-57, Су-35 или Суперджет
    serial_number: Mapped[str] = mapped_column(String(32), unique=True)
    tail_number: Mapped[str] = mapped_column(String(32), unique=True)
    base_airfield: Mapped[str] = mapped_column(String(100)) #Например, Алжир, Уфа или Москва
    belong_plane: Mapped[str] = mapped_column(String(100)) #Например, Аэрофлот или Ростех
    operating_time: Mapped[int] = mapped_column(Integer)
    manufacturer_date: Mapped[datetime | None] = mapped_column(Date, nullable=False) #Дата выпуска самолета