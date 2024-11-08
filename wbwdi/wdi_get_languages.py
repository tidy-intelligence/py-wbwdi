import polars as pl
from .perform_request import perform_request

def wdi_get_languages() -> pl.DataFrame:
    """
    Download languages from the World Bank API.

    This function returns a DataFrame of supported languages for querying the 
    World Bank API. The supported languages include English, Spanish, French, 
    Arabic, Chinese, and others.

    Returns:
     pl.DataFrame
        A DataFrame with the following columns:
        - `language_code`: A character string representing the language code 
                         (e.g., "en" for English).
        - `language_name`: A character string representing the description of the 
                         language (e.g., "English").
        - `native_form`: A character string representing the native form of the 
                       language (e.g., "English").

    Details:
    This function provides a simple reference for the supported languages when 
    querying the World Bank API.

    Source:
    https://api.worldbank.org/v2/languages

    Examples:
    Download all languages
    >>> wdi_get_languages()
    """

    langauges_raw = perform_request("languages")

    languages_processed = (pl.DataFrame(langauges_raw)
        .rename({
            "code": "language_code",
            "name": "language_name",
            "nativeForm": "native_form"
        })
        .with_columns(
            language_name = pl.col("language_name").str.strip_chars_end(),
            native_form = pl.col("native_form").str.strip_chars_end()
        )
    )

    return languages_processed