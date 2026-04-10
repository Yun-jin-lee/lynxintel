import os

import requests

from app.core.query_builder import build_google_query, build_google_search_url
from app.core.search_models import SearchRequest, SearchResult


def run_google_search(request: SearchRequest) -> dict:
    query = build_google_query(request)
    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        return {"status": "error", "message": "SERPAPI_KEY missing"}

    # Perform the API request FIRST
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    # Extract results
    organic_results = data.get("organic_results", [])

    # Build final SearchResult (success)
    result = SearchResult(
        status="success",
        provider="google",
        adapter="google_search_client",
        use_case=request.use_case,
        query=query,
        manual_search_url=build_google_search_url(query),
        message="Google search completed successfully using SerpAPI.",
        filters={
            "site": request.site,
            "filetype": request.filetype,
            "exact_phrase": request.exact_phrase,
            "exclude_terms": request.exclude_terms,
            "additional_terms": request.additional_terms,
            "language": request.language,
            "region": request.region,
        },
        results=organic_results,
        raw=data
    )

    return result.__dict__