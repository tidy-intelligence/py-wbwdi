import pytest
from wbwdi import wdi_get_languages

def test_wdi_get_languages_columns():
    result = wdi_get_languages()
    
    expected_columns = {"language_code", "language_name", "native_form"}

    assert set(result.columns) == expected_columns, "DataFrame columns do not match the expected structure"
