import pytest
from pydantic import ValidationError

from app.schemas.maintenance_record import MaintenanceRecordCreate, MaintenanceRecordUpdate


def valid_record_payload(**overrides) -> dict:
    payload = {
        "uav_id": 1,
        "maintenance_type_id": 1,
        "performed_at": "2026-07-01",
        "operating_time_at_maintenance": 50,
        "performed_by": "Иванов И.И.",
        "description": "Замена аккумулятора",
    }
    payload.update(overrides)
    return payload


def test_maintenance_record_create_valid_ok():
    obj = MaintenanceRecordCreate(**valid_record_payload())
    assert obj.uav_id == 1
    assert obj.maintenance_type_id == 1
    assert obj.operating_time_at_maintenance == 50
    assert obj.next_due_operating_time is None
    assert obj.next_due_date is None


def test_maintenance_record_create_without_maintenance_type_ok():
    payload = valid_record_payload()
    payload.pop('maintenance_type_id')
    obj = MaintenanceRecordCreate(**payload)
    assert obj.maintenance_type_id is None


def test_maintenance_record_create_explicit_next_due_ok():
    payload = valid_record_payload(next_due_operating_time=100, next_due_date="2026-10-01")
    obj = MaintenanceRecordCreate(**payload)
    assert obj.next_due_operating_time == 100
    assert obj.next_due_date.isoformat() == "2026-10-01"


def test_maintenance_record_create_negative_operating_time_raises_validation_error():
    payload = valid_record_payload(operating_time_at_maintenance=-1)
    with pytest.raises(ValidationError):
        MaintenanceRecordCreate(**payload)


def test_maintenance_record_update_empty_payload_ok():
    obj = MaintenanceRecordUpdate()
    assert obj.model_dump(exclude_unset=True) == {}
