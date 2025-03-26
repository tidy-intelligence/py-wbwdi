import importlib.util


def is_module_available(module_name):
    """Check if a module can be imported without importing it."""
    return importlib.util.find_spec(module_name) is not None


def convert_to_pandas(df):
    if not is_module_available("pandas"):  # pragma: no cover
        raise ImportError(
            "`pandas` is required for `to_pandas=True`. "
            "Install it with: `pip install pandas`."
        )
    if not is_module_available("pyarrow"):  # pragma: no cover
        raise ImportError(
            "`pyarrow` is required for `to_pandas=True`. "
            "Install it with: `pip install pyarrow`."
        )
    return df.to_pandas()
