import polars as pl

from .perform_request import perform_request
from .utils import convert_to_pandas


def wdi_get_indicators(
    language="en", per_page=32500, to_pandas: bool = False
) -> pl.DataFrame:
    """
    Download all available World Bank indicators.

    This function retrieves a comprehensive list of all indicators supported by
    the World Bank API. The indicators include metadata such as the indicator ID,
    name, unit, source, and associated topics. The user can specify the language
    of the API response and whether to include additional details.

    Parameters:
    -----------
    language (str): A string specifying the language code for the API
        response (default is "en" for English).
    per_page (int): An integer specifying the number of results per page for the
        API. Defaults to 32,500. Must be a value between 1 and 32,500.
    to_pandas (bool): A boolean indicating whether to return a pandas DataFrame.
        Requires the `pandas` and `pyarrow` packages. Defaults to `False`.

    Returns:
    -----------
        pl.DataFrame
        A DataFrame with the following columns:
        - `indicator_id`: A character string for the ID of the indicator (e.g., "NY.GDP.PCAP.KD").
        - `indicator_name`: A character string for the name of the indicator (e.g., "GDP per capita, constant prices").
        - `source_id`: An integer identifying the data source providing the indicator.
        - `source_name`: A character string describing the source of the indicator data.
        - `source_note`: A character string providing additional notes about the data source.
        - `source_organization`: A character string denoting the organization responsible for the data source.
        - `topics`: A nested list containing (possibly multiple) topics associated with the indicator, with two columns: an integer `topic_id` and a character `topic_name`.

    Details:
    -----------
    This function makes a request to the World Bank API to retrieve metadata for
    all available indicators. It processes the response into a tidy DataFrame format.

    Source:
    -----------
    https://api.worldbank.org/v2/indicators

    Examples:
    -----------
    Download all supported indicators in English
    >>> wdi_get_indicators()

    Download all supported indicators in Spanish
    >>> wdi_get_indicators(language="es")
    """

    indicators_raw = perform_request("indicators", language=language, per_page=per_page)

    indicators_processed = (
        pl.DataFrame(indicators_raw)
        .rename({"id": "indicator_id", "name": "indicator_name"})
        .unnest("source")
        .rename(
            {
                "id": "source_id",
                "value": "source_name",
                "sourceNote": "source_note",
                "sourceOrganization": "source_organization",
            }
        )
        .drop("unit")
        .with_columns(
            source_id=pl.col("source_id").cast(pl.Int64),
            source_note=pl.when(pl.col("source_note") == "")
            .then(None)
            .otherwise(pl.col("source_note")),
            source_organization=pl.when(pl.col("source_organization") == "")
            .then(None)
            .otherwise(pl.col("source_organization")),
        )
    )

    topics = (
        indicators_processed.select(pl.col("indicator_id", "topics"))
        .explode("topics")
        .unnest("topics")
        .rename({"id": "topic_id", "value": "topic_name"})
        .with_columns(
            topic_id=pl.col("topic_id").cast(pl.Int64),
            topic_name=pl.col("topic_name").str.strip_chars(),
        )
        .group_by("indicator_id")
        .agg(topics=pl.struct(["topic_id", "topic_name"]))
    )

    indicators_processed = indicators_processed.drop("topics").join(
        topics, on="indicator_id", how="left"
    )

    if to_pandas:
        indicators_processed = convert_to_pandas(indicators_processed)

    return indicators_processed
