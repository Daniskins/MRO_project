import pytest
from pydantic import ValidationError

from app.schemas.maintenance_type import MaintenanceTypeCreate, MaintenanceTypeUpdate


def valid_type_payload(**overrides) -> dict:
    payload = {
        "name": "ТО-1",
        "interval_hours": 50,
        "interval_days": 90,
        "description": "Регламентное обслуживание после 50 часов наработки"
    }
    payload.update(overrides)
    return payload


def test_maintenance_type_create_valid_ok():
    obj = MaintenanceTypeCreate(**valid_type_payload())
    assert obj.name == 'ТО-1'
    assert obj.interval_hours == 50
    assert obj.interval_days == 90


def test_maintenance_type_create_only_interval_hours_ok():
    payload = valid_type_payload()
    payload.pop('interval_days')
    obj = MaintenanceTypeCreate(**payload)
    assert obj.interval_days is None


def test_maintenance_type_create_missing_both_intervals_raises_validation_error():
    payload = valid_type_payload()
    payload.pop('interval_hours')
    payload.pop('interval_days')
    with pytest.raises(ValidationError):
        MaintenanceTypeCreate(**payload)


def test_maintenance_type_create_empty_name_raises_validation_error():
    payload = valid_type_payload(name='')
    with pytest.raises(ValidationError):
        MaintenanceTypeCreate(**payload)


def test_maintenance_type_update_empty_payload_ok():
    obj = MaintenanceTypeUpdate()
    assert obj.model_dump(exclude_unset=True) == {}
