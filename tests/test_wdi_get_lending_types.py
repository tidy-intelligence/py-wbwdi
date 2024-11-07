import pytest
from wbwdi import wdi_get_lending_types

def test_wdi_get_lending_types_columns():
    result = wdi_get_lending_types(language="en")
    
    expected_columns = {"lending_type_id", "lending_type_iso2code", "lending_type_name"}

    assert set(result.columns) == expected_columns, "DataFrame columns do not match the expected structure"

def test_wdi_get_lending_types_invalid_language():
    with pytest.raises(Exception) as excinfo:
        wdi_get_lending_types(language="xx")
    
    expected_error_message = (
        "Error code: 150\nResponse requested in an unsupported language.\n"
        "Read more at <https://datahelpdesk.worldbank.org/knowledgebase/articles/898620-api-error-codes>"
    )

    assert expected_error_message in str(excinfo.value), "The error message did not match the expected output."
