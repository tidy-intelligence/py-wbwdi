import pandas as pd
import polars as pl
import pyarrow as pa
import pytest

from wbwdi.config import VALID_FORMATS, format_output, wdi_set_format


def test_wdi_set_format_invalid():
    """Test that invalid formats raise ValueError."""
    with pytest.raises(ValueError) as excinfo:
        wdi_set_format("invalid_format")

    # Check error message contains valid formats
    error_msg = str(excinfo.value)
    assert "Invalid format 'invalid_format'" in error_msg
    for fmt in VALID_FORMATS:
        assert fmt in error_msg


def test_format_output_polars():
    """Test that polars format returns the original DataFrame."""
    # Setup - create a simple Polars DataFrame
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    # Set format to polars
    wdi_set_format("polars")

    # Test
    result = format_output(df)

    # Verify result is the same polars DataFrame
    assert isinstance(result, pl.DataFrame)
    assert result.equals(df)


def test_format_output_pandas():
    """Test that pandas format converts to pandas DataFrame."""
    # Setup - create a simple Polars DataFrame
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    # Set format to pandas
    wdi_set_format("pandas")

    # Test
    result = format_output(df)

    # Verify result is a pandas DataFrame with the same data
    assert isinstance(result, pd.DataFrame)
    assert result.equals(pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]}))


def test_format_output_arrow():
    """Test that arrow format converts to Arrow table."""
    # Setup - create a simple Polars DataFrame
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    # Set format to arrow
    wdi_set_format("arrow")

    # Test
    result = format_output(df)

    # Verify result is an Arrow Table with the same data
    assert isinstance(result, pa.Table)
    # Convert back to pandas to easily compare content
    pd_result = result.to_pandas()
    pd_expected = df.to_pandas()
    assert pd_result.equals(pd_expected)


def test_format_output_global_state():
    """Test that format_output uses the global RETURN_FORMAT."""
    # Setup - create a simple Polars DataFrame
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    for fmt in VALID_FORMATS:
        wdi_set_format(fmt)
        result = format_output(df)

        if fmt == "polars":
            assert isinstance(result, pl.DataFrame)
        elif fmt == "pandas":
            assert isinstance(result, pd.DataFrame)
        elif fmt == "arrow":
            assert isinstance(result, pa.Table)


wdi_set_format("polars")
