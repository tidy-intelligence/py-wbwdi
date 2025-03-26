# py-wbwdi
![PyPI](https://img.shields.io/pypi/v/wbwdi?label=pypi%20package)
![PyPI Downloads](https://img.shields.io/pypi/dm/wbwdi)
[![python-package.yml](https://github.com/tidy-intelligence/py-wbwdi/actions/workflows/python-package.yml/badge.svg)](https://github.com/tidy-intelligence/py-wbwdi/actions/workflows/python-package.yml)
[![codecov.yml](https://codecov.io/gh/tidy-intelligence/py-wbwdi/graph/badge.svg)](https://app.codecov.io/gh/tidy-intelligence/py-wbwdi)
[![License:
MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`wbwdi` is a Polars-based Python library to access and analyze the World Bank’s World Development Indicators (WDI) using the corresponding [API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation). WDI provides more than 24,000 country or region-level indicators for various contexts. `wbwdi` enables users to download, process and work with WDI series across multiple entities and time periods.

This library is a product of Christoph Scheuch and not sponsored by or affiliated with the World Bank in any way. For an R implementation, please consider the [`r-wbwdi`](https://github.com/tidy-intelligence/r-wbwdi) package. For packages with a shared design philosophy, check out the [econdataverse](https://www.econdataverse.org/).

## Installation

You can install the release version from [PyPI](https://pypi.org/project/wbwdi/): 

```python
pip install wbwdi
```

If you want to use the package with `pandas`, then install via:

```python
pip install wbwdi[pandas]
```

You can install the development version from GitHub:

```python
pip install "git+https://github.com/tidy-intelligence/py-wbwdi"
```

## Usage

The main function `wdi_get()` provides an interface to download multiple WDI series for multiple entities and specific date ranges.

```python
import wbwdi as wb

wb.wdi_get(
  entities=["MEX", "CAN", "USA"], 
  indicators=["NY.GDP.PCAP.KD", "SP.POP.TOTL"],
  start_year=2020, 
  end_year=2024
)
```

You can also download these indicators for all entities and available dates:

```python
wb.wdi_get(
  entities="all", 
  indicators=["NY.GDP.PCAP.KD", "SP.POP.TOTL"]
)
```

Some indicators are also available on a monthly basis, e.g.:

```python
wb.wdi_get(
  entities="AUT", 
  indicators="DPANUSSPB",         
  start_year=2012, 
  end_year=2015, 
  frequency="month"
)
```

Similarly, there are also some indicators available on a quarterly frequency, e.g.:

```python
wb.wdi_get(
  entities="NGA", 
  indicators= "DT.DOD.DECT.CD.TL.US",
  start_year=2012, 
  end_year=2015, 
  frequency="quarter"
)
```

You can get a list of all indicators supported by the WDI API via:

```python
wb.wdi_get_indicators()
```

You can get a list of all supported entities via:

```python
wb.wdi_get_entities()
```

You can also get the list of supported indicators and entities in
another language, but note that not everything seems to be translated
into other languages:

```python
wb.wdi_get_indicators(language="es")
wb.wdi_get_entities(language="zh")
```

Check out the following function for a list of supported languages:

```python
wb.wdi_get_languages()
```

In addition, you can list supported regions, sources, topics and lending
types, respectively:

```python
wb.wdi_get_regions()
wb.wdi_get_sources()
wb.wdi_get_topics()
wb.wdi_get_lending_types()
```

If you want to search for specific keywords among indicators or other data sources, you can use the Positron data explorer. Alternatively, this package comes with a helper function:

```python
indicators=wb.wdi_get_indicators()

wb.wdi_search(
  indicators,
  keywords=["inequality", "gender"],
  columns=["indicator_name"]
)
```

If you want to get a `pandas` data frame instead of `polars`, you can use the `to_pandas` option (note that `pandas` and `pyarrow` must be installed):

```python
wb.wdi_get(
  entities=["MEX", "CAN", "USA"], 
  indicators=["NY.GDP.PCAP.KD", "SP.POP.TOTL"],
  start_year=2020, 
  end_year=2024,
  to_pandas=True
)
```

## Relation to Existing Python Libraries

There are already great libraries that allow you to interact with the World Bank WDI API. The two main reasons why this library exists are: (i) to have an implementation based on Polars rather than pandas, and (ii) to have an interface consistent with the [econdataverse](https://www.econdataverse.org/).

- [world-bank-data](https://github.com/mwouts/world_bank_data)
- [wbpy](https://github.com/mattduck/wbpy/)
- [wbdata](https://github.com/oliversherouse/wbdata/)
- [pandas_datareader](https://pandas-datareader.readthedocs.io/en/latest/readers/world-bank.html)
