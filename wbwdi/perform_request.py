import httpx
from typing import List, Optional, Union
import sys

def perform_request(
    resource: str,
    language: Optional[str] = None,
    per_page: int = 1000,
    date: Optional[str] = None,
    most_recent_only: bool = False,
    source: Optional[str] = None,
    progress: bool = False,
    base_url: str = "https://api.worldbank.org/v2/"
) -> Union[List[dict], None]:
    """
    Perform a request to the World Bank API with optional parameters for pagination,
    language, date range, data source, and progress tracking.
    
    This function constructs a request URL for the specified World Bank API resource and 
    retrieves data as a JSON list. It supports paginated requests and optional progress 
    tracking to provide feedback for multi-page responses.
    
    Parameters:
    ----------
    resource : str
        The endpoint for the World Bank API resource (e.g., "incomeLevels", "lendingTypes").
    language : Optional[str], default=None
        The language code for the API response.
    per_page : int, default=1000
        The number of results per page for the API. Must be between 1 and 32,500.
    date : Optional[str], default=None
        Date range of data to retrieve (e.g., "2000:2020"). If None, no date filtering is applied.
    source : Optional[str], default=None
        Specific data source for the API request. If None, no specific source is selected.
    progress : bool, default=False
        Whether to display a progress bar for paginated requests.
    base_url : str, default="https://api.worldbank.org/v2/"
        The base URL of the World Bank API.

    Returns:
    -------
    Union[List[dict], None]
        A list of JSON objects containing the API response data. If paginated, consolidates 
        all pages into a single list. Returns None if an error occurs.

    Notes:
    ------
    - The function validates the `per_page` parameter.
    - Handles errors with descriptive messages when the API returns an error.
    - For paginated results, iterates through all pages to gather complete data.

    Raises:
    ------
    ValueError
        If `per_page` is not an integer between 1 and 32,500.
    """
    
    validate_per_page(per_page)

    url = create_request_url(base_url, resource, language, per_page, date, most_recent_only, source)

    headers={"User-Agent": "wbwdi Python library (https://github.com/tidy-intelligence/py-wbwdi)"}

    with httpx.Client() as client:
        response = client.get(url, headers=headers)
        if is_request_error(response):
            handle_request_error(response)

        body = response.json()
        pages = int(body[0]["pages"])
        
        if pages == 1:
            return body[1]
        else:
            results = []
            for page in range(1, pages + 1):
                paginated_url = f"{url}&page={page}"
                page_response = client.get(paginated_url)
                if progress:
                    print_progress(page, pages)
                results.extend(page_response.json()[1])
            return results

def validate_per_page(per_page: int):
    if not isinstance(per_page, int) or not (1 <= per_page <= 32500):
        raise ValueError("`per_page` must be an integer between 1 and 32,500.")

def create_request_url(
    base_url: str, resource: str, language: Optional[str],
    per_page: int, date: Optional[str], most_recent_only: Optional[bool], source: Optional[str]
) -> str:
    if language:
        url = f"{base_url}{language}/{resource}?format=json&per_page={str(per_page)}"
    else:
        url = f"{base_url}{resource}?format=json&per_page={str(per_page)}"
    if most_recent_only:
        url += f"&mrv=1"
    if date:
        url += f"&date={str(date)}"
    if source:
        url += f"&source={str(source)}"
    return url

def is_request_error(response: httpx.Response) -> bool:
    if response.status_code >= 400:
        return True
    body = response.json()
    if len(body) == 1 and "message" in body[0]:
        return True
    return False

def check_for_body_error(response: httpx.Response) -> List[str]:
    if "application/json" in response.headers.get("Content-Type", ""):
        body = response.json()
        message_id = body[0]["message"][0]["id"]
        message_value = body[0]["message"][0]["value"]
        docs = (
            "Read more at <https://datahelpdesk.worldbank.org/"
            "knowledgebase/articles/898620-api-error-codes>"
        )
        return [f"Error code: {message_id}", message_value, docs]
    return []

def handle_request_error(response: httpx.Response):
    error_body = check_for_body_error(response)
    raise RuntimeError("\n".join(error_body))

def print_progress(current: int, total: int):
    print(f"Progress: {current}/{total}", end='\r')
    