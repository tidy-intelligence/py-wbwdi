import polars as pl
from .perform_request import perform_request

def wdi_get_topics(language: str = "en") -> pl.DataFrame:
    """
    This function returns a tibble of supported topics for querying the World
    Bank API. Topics represent the broad subject areas covered by the World
    Bank's datasets.

    Parameters:
    ----------
    language : str, optional
        A string specifying the language code for the API response (default is "en" for English).
    
    Returns:
    -------
    pl.DataFrame
        A DataFrame with the following columns:
        - topic_id: The unique identifier for the topic.
        - topic_name: The name of the topic (e.g., "Education", "Health").
        - topic_note: A brief description or note about the topic.

    Details:
    This function provides a reference for the supported topics that can be used 
    to refine your queries when accessing the World Bank API. Topics represent 
    different areas of focus for data analysis.

    Source:
    https://api.worldbank.org/v2/topics

    Examples:
    >>> # Download all available topics in English
    >>> wdi_get_topics()
    """
    topics_raw = perform_request("topics", language=language)

    topics_processed = (pl.DataFrame(topics_raw)
        .rename(
            {"id": "topic_id", "value": "topic_name", "sourceNote": "topic_note"}
        )
        .with_columns(
            topic_id = pl.col("topic_id").cast(pl.Int64),
            topic_name = pl.col("topic_name").str.strip_chars_end(),
            topic_note = pl.col("topic_note").str.strip_chars_end()
        )
    )

    return topics_processed
