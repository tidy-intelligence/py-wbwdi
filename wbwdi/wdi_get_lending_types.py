import polars as pl

from .perform_request import perform_request
from .utils import convert_to_pandas


def wdi_get_lending_types(language="en", to_pandas: bool = False) -> pl.DataFrame:
    """
    Download lending types from the World Bank API.

    This function returns a DataFrame of supported lending types for querying the
    World Bank API. The lending types classify countries based on the financial
    terms available to them from the World Bank.

    Parameters:
    language (str): A character string specifying the language code for the API
        response (default is "en" for English).
    to_pandas (bool): A boolean indicating whether to return a pandas DataFrame.
        Requires the `pandas` and `pyarrow` packages. Defaults to `False`.

    Returns:
    -------
    pl.DataFrame
        A DataFrame with the following columns:
        - `lending_type_id`: An integer for the lending type.
        - `lending_type_iso2code`: A character string for the ISO2 code of the lending type.
        - `lending_type_name`: A description of the lending type (e.g., "IBRD", "IDA").

    Details:
    This function provides a reference for the supported lending types, which
    classify countries according to the financial terms they are eligible for
    under World Bank programs. The language parameter allows the results to be
    returned in different languages as supported by the API.

    Source:
    https://api.worldbank.org/v2/lendingTypes

    Examples:
    Download all lending types in English
    >>> wdi_get_lending_types()
    """

    lending_types_raw = perform_request("lendingTypes", language=language)

    lending_types_processed = pl.DataFrame(lending_types_raw).rename(
        {
            "id": "lending_type_id",
            "iso2code": "lending_type_iso2code",
            "value": "lending_type_name",
        }
    )

    if to_pandas:
        lending_types_processed = convert_to_pandas(lending_types_processed)

    return lending_types_processed
