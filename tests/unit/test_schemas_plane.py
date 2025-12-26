import pytest
from pydantic import ValidationError

from app.schemas.plane import PlaneCreate, PlaneUpdate, PlaneRead


def valid_plane_payload(**overrides) -> dict:
    """
    Базовый валидный датасет для PlaneCreate.
    Можно переопределять значения через overrides.
    """
    payload = {
        "type_plane": "Су-57",
        "serial_number": "900900123456789",
        "tail_number": "001",
        "base_airfield": "в/ч 77984",
        "belong_plane": "ВКС РФ",
        "operating_time": 1000,
        "manufacturer_date": "2022-01-01"
    }
    payload.update(overrides)
    return payload


# Тесты для PlaneCreate/PlaneBase

def test_plane_create_valid_ok():
    """Проверка создания PlaneCreate с валидными данными."""
    payload = valid_plane_payload()
    obj= PlaneCreate(**payload)
    assert obj.type_plane == 'Су-57'
    assert obj.serial_number == '900900123456789'
    assert obj.tail_number == '001'
    assert obj.base_airfield == 'в/ч 77984'
    assert obj.belong_plane == 'ВКС РФ'
    assert obj.operating_time == 1000
    assert obj.manufacturer_date.isoformat() == '2022-01-01'


def test_plane_create_missing_tail_number_default_when_omitted():
    """Проверка значения по умолчанию для tail_number при его отсутствии."""
    payload = valid_plane_payload()
    payload.pop('tail_number')
    obj = PlaneCreate(**payload)
    assert obj.tail_number == '001'  # Значение по умолчанию


@pytest.mark.parametrize('field_name',[
    'type_plane',
    'serial_number',
    'base_airfield',
    'belong_plane'
])
def test_plane_create_missing_required_field_raises_validation_error(field_name):
    """Проверка ошибки валидации при отсутствии обязательных полей."""
    payload = valid_plane_payload()
    payload.pop(field_name)
    with pytest.raises(ValidationError):
        PlaneCreate(**payload)


@pytest.mark.parametrize('field_name', [
    'type_plane',
    'serial_number',
    'base_airfield',
    'belong_plane'
])
def test_plane_create_empty_string_raises_validation_error(field_name):
    """Проверка ошибки валидации при пустой строке в обязательных полях."""
    payload = valid_plane_payload(**{field_name: ''})
    with pytest.raises(ValidationError):
        PlaneCreate(**payload)


def test_plane_create_type_plane_too_long_raises_validation_error():
    """Проверка ошибки валидации при слишком длинном type_plane."""
    payload = valid_plane_payload(type_plane='X' * 11)  # Длина 11, превышает максимум 10
    with pytest.raises(ValidationError):
        PlaneCreate(**payload)


def test_plane_create_serial_number_too_long_raises_validation_error():
    """Проверка ошибки валидации при слишком длинном serial_number."""
    payload = valid_plane_payload(serial_number='X' * 33)  # Длина 33, превышает максимум 32
    with pytest.raises(ValidationError):
        PlaneCreate(**payload)


def test_plane_create_operating_time_negative_raises_validation_error():
    """Проверка ошибки валидации при отрицательном operating_time."""
    payload = valid_plane_payload(operating_time=-1)
    with pytest.raises(ValidationError):
        PlaneCreate(**payload)


def test_plane_create_operating_time_too_large_raises_validation_error():
    """Проверка ошибки валидации при слишком большом operating_time."""
    payload = valid_plane_payload(operating_time=50001)   # Превышает максимум 50000
    with pytest.raises(ValidationError):
        PlaneCreate(**payload)


def test_plane_create_manufacturer_date_none_ok():
    """Проверка создания PlaneCreate с manufacturer_date=None."""
    payload = valid_plane_payload(manufacturer_date=None)
    obj = PlaneCreate(**payload)
    assert obj.manufacturer_date is None


def test_plane_create_invalid_manufacturer_date_raises_validation_error():
    """Проверка ошибки валидации при неверном формате manufacturer_date."""
    payload = valid_plane_payload(manufacturer_date='invalid-date')
    with pytest.raises(ValidationError):
        PlaneCreate(**payload)


# Тесты для PlaneUpdate

def test_plane_update_empty_payload_ok():
    """Проверка создания PlaneUpdate с пустым payload."""
    obj = PlaneUpdate()
    assert obj.model_dump(exclude_unset=True) == {}


def test_plane_update_partial_fields_ok():
    """Проверка создания PlaneUpdate с частичными полями."""
    payload = {
        "type_plane": "Су-30МКИ",
        "operating_time": 3500
    }
    obj = PlaneUpdate(**payload)
    assert obj.type_plane == 'Су-30МКИ'
    assert obj.operating_time == 3500
    assert obj.serial_number is None
    assert obj.tail_number is None
    assert obj.base_airfield is None
    assert obj.belong_plane is None
    assert obj.manufacturer_date is None


@pytest.mark.parametrize('field_name', [
    'type_plane',
    'serial_number',
    'base_airfield',
    'belong_plane'
])
def test_plane_update_empty_string_raises_validation_error(field_name):
    """Проверка ошибки валидации при пустой строке в обновлении для текстовых полей."""
    payload = {field_name: ''}
    with pytest.raises(ValidationError):
        PlaneUpdate(**payload)


def test_plane_update_operating_time_limits():
    """Проверка границ для operating_time в PlaneUpdate."""

    # Минимальное значение
    payload_min = {"operating_time": 0}
    obj_min = PlaneUpdate(**payload_min)
    with pytest.raises(ValidationError):
        PlaneUpdate(**{"operating_time": -1})
    assert obj_min.operating_time == 0

    # Максимальное значение
    payload_max = {"operating_time": 50000}
    obj_max = PlaneUpdate(**payload_max)
    with pytest.raises(ValidationError):
        PlaneUpdate(**{"operating_time": 50001})
    assert obj_max.operating_time == 50000


def test_plane_update_invalid_manufacturer_date_raises_validation_error():
    """Проверка ошибки валидации при неверном формате manufacturer_date в PlaneUpdate."""
    payload = {"manufacturer_date": "invalid-date"}
    with pytest.raises(ValidationError):
        PlaneUpdate(**payload)


# Тесты для PlaneRead

def test_plane_read_ok():
    """Проверка создания PlaneRead с валидными данными."""
    payload = valid_plane_payload()
    with pytest.raises(ValidationError):
        # PlaneRead требует поле id, его отсутствие должно вызвать ошибку
        PlaneRead.model_validate(payload)

def test_plane_read_ok_with_id():
    """Проверка создания PlaneRead с валидными данными и id."""
    payload = valid_plane_payload()
    payload['id'] = 1
    obj = PlaneRead.model_validate(payload)
    assert obj.id == 1
    assert obj.type_plane == 'Су-57'
    assert obj.serial_number == '900900123456789'
    assert obj.tail_number == '001'
    assert obj.base_airfield == 'в/ч 77984'
    assert obj.belong_plane == 'ВКС РФ'
    assert obj.operating_time == 1000
    assert obj.manufacturer_date.isoformat() == '2022-01-01'