from datetime import date
from typing import Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict


class PlaneBase(BaseModel):
    type_plane: Annotated[str, Field(min_length=1,max_length=10, description='Тип самолета', examples=['Су-57',
                                                                                                       'Су-35'])]
    serial_number: Annotated[str, Field(min_length=1, max_length=32, description='Серийный номер самолета')]
    tail_number: Annotated[str, Field(min_length=1, max_length=32, description='Номер борта')] = '001'
    base_airfield: Annotated[str, Field(min_length=1, max_length=100, description='Место базирования самолета')]
    belong_plane: Annotated[str, Field(min_length=1, max_length=100, description='Принадлежность самолета')]
    operating_time: Annotated[int, Field(ge=0, le=50000, description='Время эксплуатации самолета')]
    manufacturer_date: Annotated[date | None, Field(description='Дата производства самолета')] = None

class PlaneCreate(PlaneBase):
    pass

class PlaneUpdate(PlaneBase):
    model_config = ConfigDict(populate_by_name=True)

    type_plane: Annotated[
        Optional[str],
        Field(min_length=1, max_length=10, description='Тип самолета', examples=['Су-57', 'Су-35'])] = None
    serial_number: Annotated[
        Optional[str],
        Field(min_length=1, max_length=32, description='Серийный номер самолета')] = None
    tail_number: Annotated[
        Optional[str],
        Field(min_length=1, max_length=32, description='Номер борта')] = None
    base_airfield: Annotated[
        Optional[str],
        Field(min_length=1, max_length=100, description='Место базирования самолета')] = None
    belong_plane: Annotated[
        Optional[str],
        Field(min_length=1, max_length=100, description='Принадлежность самолета')] = None
    operating_time: Annotated[
        Optional[int],
        Field(ge=0, le=50000, description='Время эксплуатации самолета')] = None
    manufacturer_date: Annotated[
        Optional[date],
        Field(description='Дата производства самолета')] = None

class PlaneRead(PlaneBase):
    model_config = ConfigDict(from_attributes=True)

    id: int