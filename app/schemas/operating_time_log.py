from datetime import date
from typing import Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict


class OperatingTimeLogBase(BaseModel):
    uav_id: Annotated[int, Field(gt=0, description='ID БПЛА')]
    flight_date: Annotated[date, Field(description='Дата вылета')]
    duration_hours: Annotated[float, Field(gt=0, le=48, description='Наработка за вылет, часы')]
    cycles: Annotated[int, Field(ge=1, le=100, description='Количество взлётов/посадок')] = 1
    notes: Annotated[str | None, Field(max_length=255, description='Примечание')] = None


class OperatingTimeLogCreate(OperatingTimeLogBase):
    pass


class OperatingTimeLogUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    flight_date: Annotated[Optional[date], Field(description='Дата вылета')] = None
    duration_hours: Annotated[Optional[float], Field(gt=0, le=48, description='Наработка за вылет, часы')] = None
    cycles: Annotated[Optional[int], Field(ge=1, le=100, description='Количество взлётов/посадок')] = None
    notes: Annotated[Optional[str], Field(max_length=255, description='Примечание')] = None


class OperatingTimeLogRead(OperatingTimeLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
