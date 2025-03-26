import pytest

from wbwdi import wdi_get_income_levels


def test_wdi_get_income_levels_columns():
    result = wdi_get_income_levels(language="en")

    expected_columns = {"income_level_id", "income_level_iso2code", "income_level_name"}

    assert set(result.columns) == expected_columns, (
        "DataFrame columns do not match the expected structure"
    )


def test_wdi_get_income_levels_invalid_language():
    with pytest.raises(Exception) as excinfo:
        wdi_get_income_levels(language="xx")

    expected_error_message = (
        "Error code: 150\nResponse requested in an unsupported language.\n"
        "Read more at <https://datahelpdesk.worldbank.org/knowledgebase/articles/898620-api-error-codes>"
    )

    assert expected_error_message in str(excinfo.value), (
        "The error message did not match the expected output."
    )
