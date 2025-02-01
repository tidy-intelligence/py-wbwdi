# py-wbwdi
![PyPI](https://img.shields.io/pypi/v/wbwdi?label=pypi%20package)
![PyPI Downloads](https://img.shields.io/pypi/dm/wbwdi)
[![python-package.yml](https://github.com/tidy-finance/py-wbwdi/actions/workflows/python-package.yml/badge.svg)](https://github.com/tidy-finance/py-wbwdi/actions/workflows/python-package.yml)
[![codecov.yml](https://codecov.io/gh/tidy-finance/py-wbwdi/graph/badge.svg)](https://app.codecov.io/gh/tidy-finance/py-wbwdi)
[![License:
MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`wbwdi` is a Polars-based Python library to access and analyze the World Bank’s World Development Indicators (WDI) using the corresponding [API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation). WDI provides more than 24,000 country or region-level indicators for various contexts. `wbwdi` enables users to download, process and work with WDI series across multiple geographies and time periods.

This library is a product of Christoph Scheuch and not sponsored by or affiliated with the World Bank in any way. For an R implementation, please consider the [`r-wbwdi`](https://github.com/tidy-intelligence/r-wbwdi) package.

## Installation

<!-- You can install the release version from PyPI: 

```python
pip install wbwdi
``` -->

You can install the development version from GitHub:

```python
pip install "git+https://github.com/tidy-intelligence/py-wbwdi"
```

## Usage

The main function `wdi_get()` provides an interface to download multiple WDI series for multiple geographies and specific date ranges.

```python
from wbwdi import wdi_get

wdi_get(
  geographies = ["MX", "CA", "US"], 
  indicators = ["NY.GDP.PCAP.KD", "SP.POP.TOTL"],
  start_year = 2020, end_year = 2024
)
```

You can also download these indicators for all geographies and available dates:

```python
wdi_get(
  geographies = "all", 
  indicators = ["NY.GDP.PCAP.KD", "SP.POP.TOTL"]
)
```

Some indicators are also available on a monthly basis, e.g.:

```python
wdi_get(
  geographies = "AUT", 
  indicators = "DPANUSSPB",         
  start_year = 2012, end_year = 2015, 
  frequency = "month"
)
```

Similarly, there are also some indicators available on a quarterly frequency, e.g.:

```python
wdi_get(
  geographies = "NGA", 
  indicators =  "DT.DOD.DECT.CD.TL.US",
  start_year = 2012, end_year = 2015, 
  frequency = "quarter"
)
```

You can get a list of all indicators supported by the WDI API via:

```python
from wbwdi import wdi_get_indicators

wdi_get_indicators()
```

You can get a list of all supported geographies via:

```python
from wbwdi import wdi_get_geographies

wdi_get_geographies()
```

You can also get the list of supported indicators and geographies in
another language, but note that not everything seems to be translated
into other languages:

```python
wdi_get_indicators(language = "es")
wdi_get_geographies(language = "zh")
```

Check out the following function for a list of supported languages:

```python
from wbwdi import wdi_get_languages

wdi_get_languages()
```

In addition, you can list supported regions, sources, topics and lending
types, respectively:

```python
from wbwdi import wdi_get_regions, wdi_get_sources, wdi_get_topics, wdi_get_lending_types

wdi_get_regions()
wdi_get_sources()
wdi_get_topics()
wdi_get_lending_types()
```

If you want to search for specific keywords among indicators or other data sources, you can use the Positron data explorer. Alternatively, this package comes with a helper function:

```python
from wbwdi import wdi_get_indicators, wdi_search

indicators = wdi_get_indicators()

wdi_search(
  indicators,
  keywords = ["inequality", "gender"],
  columns = ["indicator_name"]
)
```

## Relation to Existing Libraries

There are already great libraries that allow you to interact with the World Bank WDI API. The two main reasons why this library exists are: (i) to have an implementation based on Polars rather than pandas, and (ii) to have an interface consistent with the [econdataverse](https://www.econdataverse.org/).

- [world-bank-data](https://github.com/mwouts/world_bank_data)
- [wbpy](https://github.com/mattduck/wbpy/)
- [wbdata](https://github.com/oliversherouse/wbdata/)
- [pandas_datareader](https://pandas-datareader.readthedocs.io/en/latest/readers/world-bank.html)

## Contributing

Feel free to open issues or submit pull requests to improve the package. Contributions are welcome!

## License

This package is licensed under the MIT License.