from urllib.parse import quote_plus

import requests

from app.adapters.lynx_client import open_with_lynx
from app.config import load_config


def build_search_url(keyword: str, provider: str) -> str:
    query = quote_plus(keyword)
    provider = provider.lower()

    if provider == "ddg":
        return f"https://lite.duckduckgo.com/lite/?q={query}"

    if provider == "baidu":
        return f"https://www.baidu.com/s?wd={query}"

    raise ValueError("Direct URL building is only used for ddg and baidu.")


def search_with_serpapi(keyword: str, provider: str) -> str:
    config = load_config()

    if not config.serpapi_api_key:
        raise ValueError("SERPAPI_API_KEY is not set in .env.")

    provider = provider.lower()

    if provider == "google":
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": config.serpapi_api_key,
        }

    elif provider == "yandex":
        params = {
            "engine": "yandex",
            "text": keyword,
            "yandex_domain": "yandex.com",
            "lang": "en",
            "api_key": config.serpapi_api_key,
        }

    else:
        raise ValueError("SerpApi search supports only google and yandex.")

    response = requests.get(
        "https://serpapi.com/search.json",
        params=params,
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()
    organic_results = data.get("organic_results", [])

    if not organic_results:
        raise RuntimeError(f"No {provider} results returned by SerpApi.")

    first_result = organic_results[0].get("link")
    if not first_result:
        raise RuntimeError(f"Top {provider} result did not contain a usable link.")

    return first_result


def handle_search(user_input: str, provider: str = "ddg", dump: bool = False) -> int:
    provider = provider.lower()

    print("[OK] Keyword detected")
    print(f"[INFO] Provider: {provider}")
    print(f"[INFO] Search query: {user_input}")

    if provider in {"google", "yandex"}:
        print("[INFO] External provider selected through SerpApi.")
        print("[INFO] This may reduce privacy compared to the default provider.")
        target_url = search_with_serpapi(user_input, provider)
        print(f"[INFO] Top result URL: {target_url}")
        return open_with_lynx(target_url, dump=dump)

    search_url = build_search_url(user_input, provider)
    print(f"[INFO] Search URL: {search_url}")

    if provider != "ddg":
        print("[INFO] External provider selected.")
        print("[INFO] This may reduce privacy and may be blocked by the provider.")

    return open_with_lynx(search_url, dump=dump)