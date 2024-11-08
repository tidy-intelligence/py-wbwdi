import pytest
from wbwdi import wdi_get_geographies  

def test_wdi_get_geographies_columns():
    result = wdi_get_geographies()
    
    expected_columns = {
        "geography_id", "geography_name", "geography_iso2code",
        "geography_type", "capital_city", "region_id", "region_name",
        "region_iso2code", "admin_region_id", "admin_region_name",
        "admin_region_iso2code", "income_level_id", "income_level_name",
        "income_level_iso2code", "lending_type_id", "lending_type_name",
        "lending_type_iso2code", "longitude", "latitude"
    }

    assert set(result.columns) == expected_columns, "DataFrame columns do not match the expected structure"

def test__wdi_get_geographies_invalid_language():
    with pytest.raises(Exception) as excinfo:
        wdi_get_geographies(language="xx")
    
    expected_error_message = (
        "Error code: 150\nResponse requested in an unsupported language.\n"
        "Read more at <https://datahelpdesk.worldbank.org/knowledgebase/articles/898620-api-error-codes>"
    )

    assert expected_error_message in str(excinfo.value), "The error message did not match the expected output."

def test_wdi_get_geographies_invalid_per_page():
    with pytest.raises(ValueError, match="`per_page` must be an integer between 1 and 32,500"):
        wdi_get_geographies(per_page="xx")
    