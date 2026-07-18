from datetime import date
from typing import Literal, Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict

UavStatus = Literal["active", "in_maintenance", "decommissioned"]


class UavBase(BaseModel):
    uav_model: Annotated[str, Field(min_length=1, max_length=50, description='Модель БПЛА', examples=['Орлан-10',
                                                                                                        'ZALA 421-16E'])]
    serial_number: Annotated[str, Field(min_length=1, max_length=32, description='Серийный номер БПЛА')]
    tail_number: Annotated[str, Field(min_length=1, max_length=32, description='Бортовой номер')] = '001'
    base_location: Annotated[str, Field(min_length=1, max_length=100, description='Место базирования / пункт управления')]
    operator: Annotated[str, Field(min_length=1, max_length=100, description='Эксплуатант (принадлежность)')]
    status: Annotated[UavStatus, Field(description='Текущий статус БПЛА')] = 'active'
    total_operating_time: Annotated[int, Field(ge=0, le=50000, description='Суммарная наработка БПЛА, часы')] = 0
    manufacture_date: Annotated[date | None, Field(description='Дата выпуска БПЛА')] = None


class UavCreate(UavBase):
    pass


class UavUpdate(UavBase):
    model_config = ConfigDict(populate_by_name=True)

    uav_model: Annotated[
        Optional[str],
        Field(min_length=1, max_length=50, description='Модель БПЛА', examples=['Орлан-10', 'ZALA 421-16E'])] = None
    serial_number: Annotated[
        Optional[str],
        Field(min_length=1, max_length=32, description='Серийный номер БПЛА')] = None
    tail_number: Annotated[
        Optional[str],
        Field(min_length=1, max_length=32, description='Бортовой номер')] = None
    base_location: Annotated[
        Optional[str],
        Field(min_length=1, max_length=100, description='Место базирования / пункт управления')] = None
    operator: Annotated[
        Optional[str],
        Field(min_length=1, max_length=100, description='Эксплуатант (принадлежность)')] = None
    status: Annotated[
        Optional[UavStatus],
        Field(description='Текущий статус БПЛА')] = None
    total_operating_time: Annotated[
        Optional[int],
        Field(ge=0, le=50000, description='Суммарная наработка БПЛА, часы')] = None
    manufacture_date: Annotated[
        Optional[date],
        Field(description='Дата выпуска БПЛА')] = None


class UavRead(UavBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
