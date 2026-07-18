from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date, ForeignKey, Integer, String

from app.models.base import Base


class MaintenanceRecord(Base):
    """Фактически выполненное ТО по конкретному БПЛА."""

    uav_id: Mapped[int] = mapped_column(ForeignKey("uavs.id", ondelete="CASCADE"))
    maintenance_type_id: Mapped[int | None] = mapped_column(
        ForeignKey("maintenance_types.id", ondelete="SET NULL"), nullable=True
    )
    performed_at: Mapped[date] = mapped_column(Date)
    operating_time_at_maintenance: Mapped[int] = mapped_column(Integer)  # Наработка БПЛА на момент ТО, ч
    performed_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    next_due_operating_time: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Следующее ТО по наработке
    next_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)  # Следующее ТО по календарю
