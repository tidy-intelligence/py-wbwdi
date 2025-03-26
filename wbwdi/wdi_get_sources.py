import polars as pl

from .config import format_output
from .perform_request import perform_request


def wdi_get_sources(language: str = "en") -> pl.DataFrame:
    """
    Download data sources from the World Bank API.

    This function returns a DataFrame of supported data sources for querying the
    World Bank API. The data sources include various databases and datasets
    provided by the World Bank.

    Parameters
    ----------
    language (str): A string specifying the language code for the API response
                    (default is "en" for English).

    Returns
    -------
    pl.DataFrame
        A DataFrame with the following columns:
        - `source_id`: An integer identifier for the data source.
        - `source_code`: A character string for the source code.
        - `source_name`: The name of the data source (e.g., "World Development Indicators").
        - `update_date`: The last update date of the data source.
        - `is_data_available`: A boolean indicating whether data is available.
        - `is_metadata_available`: A boolean indicating whether metadata is available.
        - `concepts`: The number of concepts defined for the data source.

    Details
    -------
    This function provides a reference for the supported data sources and their metadata when querying
    the World Bank API. The columns `is_data_available` and `is_metadata_available` are boolean values
    derived from the API response, where "Y" indicates availability.

    Source
    ------
    https://api.worldbank.org/v2/sources

    Examples
    --------
    Download all available data sources in English
    >>> wdi_get_sources()
    """
    sources_raw = perform_request("sources", language=language)

    sources_processed = (
        pl.DataFrame(sources_raw)
        .rename(
            {
                "id": "source_id",
                "code": "source_code",
                "name": "source_name",
                "lastupdated": "update_date",
                "dataavailability": "is_data_available",
                "metadataavailability": "is_metadata_available",
                "concepts": "concepts",
            }
        )
        .with_columns(
            source_id=pl.col("source_id").cast(pl.Int64),
            source_name=pl.col("source_name").str.strip_chars(),
            update_date=pl.col("update_date").str.to_date(),
            is_data_available=pl.col("is_data_available") == "Y",
            is_metadata_available=pl.col("is_metadata_available") == "Y",
            concepts=pl.col("concepts").cast(pl.Int64),
        )
        .select(
            pl.col("source_id"),
            pl.col("source_code"),
            pl.col("source_name"),
            pl.col("update_date"),
            pl.col("is_data_available"),
            pl.col("is_metadata_available"),
            pl.col("concepts"),
        )
    )

    return format_output(sources_processed)
