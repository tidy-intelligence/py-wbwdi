import polars as pl
import pytest
from wbwdi import wdi_search

def test_wdi_search_basic():
    data = pl.DataFrame({
        "indicator_name": ["GDP per capita", "Gender inequality index", "Education index"],
        "description": ["Economic performance", "Social inequality", "Human capital development"]
    })
    result = wdi_search(data, keywords=["inequality", "education"])
    assert result.shape[0] == 2  
    assert "Gender inequality index" in result["indicator_name"].to_list()
    assert "Education index" in result["indicator_name"].to_list()

def test_wdi_search_case_insensitive():
    data = pl.DataFrame({
        "indicator_name": ["GDP per capita", "Gender Inequality Index", "education index"],
        "description": ["Economic performance", "Social inequality", "Human capital development"]
    })
    result = wdi_search(data, keywords=["inequality", "education"])
    assert result.shape[0] == 2 

def test_wdi_search_specific_columns():
    data = pl.DataFrame({
        "indicator_name": ["GDP per capita", "Gender inequality index", "Education index"],
        "description": ["Economic performance", "Social inequality", "Human capital development"]
    })
    result = wdi_search(data, keywords=["inequality"], columns=["indicator_name"])
    assert result.shape[0] == 1 
    assert result["indicator_name"].to_list() == ["Gender inequality index"]

def test_wdi_search_empty_keywords():
    data = pl.DataFrame({
        "indicator_name": ["GDP per capita", "Gender inequality index", "Education index"],
        "description": ["Economic performance", "Social inequality", "Human capital development"]
    })
    result = wdi_search(data, keywords=[])
    assert result.shape[0] == 0 

def test_wdi_search_invalid_keywords_type():
    data = pl.DataFrame({"indicator_name": ["GDP per capita"]})
    with pytest.raises(TypeError):
        wdi_search(data, keywords="inequality")

def test_wdi_search_invalid_columns_type():
    data = pl.DataFrame({"indicator_name": ["GDP per capita"]})
    with pytest.raises(TypeError):
        wdi_search(data, keywords=["inequality"], columns="indicator_name")

def test_wdi_search_unsupported_column_type():
    data = pl.DataFrame({
        "indicator_name": ["GDP per capita", "Gender inequality index"],
        "nested_column": [pl.Series(["A", "B"]), pl.Series(["C", "D"])]
    })
    with pytest.raises(ValueError):
        wdi_search(data, keywords=["inequality"], columns=["nested_column"])
