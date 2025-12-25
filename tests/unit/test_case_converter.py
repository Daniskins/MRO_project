import pytest
from app.utils.case_converter import camel_to_snake_case

@pytest.mark.parametrize('input_str, expected_output', [
                         ("camelCaseString", "camel_case_string"),
                         ("CamelCaseString", "camel_case_string"),
                         ("camel2Camel2Case", "camel2_camel2_case"),
                         ("Camel2Camel2Case", "camel2_camel2_case"),
                         ("Camel2Camel2Case123", "camel2_camel2_case123"),
                         ("Camel2Camel2Case123ABC", "camel2_camel2_case123_abc")])

def test_camel_to_snake_case(input_str, expected_output):
    assert camel_to_snake_case(input_str) == expected_output