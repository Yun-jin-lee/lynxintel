from urllib.parse import quote_plus

import requests

from app.adapters.lynx_client import open_with_lynx
from app.config import load_config


PAGE_SIZE = 5


def build_search_url(keyword: str, provider: str) -> str:
    query = quote_plus(keyword)
    provider = provider.lower()

    if provider == "ddg":
        return f"https://lite.duckduckgo.com/lite/?q={query}"

    if provider == "baidu":
        return f"https://www.baidu.com/s?wd={query}"

    raise ValueError("Direct URL building is only used for ddg and baidu.")


def get_serpapi_results(keyword: str, provider: str, page: int = 1) -> list[dict]:
    config = load_config()

    if not config.serpapi_api_key:
        raise ValueError("SERPAPI_API_KEY is not set in .env.")

    provider = provider.lower()

    if provider == "google":
        params = {
            "engine": "google",
            "q": keyword,
            "start": (page - 1) * PAGE_SIZE,
            "num": PAGE_SIZE,
            "api_key": config.serpapi_api_key,
        }

    elif provider == "yandex":
        params = {
            "engine": "yandex",
            "text": keyword,
            "p": page - 1,
            "yandex_domain": "yandex.com",
            "lang": "en",
            "api_key": config.serpapi_api_key,
        }

    else:
        raise ValueError("SerpApi supports only google and yandex in this flow.")

    response = requests.get(
        "https://serpapi.com/search.json",
        params=params,
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()
    organic_results = data.get("organic_results", [])

    results: list[dict] = []
    for item in organic_results[:PAGE_SIZE]:
        link = item.get("link")
        if not link:
            continue

        results.append(
            {
                "title": item.get("title") or "<no title>",
                "link": link,
                "snippet": item.get("snippet") or "",
            }
        )

    return results


def choose_serpapi_result(keyword: str, provider: str) -> str:
    page = 1

    while True:
        results = get_serpapi_results(keyword, provider, page=page)

        if not results:
            if page == 1:
                raise RuntimeError(f"No usable {provider} results returned.")
            print("[INFO] No more results.")
            page -= 1
            continue

        print()
        print(f"[OK] {provider.capitalize()} results - page {page}")
        print()

        for idx, result in enumerate(results, start=1):
            print(f"[{idx}] {result['title']}")
            print(f"    {result['link']}")
            if result["snippet"]:
                print(f"    {result['snippet']}")
            print()

        print("Commands: 1-5=open, n=next page, p=previous page, q=quit")
        choice = input("Choose: ").strip().lower()

        if choice == "q":
            raise KeyboardInterrupt

        if choice == "n":
            page += 1
            continue

        if choice == "p":
            if page > 1:
                page -= 1
            else:
                print("[INFO] Already on the first page.")
            continue

        if choice.isdigit():
            number = int(choice)
            if 1 <= number <= len(results):
                return results[number - 1]["link"]

        print("[ERROR] Invalid choice.")


def handle_search(user_input: str, provider: str = "ddg", dump: bool = False) -> int:
    provider = provider.lower()

    print("[OK] Keyword detected")
    print(f"[INFO] Provider: {provider}")
    print(f"[INFO] Search query: {user_input}")

    if provider in {"google", "yandex"}:
        print("[INFO] External provider selected through SerpApi.")
        print("[INFO] This may reduce privacy compared to the default provider.")

        target_url = choose_serpapi_result(user_input, provider)

        print()
        print(f"[INFO] Opening selected result: {target_url}")
        return open_with_lynx(target_url, dump=dump)

    search_url = build_search_url(user_input, provider)
    print(f"[INFO] Search URL: {search_url}")

    if provider != "ddg":
        print("[INFO] External provider selected.")
        print("[INFO] This may reduce privacy and may be blocked by the provider.")

    return open_with_lynx(search_url, dump=dump)