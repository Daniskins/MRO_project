from typing import Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict, model_validator


class MaintenanceTypeBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100, description='Название вида ТО', examples=['ТО-1', 'ТО-2'])]
    interval_hours: Annotated[Optional[int], Field(ge=1, le=50000, description='Периодичность по наработке, часы')] = None
    interval_days: Annotated[Optional[int], Field(ge=1, le=3650, description='Периодичность по календарю, дни')] = None
    description: Annotated[Optional[str], Field(max_length=255, description='Описание')] = None

    @model_validator(mode='after')
    def check_interval_present(self) -> 'MaintenanceTypeBase':
        if self.interval_hours is None and self.interval_days is None:
            raise ValueError('Нужно указать хотя бы одну периодичность: interval_hours или interval_days')
        return self


class MaintenanceTypeCreate(MaintenanceTypeBase):
    pass


class MaintenanceTypeUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: Annotated[Optional[str], Field(min_length=1, max_length=100, description='Название вида ТО')] = None
    interval_hours: Annotated[Optional[int], Field(ge=1, le=50000, description='Периодичность по наработке, часы')] = None
    interval_days: Annotated[Optional[int], Field(ge=1, le=3650, description='Периодичность по календарю, дни')] = None
    description: Annotated[Optional[str], Field(max_length=255, description='Описание')] = None


class MaintenanceTypeRead(MaintenanceTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
