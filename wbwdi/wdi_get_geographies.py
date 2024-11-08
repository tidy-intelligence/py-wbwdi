import polars as pl
from .perform_request import perform_request

def wdi_get_geographies(language="en", per_page=1000) -> pl.DataFrame:
    """
    Download all countries and regions from the World Bank API.

    This function retrieves information about geographies (countries and regions) 
    from the World Bank API. It returns a DataFrame containing various details such 
    as the geography's ID, ISO2 code, name, region information, lending type, 
    capital city, and coordinates.

    Parameters:
    -----------
    language (str): A character string specifying the language for the API response. 
                    Defaults to "en" (English). Other supported options include "es" 
                    (Spanish), "fr" (French), and others depending on the API.
    per_page (int): An integer specifying the number of records to fetch per request. 
                    Defaults to 1000.

    Returns:
    -----------
    pl.DataFrame
        A DataFrame with the following columns:
        - `geography_id`: A character string representing the geography's unique identifier.
        - `geography_name`: A character string for the name of the geography.
        - `geography_iso2code`: A character string for the ISO2 country code.
        - `geography_type`: A character string for the type of the geography ("country" or "region").
        - `region_id`: A character string representing the region's unique identifier.
        - `region_name`: A character string for the name of the region.
        - `region_iso2code`: A character string for the ISO2 region code.
        - `admin_region_id`: A character string representing the administrative region's unique identifier.
        - `admin_region_name`: A character string for the name of the administrative region.
        - `admin_region_iso2code`: A character string for the ISO2 code of the administrative region.
        - `income_level_id`: A character string representing the geography's income level.
        - `income_level_name`: A character string for the name of the income level.
        - `income_level_iso2code`: A character string for the ISO2 code of the income level.
        - `lending_type_id`: A character string representing the lending type's unique identifier.
        - `lending_type_name`: A character string for the name of the lending type.
        - `lending_type_iso2code`: A character string for the ISO2 code of the lending type.
        - `capital_city`: A character string for the name of the capital city.
        - `longitude`: A numeric value for the longitude of the geography.
        - `latitude`: A numeric value for the latitude of the geography.

    Details:
    -----------
    This function sends a request to the World Bank API to retrieve data for all 
    supported geographies in the specified language. The data is then processed into 
    a tidy format and includes information about the country, such as its ISO code, 
    capital city, geographical coordinates, and additional metadata about regions, 
    income levels, and lending types.

    Source:
    -----------
    https://api.worldbank.org/v2/geographies

    Examples:
    -----------
    Download all geographies in English
    >>> wdi_get_geographies()

    Download all geographies in Spanish
    >>> wdi_get_geographies(language="es")
    """
    geographies_raw = perform_request("countries/all", language, per_page)

    geographies_processed = (pl.DataFrame(geographies_raw)
        .rename({"id": "geography_id", "iso2Code": "geography_iso2code", "name": "geography_name"})
        .unnest("region")
        .rename({"id": "region_id", "iso2code": "region_iso2code", "value": "region_name"})
        .unnest("adminregion")
        .rename({"id": "admin_region_id", "iso2code": "admin_region_iso2code", "value": "admin_region_name"})
        .unnest("incomeLevel")
        .rename({"id": "income_level_id", "iso2code": "income_level_iso2code", "value": "income_level_name"})
        .unnest("lendingType")
        .rename({"id": "lending_type_id", "iso2code": "lending_type_iso2code", "value": "lending_type_name"})
        .rename({"capitalCity": "capital_city"})
        .with_columns(
            longitude = pl.when(pl.col("longitude") == "").then(None).otherwise(pl.col("longitude")).cast(pl.Float64),
            latitude = pl.when(pl.col("latitude") == "").then(None).otherwise(pl.col("latitude")).cast(pl.Float64),
            geography_type = pl.when(pl.col("region_name") == "Aggregates").then(pl.lit("Region")).otherwise(pl.lit("Country"))
        )
    )

    geographies_processed = (geographies_processed
        .with_columns([
            pl.when(pl.col(column) == "").then(None).otherwise(pl.col(column)).alias(column)
            for column in geographies_processed.select(pl.col(pl.Utf8)).columns
        ])
        .with_columns([
            pl.col(column).str.strip_chars().alias(column)
            for column in geographies_processed.select(pl.col(pl.Utf8)).columns
        ])
        .select(
            pl.col("geography_id"), pl.col("geography_name"), pl.col("geography_iso2code"),
            pl.col("geography_type"), pl.col("capital_city"), pl.col("region_id"), pl.col("region_name"),
            pl.col("region_iso2code"), pl.col("admin_region_id"), pl.col("admin_region_name"),
            pl.col("admin_region_iso2code"), pl.col("income_level_id"), pl.col("income_level_name"),
            pl.col("income_level_iso2code"), pl.col("lending_type_id"), pl.col("lending_type_name"),
            pl.col("lending_type_iso2code"), pl.col("longitude"), pl.col("latitude")
        )
    )

    return geographies_processed