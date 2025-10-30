import unittest
from app.utils.case_converter import camel_to_snake_case

class TestCamelCaseToSnakeCase(unittest.TestCase):
    def test_camel_to_snake_case(self):
        self.assertEqual(camel_to_snake_case("camelCaseString"), "camel_case_string")
        self.assertEqual(camel_to_snake_case("CamelCaseString"), "camel_case_string")
        self.assertEqual(camel_to_snake_case("camel2Camel2Case"), "camel2_camel2_case")
        self.assertEqual(camel_to_snake_case("Camel2Camel2Case"), "camel2_camel2_case")
        self.assertEqual(camel_to_snake_case("Camel2Camel2Case123"), "camel2_camel2_case123")
        self.assertEqual(camel_to_snake_case("Camel2Camel2Case123ABC"), "camel2_camel2_case123_abc")

if __name__ == '__main__':
    unittest.main()