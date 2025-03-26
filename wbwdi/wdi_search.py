from functools import reduce

import polars as pl


def wdi_search(data, keywords, columns=None):
    """
    Search for Keywords in DataFrame Columns.

    This function searches for specified keywords across columns in a DataFrame
    and returns only the rows where at least one keyword appears in any of the
    specified columns. It does not support nested columns (lists within columns) and
    provides the option to limit the search to specific columns.

    Parameters:
    -----------
    data (pl.DataFrame): A DataFrame to search. It can include nested columns (lists within columns).
    keywords (list of str): A list of keywords to search for within the specified columns. The search is case-insensitive.
    columns (list of str, optional): A list of column names to limit the search to specific columns. If None, all columns in `data` will be searched.

    Returns:
    -----------
    pl.DataFrame: A DataFrame containing only the rows where at least one keyword is found in the specified columns. The returned DataFrame has the same structure as `data`.

    Examples:
    -----------
    Download indicators
    >>> indicators = wdi_get_indicators()

    Search for keywords "inequality" or "gender" across all columns
    >>> wdi_search(indicators, keywords=["inequality", "gender"])

    Search for keywords only within the "indicator_name" column
    >>> wdi_search(indicators, keywords=["inequality", "gender"], columns=["indicator_name"])
    """

    if not keywords or (columns is not None and not columns):
        return data.head(0)

    if not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords):
        raise TypeError("`keywords` must be a list of strings.")

    if columns is not None:
        if not isinstance(columns, list) or not all(
            isinstance(c, str) for c in columns
        ):
            raise TypeError("`columns` must be a list of strings or `None`.")
        for col in columns:
            if isinstance(data[col].dtype, (pl.List, pl.Struct)):
                raise ValueError(
                    f"Column '{col}' has unsupported type {data[col].dtype}. Struct or list columns are currently not supported."
                )
        columns_to_search = columns
    else:
        columns_to_search = [
            col
            for col in data.columns
            if not isinstance(data[col].dtype, (pl.List, pl.Struct))
        ]

    conditions = [
        pl.col(col)
        .cast(pl.Utf8)
        .str.contains_any(keywords, ascii_case_insensitive=True)
        for col in columns_to_search
    ]
    data_filtered = data.filter(reduce(lambda acc, cond: acc | cond, conditions))

    return data_filtered
