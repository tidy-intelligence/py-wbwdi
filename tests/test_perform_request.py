import pytest
import httpx
from pytest_httpx import HTTPXMock
import json
from typing import List, Dict, Any

from wbwdi.perform_request import (
    perform_request,
    validate_per_page,
    create_request_url,
    is_request_error,
    check_for_body_error,
    handle_request_error,
    print_progress
)

# Test perform_request function
def test_perform_request_single_page(httpx_mock: HTTPXMock):
    """Test successful single page request"""
    single_page_response = [
        {"page": 1, "pages": 1, "per_page": 1000, "total": 2},
        [
            {"id": "HIC", "name": "High income"},
            {"id": "LIC", "name": "Low income"}
        ]
    ]
    httpx_mock.add_response(
        method="GET",
        url="https://api.worldbank.org/v2/incomeLevels?format=json&per_page=1000",
        json=single_page_response,
        headers={"Content-Type": "application/json"}
    )
    
    result = perform_request("incomeLevels")
    assert len(result) == 2
    assert result[0]["id"] == "HIC"
    assert result[1]["id"] == "LIC"

def test_perform_request_with_options():
    """Test request URL construction with all optional parameters"""
    url = create_request_url(
        "https://api.worldbank.org/v2/",
        "incomeLevels",
        "en",
        1000,
        "2020:2022",
        "2"
    )
    expected = "https://api.worldbank.org/v2/en/incomeLevels?format=json&per_page=1000&date=2020:2022&source=2"
    assert url == expected

def test_validate_per_page_valid():
    """Test valid per_page values"""
    validate_per_page(1)
    validate_per_page(1000)
    validate_per_page(32500)

def test_validate_per_page_invalid():
    """Test invalid per_page values"""
    with pytest.raises(ValueError):
        validate_per_page(0)
    with pytest.raises(ValueError):
        validate_per_page(32501)
    with pytest.raises(ValueError):
        validate_per_page("1000")
    
def test_is_request_error(httpx_mock: HTTPXMock):
    """Test error detection in responses"""
    # Test status code error
    httpx_mock.add_response(
        status_code=404
    )

    with httpx.Client() as client:
        with pytest.raises(RuntimeError) as exc_info:
            perform_request(resource="invalid-resource")
    
def test_print_progress(capsys):
    """Test progress printing functionality"""
    print_progress(1, 10)
    captured = capsys.readouterr()
    assert "Progress: 1/10" in captured.out

def test_multiple_pages():
    perform_request("languages", per_page = 5)

def test_print_progress2():
    perform_request("languages", per_page = 5, progress=True)

def test_error_handling(httpx_mock: HTTPXMock):
    example_body = [
        {"message": [
            {
                "id": "120",
                "key": "Invalid value",
                "value": "The provided parameter value is not valid"
            }
        ]}
    ]

    httpx_mock.add_response(status_code = 200, json=example_body)

    with httpx.Client() as client:
        with pytest.raises(RuntimeError) as exc_info:
            perform_request("invalid_resource")
        assert "Error code: 120" in str(exc_info.value)
    
def test_error_handling2(httpx_mock: HTTPXMock):
    example_body = [
        {"message": [
            {
                "id": "120",
                "key": "Invalid value",
                "value": "The provided parameter value is not valid"
            }
        ]}
    ]

    httpx_mock.add_response(status_code=404, json=example_body)

    with httpx.Client() as client:
        with pytest.raises(RuntimeError) as exc_info:
            perform_request("invalid_resource")
        assert "Error code: 120" in str(exc_info.value)
    