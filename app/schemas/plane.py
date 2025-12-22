from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class PlaneBase(BaseModel):
    type_plane: str = Field(..., min_length=1,max_length=10, description='Тип самолета', example='Су-57')
    serial_number: str =  Field(..., min_length=1, max_length=32, description='Серийный номер самолета')
    tail_number: str = Field('001', min_length=1, max_length=32, description='Номер борта')
    base_airfield: str = Field(..., min_length=1, max_length=100, description='Место базирования самолета')
    belong_plane: str = Field(..., min_length=1, max_length=100, description='Принадлежность самолета')
    operating_time: int = Field(..., ge=0, le=50000, description='Время эксплуатации самолета')
    manufacturer_date: date | None = Field(description='Дата производства самолета', default=None)

class PlaneCreate(PlaneBase):
    pass

class PlaneUpdate(PlaneBase):
    model_config = ConfigDict(populate_by_name=True)

    type_plane: Optional[str] = Field(None, min_length=1, max_length=10, description='Тип самолета', example='Су-57')
    serial_number: Optional[str] = Field(None, min_length=1, max_length=32, description='Серийный номер самолета')
    tail_number: Optional[str] = Field(None, min_length=1, max_length=32, description='Номер борта')
    base_airfield: Optional[str] = Field(None, min_length=1, max_length=100, description='Место базирования самолета')
    belong_plane: Optional[str] = Field(None, min_length=1, max_length=100, description='Принадлежность самолета')
    operating_time: Optional[int] = Field(None, ge=0, le=50000, description='Время эксплуатации самолета')
    manufacturer_date: Optional[date] = Field(default=None, description='Дата производства самолета')

class PlaneRead(PlaneBase):
    model_config = ConfigDict(from_attributes=True)

    id: int