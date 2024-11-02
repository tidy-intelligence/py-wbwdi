import polars as pl
from .perform_request import perform_request

def wdi_get_income_levels(language: str = "en") -> pl.DataFrame:
    """
    Retrieve and process income level data from the World Bank API.

    Parameters:
    ----------
    language : str, default="en"
        The language code for the API response.

    Returns:
    -------
    pl.DataFrame
        A DataFrame containing income level data with renamed columns and whitespace trimmed.
    """
    income_levels_raw = perform_request("incomeLevels", language=language)

    income_levels_processed = (pl.DataFrame(income_levels_raw)
        .rename({
            "id": "income_level_id",
            "iso2code": "income_level_iso2code",
            "value": "income_level_name"
        })
    )

    return income_levels_processed
