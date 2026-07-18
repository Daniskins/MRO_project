import pytest
from pydantic import ValidationError

from app.schemas.operating_time_log import OperatingTimeLogCreate, OperatingTimeLogUpdate


def valid_log_payload(**overrides) -> dict:
    payload = {
        "uav_id": 1,
        "flight_date": "2026-07-01",
        "duration_hours": 2.5,
        "cycles": 1,
        "notes": "Плановый облёт"
    }
    payload.update(overrides)
    return payload


def test_operating_time_log_create_valid_ok():
    obj = OperatingTimeLogCreate(**valid_log_payload())
    assert obj.uav_id == 1
    assert obj.duration_hours == 2.5
    assert obj.cycles == 1


def test_operating_time_log_create_default_cycles_ok():
    payload = valid_log_payload()
    payload.pop('cycles')
    obj = OperatingTimeLogCreate(**payload)
    assert obj.cycles == 1


def test_operating_time_log_create_zero_duration_raises_validation_error():
    payload = valid_log_payload(duration_hours=0)
    with pytest.raises(ValidationError):
        OperatingTimeLogCreate(**payload)


def test_operating_time_log_create_duration_too_large_raises_validation_error():
    payload = valid_log_payload(duration_hours=49)
    with pytest.raises(ValidationError):
        OperatingTimeLogCreate(**payload)


def test_operating_time_log_create_invalid_uav_id_raises_validation_error():
    payload = valid_log_payload(uav_id=0)
    with pytest.raises(ValidationError):
        OperatingTimeLogCreate(**payload)


def test_operating_time_log_update_empty_payload_ok():
    obj = OperatingTimeLogUpdate()
    assert obj.model_dump(exclude_unset=True) == {}


def test_operating_time_log_update_partial_fields_ok():
    obj = OperatingTimeLogUpdate(duration_hours=3.0)
    assert obj.duration_hours == 3.0
    assert obj.flight_date is None
