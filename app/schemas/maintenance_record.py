from datetime import date
from typing import Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict


class MaintenanceRecordBase(BaseModel):
    uav_id: Annotated[int, Field(gt=0, description='ID БПЛА')]
    maintenance_type_id: Annotated[Optional[int], Field(gt=0, description='ID вида ТО (справочник)')] = None
    performed_at: Annotated[date, Field(description='Дата выполнения ТО')]
    operating_time_at_maintenance: Annotated[int, Field(ge=0, le=50000, description='Наработка БПЛА на момент ТО, часы')]
    performed_by: Annotated[Optional[str], Field(max_length=100, description='Кто выполнил ТО')] = None
    description: Annotated[Optional[str], Field(max_length=255, description='Описание выполненных работ')] = None
    # Если не заданы явно — рассчитываются автоматически из интервалов MaintenanceType
    next_due_operating_time: Annotated[Optional[int], Field(ge=0, le=50000, description='Следующее ТО по наработке, часы')] = None
    next_due_date: Annotated[Optional[date], Field(description='Следующее ТО по календарю')] = None


class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass


class MaintenanceRecordUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    maintenance_type_id: Annotated[Optional[int], Field(gt=0, description='ID вида ТО (справочник)')] = None
    performed_at: Annotated[Optional[date], Field(description='Дата выполнения ТО')] = None
    operating_time_at_maintenance: Annotated[Optional[int], Field(ge=0, le=50000, description='Наработка БПЛА на момент ТО, часы')] = None
    performed_by: Annotated[Optional[str], Field(max_length=100, description='Кто выполнил ТО')] = None
    description: Annotated[Optional[str], Field(max_length=255, description='Описание выполненных работ')] = None
    next_due_operating_time: Annotated[Optional[int], Field(ge=0, le=50000, description='Следующее ТО по наработке, часы')] = None
    next_due_date: Annotated[Optional[date], Field(description='Следующее ТО по календарю')] = None


class MaintenanceRecordRead(MaintenanceRecordBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
