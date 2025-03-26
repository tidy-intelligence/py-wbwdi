VALID_FORMATS = {"polars", "pandas", "arrow"}
RETURN_FORMAT = "polars"


def wdi_set_format(fmt: str):
    fmt = fmt.lower()
    if fmt not in VALID_FORMATS:
        raise ValueError(f"Invalid format '{fmt}'. Choose from {VALID_FORMATS}.")
    global RETURN_FORMAT
    RETURN_FORMAT = fmt


def format_output(df):
    """
    Converts a Polars DataFrame to the desired output format.

    Parameters:
    -----------
    df : pl.DataFrame
        The input Polars DataFrame.

    Returns:
    --------
    The DataFrame in the requested format.
    """
    if RETURN_FORMAT == "pandas":
        return df.to_pandas()
    elif RETURN_FORMAT == "arrow":
        return df.to_arrow()
    elif RETURN_FORMAT == "polars":
        return df
