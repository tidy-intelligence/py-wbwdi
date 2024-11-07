import polars as pl
from .perform_request import perform_request

def wdi_get_income_levels(language: str = "en") -> pl.DataFrame:
    """
    Download income levels from the World Bank API.

    This function returns a DataFrame of supported income levels for querying the
    World Bank API. The income levels categorize countries based on their gross
    national income per capita.

    Parameters:
    -----------
    language : str, optional
        A string specifying the language code for the API response (default is "en" for English).

    Returns:
    --------
    pl.DataFrame
        A DataFrame with the following columns:
        - `income_level_id`: An integer identifier for the income level.
        - `income_level_iso2code`: Character string representing the ISO2 code for the income level.
        - `income_level_name`: Description of the income level (e.g., "Low income", "High income").

    Details:
    --------
    This function provides a reference for the supported income levels,
    which categorize countries according to their income group as defined by the
    World Bank. The language parameter allows the results to be returned in
    different languages as supported by the API.

    Source:
    -------
    https://api.worldbank.org/v2/incomeLevels
    
    Examples:
    -------
    >>> wdi_get_income_levels()
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
