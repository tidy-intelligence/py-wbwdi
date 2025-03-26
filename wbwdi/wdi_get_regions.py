import polars as pl

from .config import format_output
from .perform_request import perform_request


def wdi_get_regions(language: str = "en") -> pl.DataFrame:
    """
    Download regions from the World Bank API.

    This function returns a DataFrame of supported regions for querying the World
    Bank API. The regions include various geographic areas covered by the World
    Bank's datasets.

    Parameters
    ----------
    language (str): A string specifying the language code for the API response
        (default is "en" for English).

    Returns
    -------
    pl.DataFrame
        A DataFrame with the following columns:
        - `region_id`: An integer for the identifier for each region.
        - `region_code`: A character string representing the region code.
        - `region_iso2code`: A character string representing the ISO2 code for the region.
        - `region_name`: A character string representing the name of the region, in the specified language.

    Details
    -------
    This function provides a reference for the supported regions, which are important
    for refining queries related to geographic data in the World Bank's datasets.
    The `region_id` column is unique for seven key regions.

    Source
    ------
    https://api.worldbank.org/v2/region

    Examples
    --------
    Download all regions in English
    >>> wdi_get_regions()
    """
    regions_raw = perform_request("region", language=language)

    # id is non-missing for 7 entries
    regions_processed = (
        pl.DataFrame(regions_raw)
        .rename(
            {
                "id": "region_id",
                "code": "region_code",
                "iso2code": "region_iso2code",
                "name": "region_name",
            }
        )
        .with_columns(
            region_id=pl.when(pl.col("region_id") == "")
            .then(None)
            .otherwise(pl.col("region_id"))
            .cast(pl.Int64),
            region_name=pl.col("region_name").str.strip_chars(),
        )
    )

    return format_output(regions_processed)
