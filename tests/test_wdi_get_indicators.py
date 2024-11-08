import pytest
from wbwdi import wdi_get_indicators

def test_wdi_get_indicators_columns():
    result = wdi_get_indicators()
    
    expected_columns = {
        "indicator_id", "indicator_name", "source_id",
        "source_name", "source_note", "source_organization", "topics"
    }

    assert set(result.columns) == expected_columns, "DataFrame columns do not match the expected structure"

def test_wdi_get_indicators_invalid_language():
    with pytest.raises(Exception) as excinfo:
        wdi_get_indicators(language="xx")
    
    expected_error_message = (
        "Error code: 150\nResponse requested in an unsupported language.\n"
        "Read more at <https://datahelpdesk.worldbank.org/knowledgebase/articles/898620-api-error-codes>"
    )

    assert expected_error_message in str(excinfo.value), "The error message did not match the expected output."

def testwdi_get_indicators_invalid_per_page():
    with pytest.raises(ValueError, match="`per_page` must be an integer between 1 and 32,500"):
        wdi_get_indicators(per_page="xxx")
    