import unittest
from datetime import date
from pydantic import ValidationError
from app.schemas.plane import PlaneBase


class TestPlaneBase(unittest.TestCase):

    def test_valid_plane_base(self):
        data = {
            "type_plane": "Су-57",
            "serial_number": "SN123456789",
            "tail_number": "TN987654321",
            "base_airfield": "Аэродром №1",
            "belong_plane": "ВВС России",
            "operating_time": 15000,
            "manufacturer_date": date(2020, 5, 15)
        }
        plane = PlaneBase(**data)
        self.assertEqual(plane.type_plane, "Су-57")
        self.assertEqual(plane.serial_number, "SN123456789")
        self.assertEqual(plane.tail_number, "TN987654321")
        self.assertEqual(plane.base_airfield, "Аэродром №1")
        self.assertEqual(plane.belong_plane, "ВВС России")
        self.assertEqual(plane.operating_time, 15000)
        self.assertEqual(plane.manufacturer_date, date(2020, 5, 15))

    def test_missing_required_fields(self):
        with self.assertRaises(ValidationError):
            PlaneBase(
                serial_number="SN123456789",
                tail_number="TN987654321",
                base_airfield="Аэродром №1",
                belong_plane="ВВС России",
                operating_time=15000
            )

    def test_type_plane_too_short(self):
        with self.assertRaises(ValidationError):
            PlaneBase(
                type_plane="",
                serial_number="SN123456789",
                tail_number="TN987654321",
                base_airfield="Аэродром №1",
                belong_plane="ВВС России",
                operating_time=15000
            )

    def test_type_plane_too_long(self):
        with self.assertRaises(ValidationError):
            PlaneBase(
                type_plane="A" * 11,
                serial_number="SN123456789",
                tail_number="TN987654321",
                base_airfield="Аэродром №1",
                belong_plane="ВВС России",
                operating_time=15000
            )

    def test_serial_number_too_long(self):
        with self.assertRaises(ValidationError):
            PlaneBase(
                type_plane="Су-57",
                serial_number="A" * 33,
                tail_number="TN987654321",
                base_airfield="Аэродром №1",
                belong_plane="ВВС России",
                operating_time=15000
            )

    def test_tail_number_too_long(self):
        with self.assertRaises(ValidationError):
            PlaneBase(
                type_plane="Су-57",
                serial_number="SN123456789",
                tail_number="A" * 33,
                base_airfield="Аэродром №1",
                belong_plane="ВВС России",
                operating_time=15000
            )

    def test_base_airfield_too_long(self):
        with self.assertRaises(ValidationError):
            PlaneBase(
                type_plane="Су-57",
                serial_number="SN123456789",
                tail_number="TN987654321",
                base_airfield="A" * 101,
                belong_plane="ВВС России",
                operating_time=15000
            )

    def test_belong_plane_too_long(self):
        with self.assertRaises(ValidationError):
            PlaneBase(
                type_plane="Су-57",
                serial_number="SN123456789",
                tail_number="TN987654321",
                base_airfield="Аэродром №1",
                belong_plane="A" * 101,
                operating_time=15000
            )

    def test_operating_time_negative(self):
        with self.assertRaises(ValidationError):
            PlaneBase(
                type_plane="Су-57",
                serial_number="SN123456789",
                tail_number="TN987654321",
                base_airfield="Аэродром №1",
                belong_plane="ВВС России",
                operating_time=-1
            )

    def test_operating_time_too_high(self):
        with self.assertRaises(ValidationError):
            PlaneBase(
                type_plane="Су-57",
                serial_number="SN123456789",
                tail_number="TN987654321",
                base_airfield="Аэродром №1",
                belong_plane="ВВС России",
                operating_time=50001
            )

    def test_optional_manufacturer_date(self):
        data = {
            "type_plane": "Су-57",
            "serial_number": "SN123456789",
            "tail_number": "TN987654321",
            "base_airfield": "Аэродром №1",
            "belong_plane": "ВВС России",
            "operating_time": 15000,
            "manufacturer_date": None
        }
        plane = PlaneBase(**data)
        self.assertIsNone(plane.manufacturer_date)


if __name__ == "__main__":
    unittest.main()
