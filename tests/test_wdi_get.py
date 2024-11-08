import pytest
import polars as pl
from wbwdi import wdi_get

def test_single_geography_single_indicator():
    result = wdi_get("US", "NY.GDP.PCAP.KD", start_date=2020, end_date=2021)
    assert isinstance(result, pl.DataFrame)
    assert not result.is_empty(), "DataFrame should not be empty for valid inputs."
    assert "geography_id" in result.columns, "Expected 'geography_id' column in DataFrame."
    assert "indicator_id" in result.columns, "Expected 'indicator_id' column in DataFrame."

def test_multiple_geographies_single_indicator():
    result = wdi_get(["US", "CA"], "NY.GDP.PCAP.KD", start_date=2020, end_date=2021)
    assert isinstance(result, pl.DataFrame)
    assert not result.is_empty(), "DataFrame should not be empty for valid inputs."
    assert len(result["geography_id"].unique()) == 2, "Should have data for two geographies."

def test_single_geography_multiple_indicators():
    result = wdi_get("US", ["NY.GDP.PCAP.KD", "SP.POP.TOTL"], start_date=2020, end_date=2021)
    assert isinstance(result, pl.DataFrame)
    assert not result.is_empty(), "DataFrame should not be empty for valid inputs."
    assert len(result["indicator_id"].unique()) == 2, "Should have data for two indicators."

def test_multiple_geographies_multiple_indicators():
    result = wdi_get(["US", "CA"], ["NY.GDP.PCAP.KD", "SP.POP.TOTL"], start_date=2020, end_date=2021)
    assert isinstance(result, pl.DataFrame)
    assert not result.is_empty(), "DataFrame should not be empty for valid inputs."
    assert len(result["geography_id"].unique()) == 2, "Should have data for two geographies."
    assert len(result["indicator_id"].unique()) == 2, "Should have data for two indicators."

def test_frequency_quarterly():
    result = wdi_get("NG", "DT.DOD.DECT.CD.TL.US", start_date=2020, end_date=2021, frequency="quarter")
    assert isinstance(result, pl.DataFrame)
    assert "quarter" in result.columns, "Expected 'quarter' column for quarterly data."

def test_frequency_monthly():
    result = wdi_get("US", "DPANUSSPB", start_date=2020, end_date=2021, frequency="month")
    assert isinstance(result, pl.DataFrame)
    assert "month" in result.columns, "Expected 'month' column for monthly data."

def test_all_geographies():
    result = wdi_get("all", "NY.GDP.PCAP.KD", start_date=2020, end_date=2021, progress=False)
    assert isinstance(result, pl.DataFrame)
    assert not result.is_empty(), "DataFrame should not be empty for 'all' geographies input."

def test_long_format():
    result = wdi_get("US", "NY.GDP.PCAP.KD", start_date=2020, end_date=2021, format="long")
    assert isinstance(result, pl.DataFrame)
    assert "indicator_id" in result.columns, "Expected 'indicator_id' column in long format."
    assert "value" in result.columns, "Expected 'value' column in long format."

def test_wide_format():
    result = wdi_get("US", ["NY.GDP.PCAP.KD", "SP.POP.TOTL"], start_date=2020, end_date=2021, format="wide")
    assert isinstance(result, pl.DataFrame)
    assert "NY.GDP.PCAP.KD" in result.columns, "Expected GDP indicator as column in wide format."
    assert "SP.POP.TOTL" in result.columns, "Expected population indicator as column in wide format."

def test_invalid_frequency():
    with pytest.raises(ValueError, match="`frequency` must be either 'annual', 'quarter', or 'month'."):
        wdi_get("US", "NY.GDP.PCAP.KD", start_date=2020, end_date=2021, frequency="daily")

def test_invalid_format():
    with pytest.raises(ValueError, match="`format` must be either 'long' or 'wide'."):
        wdi_get("US", "NY.GDP.PCAP.KD", start_date=2020, end_date=2021, format="compact")

def test_invalid_geography():
    with pytest.raises(Exception) as excinfo:
        wdi_get("INVALID.GEOGRAPHY", "NY.GDP.PCAP.KD")
    
    expected_error_message = (
        "Error code: 120\nThe provided parameter value is not valid\n"
        "Read more at <https://datahelpdesk.worldbank.org/knowledgebase/articles/898620-api-error-codes>"
    )

    assert expected_error_message in str(excinfo.value), "The error message did not match the expected output."     

def test_invalid_indicator():
    with pytest.raises(Exception) as excinfo:
        wdi_get("US", "INVALID.INDICATOR")
    
    expected_error_message = (
        "Error code: 120\nThe provided parameter value is not valid\n"
        "Read more at <https://datahelpdesk.worldbank.org/knowledgebase/articles/898620-api-error-codes>"
    )

    assert expected_error_message in str(excinfo.value), "The error message did not match the expected output."
        
