import pytest
from wbwdi import wdi_get_income_levels  

def test_wdi_get_income_levels_columns():
    result = wdi_get_income_levels(language="en")
    
    expected_columns = {"income_level_id", "income_level_iso2code", "income_level_name"}

    assert set(result.columns) == expected_columns, "DataFrame columns do not match the expected structure"