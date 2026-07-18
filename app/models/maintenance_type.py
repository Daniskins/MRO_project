from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from app.models.base import Base


class MaintenanceType(Base):
    """Справочник видов ТО и их регламентной периодичности."""

    name: Mapped[str] = mapped_column(String(100), unique=True)  # Например, ТО-1, ТО-2, Регламент 50ч
    interval_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Периодичность по наработке, ч
    interval_days: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Периодичность по календарю, дн.
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
