import pytest
from wbwdi import wdi_get_sources

def test_wdi_get_sources_columns():
    result = wdi_get_sources(language="en")
    
    expected_columns = {"source_id", "source_iso2code", "source_name", "update_date", "is_data_available", "is_metadata_available", "concepts"}

    assert set(result.columns) == expected_columns, "DataFrame columns do not match the expected structure"

def test_wdi_get_sources_invalid_language():
    with pytest.raises(Exception) as excinfo:
        wdi_get_sources(language="xx")
    
    expected_error_message = (
        "Error code: 150\nResponse requested in an unsupported language.\n"
        "Read more at <https://datahelpdesk.worldbank.org/knowledgebase/articles/898620-api-error-codes>"
    )

    assert expected_error_message in str(excinfo.value), "The error message did not match the expected output."
