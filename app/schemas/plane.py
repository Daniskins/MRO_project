from datetime import date
from pydantic import BaseModel, Field


class PlaneBase(BaseModel):
    type_plane: str = Field(..., min_length=1,max_length=10, description='Тип самолета', example='Су-57')
    serial_number: str =  Field(..., min_length=1, max_length=32, description='Серийный номер самолета')
    tail_number: str = Field(min_lenght=1, max_length=32, description='Номер борта')
    base_airfield: str = Field(..., min_length=1, max_length=100, description='Место базирования самолета')
    belong_plane: str = Field(..., min_length=1, max_length=100, description='Принадлежность самолета')
    operating_time: int = Field(..., ge=0, le=50000, description='Время эксплуатации самолета')
    manufacturer_date: date | None = Field(description='Дата производства самолета')

class PlaneCreate(PlaneBase):
    pass

class PlaneUpdate(PlaneBase):
    pass

class PlaneRead(PlaneBase):
    id: int