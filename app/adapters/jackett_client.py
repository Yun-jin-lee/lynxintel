from typing import Any

import requests

from app.config import (
    get_jackett_api_key,
    get_jackett_base_url,
    get_jackett_indexer,
)


def run_keyword_search(keyword: str) -> dict[str, Any]:
    """
    Run a basic keyword search against a Jackett instance using the Torznab API.
    """
    base_url = get_jackett_base_url()
    api_key = get_jackett_api_key()
    indexer = get_jackett_indexer()

    if not api_key or api_key == "your_jackett_api_key_here":
        return {
            "status": "error",
            "input_type": "keyword",
            "value": keyword,
            "adapter": "jackett_client",
            "message": "Missing or placeholder JACKETT_API_KEY in environment.",
        }

    url = f"{base_url}/api/v2.0/indexers/{indexer}/results/torznab/api"
    params = {
        "apikey": api_key,
        "t": "search",
        "q": keyword,
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
    except requests.RequestException as exc:
        return {
            "status": "error",
            "input_type": "keyword",
            "value": keyword,
            "adapter": "jackett_client",
            "message": f"Jackett request failed: {exc}",
        }

    return {
        "status": "ok",
        "input_type": "keyword",
        "value": keyword,
        "adapter": "jackett_client",
        "message": "Jackett search request completed successfully.",
        "request_url": response.url,
        "http_status": response.status_code,
        "response_preview": response.text[:500],
    }