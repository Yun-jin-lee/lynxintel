from app.core.query_builder import (
    build_baidu_query,
    build_baidu_search_url,
    build_google_query,
    build_google_search_url,
    build_yandex_query,
    build_yandex_search_url,
)
from app.core.search_models import SearchRequest


def build_provider_comparison(request: SearchRequest) -> dict:
    google_query = build_google_query(request)
    yandex_query = build_yandex_query(request)
    baidu_query = build_baidu_query(request)

    return {
        "status": "ok",
        "adapter": "comparison_builder",
        "provider": "comparison",
        "use_case": request.use_case,
        "keyword": request.keyword,
        "message": "Built comparison output for Google, Yandex, and Baidu.",
        "filters": {
            "site": request.site,
            "filetype": request.filetype,
            "exact_phrase": request.exact_phrase,
            "exclude_terms": request.exclude_terms,
            "additional_terms": request.additional_terms,
            "language": request.language,
            "region": request.region,
        },
        "comparisons": {
            "google": {
                "query": google_query,
                "manual_search_url": build_google_search_url(google_query),
            },
            "yandex": {
                "query": yandex_query,
                "manual_search_url": build_yandex_search_url(yandex_query),
            },
            "baidu": {
                "query": baidu_query,
                "manual_search_url": build_baidu_search_url(baidu_query),
            },
        },
    }