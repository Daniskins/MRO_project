import pytest
from pydantic import ValidationError

from app.schemas.uav import UavCreate, UavUpdate, UavRead


def valid_uav_payload(**overrides) -> dict:
    """
    Базовый валидный датасет для UavCreate.
    Можно переопределять значения через overrides.
    """
    payload = {
        "uav_model": "Орлан-10",
        "serial_number": "900900123456789",
        "tail_number": "001",
        "base_location": "в/ч 77984",
        "operator": "ВКС РФ",
        "status": "active",
        "total_operating_time": 1000,
        "manufacture_date": "2022-01-01"
    }
    payload.update(overrides)
    return payload


# Тесты для UavCreate/UavBase

def test_uav_create_valid_ok():
    """Проверка создания UavCreate с валидными данными."""
    payload = valid_uav_payload()
    obj = UavCreate(**payload)
    assert obj.uav_model == 'Орлан-10'
    assert obj.serial_number == '900900123456789'
    assert obj.tail_number == '001'
    assert obj.base_location == 'в/ч 77984'
    assert obj.operator == 'ВКС РФ'
    assert obj.status == 'active'
    assert obj.total_operating_time == 1000
    assert obj.manufacture_date.isoformat() == '2022-01-01'


def test_uav_create_missing_tail_number_default_when_omitted():
    """Проверка значения по умолчанию для tail_number при его отсутствии."""
    payload = valid_uav_payload()
    payload.pop('tail_number')
    obj = UavCreate(**payload)
    assert obj.tail_number == '001'  # Значение по умолчанию


def test_uav_create_missing_status_and_operating_time_defaults_when_omitted():
    """Проверка значений по умолчанию для status и total_operating_time."""
    payload = valid_uav_payload()
    payload.pop('status')
    payload.pop('total_operating_time')
    obj = UavCreate(**payload)
    assert obj.status == 'active'
    assert obj.total_operating_time == 0


@pytest.mark.parametrize('field_name', [
    'uav_model',
    'serial_number',
    'base_location',
    'operator'
])
def test_uav_create_missing_required_field_raises_validation_error(field_name):
    """Проверка ошибки валидации при отсутствии обязательных полей."""
    payload = valid_uav_payload()
    payload.pop(field_name)
    with pytest.raises(ValidationError):
        UavCreate(**payload)


@pytest.mark.parametrize('field_name', [
    'uav_model',
    'serial_number',
    'base_location',
    'operator'
])
def test_uav_create_empty_string_raises_validation_error(field_name):
    """Проверка ошибки валидации при пустой строке в обязательных полях."""
    payload = valid_uav_payload(**{field_name: ''})
    with pytest.raises(ValidationError):
        UavCreate(**payload)


def test_uav_create_uav_model_too_long_raises_validation_error():
    """Проверка ошибки валидации при слишком длинном uav_model."""
    payload = valid_uav_payload(uav_model='X' * 51)  # Длина 51, превышает максимум 50
    with pytest.raises(ValidationError):
        UavCreate(**payload)


def test_uav_create_serial_number_too_long_raises_validation_error():
    """Проверка ошибки валидации при слишком длинном serial_number."""
    payload = valid_uav_payload(serial_number='X' * 33)  # Длина 33, превышает максимум 32
    with pytest.raises(ValidationError):
        UavCreate(**payload)


def test_uav_create_operating_time_negative_raises_validation_error():
    """Проверка ошибки валидации при отрицательном total_operating_time."""
    payload = valid_uav_payload(total_operating_time=-1)
    with pytest.raises(ValidationError):
        UavCreate(**payload)


def test_uav_create_operating_time_too_large_raises_validation_error():
    """Проверка ошибки валидации при слишком большом total_operating_time."""
    payload = valid_uav_payload(total_operating_time=50001)  # Превышает максимум 50000
    with pytest.raises(ValidationError):
        UavCreate(**payload)


def test_uav_create_invalid_status_raises_validation_error():
    """Проверка ошибки валидации при недопустимом значении status."""
    payload = valid_uav_payload(status='flying')
    with pytest.raises(ValidationError):
        UavCreate(**payload)


def test_uav_create_manufacture_date_none_ok():
    """Проверка создания UavCreate с manufacture_date=None."""
    payload = valid_uav_payload(manufacture_date=None)
    obj = UavCreate(**payload)
    assert obj.manufacture_date is None


def test_uav_create_invalid_manufacture_date_raises_validation_error():
    """Проверка ошибки валидации при неверном формате manufacture_date."""
    payload = valid_uav_payload(manufacture_date='invalid-date')
    with pytest.raises(ValidationError):
        UavCreate(**payload)


# Тесты для UavUpdate

def test_uav_update_empty_payload_ok():
    """Проверка создания UavUpdate с пустым payload."""
    obj = UavUpdate()
    assert obj.model_dump(exclude_unset=True) == {}


def test_uav_update_partial_fields_ok():
    """Проверка создания UavUpdate с частичными полями."""
    payload = {
        "uav_model": "ZALA 421-16E",
        "total_operating_time": 3500
    }
    obj = UavUpdate(**payload)
    assert obj.uav_model == 'ZALA 421-16E'
    assert obj.total_operating_time == 3500
    assert obj.serial_number is None
    assert obj.tail_number is None
    assert obj.base_location is None
    assert obj.operator is None
    assert obj.status is None
    assert obj.manufacture_date is None


@pytest.mark.parametrize('field_name', [
    'uav_model',
    'serial_number',
    'base_location',
    'operator'
])
def test_uav_update_empty_string_raises_validation_error(field_name):
    """Проверка ошибки валидации при пустой строке в обновлении для текстовых полей."""
    payload = {field_name: ''}
    with pytest.raises(ValidationError):
        UavUpdate(**payload)


def test_uav_update_operating_time_limits():
    """Проверка границ для total_operating_time в UavUpdate."""

    # Минимальное значение
    payload_min = {"total_operating_time": 0}
    obj_min = UavUpdate(**payload_min)
    with pytest.raises(ValidationError):
        UavUpdate(**{"total_operating_time": -1})
    assert obj_min.total_operating_time == 0

    # Максимальное значение
    payload_max = {"total_operating_time": 50000}
    obj_max = UavUpdate(**payload_max)
    with pytest.raises(ValidationError):
        UavUpdate(**{"total_operating_time": 50001})
    assert obj_max.total_operating_time == 50000


def test_uav_update_invalid_manufacture_date_raises_validation_error():
    """Проверка ошибки валидации при неверном формате manufacture_date в UavUpdate."""
    payload = {"manufacture_date": "invalid-date"}
    with pytest.raises(ValidationError):
        UavUpdate(**payload)


# Тесты для UavRead

def test_uav_read_missing_id_raises_validation_error():
    """Проверка создания UavRead с валидными данными без id."""
    payload = valid_uav_payload()
    with pytest.raises(ValidationError):
        # UavRead требует поле id, его отсутствие должно вызвать ошибку
        UavRead.model_validate(payload)


def test_uav_read_ok_with_id():
    """Проверка создания UavRead с валидными данными и id."""
    payload = valid_uav_payload()
    payload['id'] = 1
    obj = UavRead.model_validate(payload)
    assert obj.id == 1
    assert obj.uav_model == 'Орлан-10'
    assert obj.serial_number == '900900123456789'
    assert obj.tail_number == '001'
    assert obj.base_location == 'в/ч 77984'
    assert obj.operator == 'ВКС РФ'
    assert obj.status == 'active'
    assert obj.total_operating_time == 1000
    assert obj.manufacture_date.isoformat() == '2022-01-01'
