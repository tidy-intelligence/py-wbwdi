import polars as pl
from wbwdi.wdi_get_sources import wdi_get_sources
from wbwdi.perform_request import perform_request

def wdi_get(entities, indicators, start_year=None, end_year=None, frequency="annual", 
            language="en", per_page=1000, progress=True, source=None, format="long"):
    """
    Download World Bank indicator data for specific entities and time periods.

    This function retrieves indicator data from the World Bank API for a specified set 
    of entities and indicators. The user can specify one or more indicators, a date 
    range, and other options to tailor the request. The data is processed and returned 
    in a tidy format, including country, indicator, date, and value fields.

    Parameters:
    entities (list of str): A list of ISO 2-country codes, or "all" to retrieve data for all entities.
    indicators (list of str): A list specifying one or more World Bank indicators to download (e.g., ["NY.GDP.PCAP.KD", "SP.POP.TOTL"]).
    start_year (int, optional): The starting year for the data.
    end_year (int, optional): The ending year for the data.
    frequency (str): The frequency of the data ("annual", "quarter", "month"). Defaults to "annual".
    language (str): The language for the request. See wdi_get_languages for options. Defaults to "en".
    per_page (int): The number of results per page for the API. Defaults to 1000.
    progress (bool): Whether to show progress messages during data download and parsing. Defaults to True.
    source (int, optional): The data source, see wdi_get_sources.
    format (str): Specifies whether the data is returned in "long" or "wide" format. Defaults to "long".

    Returns:
    -----------
    pl.DataFrame
        A DataFrame with the following columns:
        - `indicator_id`: The ID of the indicator (e.g., "NY.GDP.PCAP.KD").
        - `entity_id`: The ISO 2-country code of the country or region for which the data was retrieved.
        - `year`: The year of the indicator data as an integer.
        - `quarter` (optional`: The quarter of the indicator data as an integer.
        - `month` (optional): The month of the indicator data as an integer.
        - `value`: The value of the indicator for the given country and date.

    Details:
    This function constructs a request URL for the World Bank API, retrieves the relevant 
    data for the given entities and indicators, and processes the response into a tidy 
    format. The user can optionally specify a date range, and the function will handle 
    requests for multiple pages if necessary. If `progress` is True, messages will be 
    displayed during the request and parsing process.

    The function supports downloading multiple indicators by sending individual API requests 
    for each indicator and then combining the results into a single tidy DataFrame.

    Examples:
    # Download single indicator for multiple entities
    >>> wdi_get(["US", "CA", "GB"], "NY.GDP.PCAP.KD")

    # Download single indicator for a specific time frame
    >>> wdi_get(["US", "CA", "GB"], "DPANUSSPB", start_year=2012, end_year=2013)

    # Download single indicator for monthly frequency
    >>> wdi_get("AT", "DPANUSSPB", start_year=2012, end_year=2015, frequency="month")

    # Download single indicator for quarterly frequency
    >>> wdi_get("NG", "DT.DOD.DECT.CD.TL.US", start_year=2012, end_year=2015, frequency="quarter")

    # Download single indicator for all entities and disable progress bar
    >>> wdi_get("all", "NY.GDP.PCAP.KD", progress=False)

    # Download multiple indicators for multiple entities
    >>> wdi_get(["US", "CA", "GB"], ["NY.GDP.PCAP.KD", "SP.POP.TOTL"])

    # Download indicators for different sources
    >>> wdi_get("DE", "SG.LAW.INDX", source=2)
    >>> wdi_get("DE", "SG.LAW.INDX", source=14)

    # Download indicators in wide format
    >>> wdi_get(["US", "CA", "GB"], ["NY.GDP.PCAP.KD"], format="wide")
    >>> wdi_get(["US", "CA", "GB"], ["NY.GDP.PCAP.KD", "SP.POP.TOTL"], format="wide")
    """
    if isinstance(entities, str):
        entities = [entities] 
    if isinstance(indicators, str):
        indicators = [indicators]

    validate_frequency(frequency)
    validate_progress(progress)
    validate_source(source)
    validate_format(format)

    if frequency == "annual" and start_year and end_year:
        start_year = str(start_year)
        end_year = str(end_year)
    elif frequency == "quarter" and start_year and end_year:
        start_year = f"{start_year}Q1"
        end_year = f"{end_year}Q4"
    elif frequency == "month" and start_year and end_year:
        start_year = f"{start_year}M01"
        end_year = f"{end_year}M12"

    indicators_processed = pl.concat([
        get_indicator(
            indicator, entities, start_year, end_year,
            language, per_page, progress, source
        )
        for indicator in indicators
    ])

    if format == "wide":
        indicators_processed = (indicators_processed
            .pivot(
                index=["entity_id", "year"], 
                on="indicator_id", 
                values="value"
            )
        )
    
    return indicators_processed

def validate_frequency(frequency):
    valid_frequencies = ["annual", "quarter", "month"]
    if frequency not in valid_frequencies:
        raise ValueError("`frequency` must be either 'annual', 'quarter', or 'month'.")

def validate_progress(progress):
    if not isinstance(progress, bool):
        raise ValueError("`progress` must be either True or False.")

def validate_source(source):
    if source is not None:
        supported_sources = wdi_get_sources()
        if source not in supported_sources["source_id"]:
            raise ValueError("`source` is not supported. Please call `wdi_get_sources()`.")

def validate_format(format):
    if format not in ["long", "wide"]:
        raise ValueError("`format` must be either 'long' or 'wide'.")

def create_date(start_year, end_year):
    return f"{start_year}:{end_year}" if start_year and end_year else None

def get_indicator(indicator, entities, start_year, end_year,
                  language, per_page, progress, source):
    progress_req = f"Sending requests for indicator {indicator}" if progress else None
    date = create_date(start_year, end_year)
    resource = f"country/{';'.join(entities)}/indicator/{indicator}"
    indicator_raw = perform_request(resource, language, per_page, date, source, progress_req)

    indicator_parsed = (pl.DataFrame(indicator_raw)
        .rename({"value" : "_value"})
        .unnest("indicator")
        .rename({"id": "indicator_id"})
        .drop("value")
        .unnest("country")
        .rename({"id": "entity_id"})
        .drop("value")
        .select(["indicator_id", "entity_id", "date", "_value"])
        .rename({"_value": "value"})
        .with_columns(
            value = pl.col("value").cast(pl.Float64)
        )
    )
    
    if "Q" in indicator_parsed["date"][0]:
        indicator_parsed = (indicator_parsed
            .with_columns(
                year = pl.col("date").str.slice(0, 4).cast(pl.Int32),
                quarter = pl.col("date").str.slice(5, 6).cast(pl.Int32)
            )
            .drop("date")
            .sort(["year", "quarter"])
        )
    elif "M" in indicator_parsed["date"][0]:
        indicator_parsed = (indicator_parsed
            .with_columns(
                year = pl.col("date").str.slice(0, 4).cast(pl.Int32),
                month = pl.col("date").str.slice(5, 7).cast(pl.Int32)
            )
            .drop("date")
            .sort(["year", "month"])
        )
    else:
        indicator_parsed = (indicator_parsed
            .with_columns(
                year = pl.col("date").cast(pl.Int32)
            )
            .drop("date")
            .sort("year")
        )
    
    return indicator_parsed
