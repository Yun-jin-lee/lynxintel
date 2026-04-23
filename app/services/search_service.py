import requests
from urllib.parse import urlparse, urlunparse

from app.adapters.lynx_client import open_with_lynx
from app.config import load_config


PAGE_SIZE = 5
UNIQUE_PAGE_SIZE = 10
COMPARE_ENGINES = ["google", "yandex", "baidu"]


def normalize_search_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if not parsed.scheme:
        parsed = parsed._replace(scheme="http")

    normalized = parsed._replace(
        netloc=parsed.netloc.lower(),
        path=parsed.path.rstrip("/"),
        params="",
        query="",
        fragment="",
    )
    return urlunparse(normalized)


def get_searxng_results(keyword: str, provider: str = "all", page: int = 1, page_size: int = PAGE_SIZE) -> list[dict]:
    config = load_config()

    params = {
        "q": keyword,
        "format": "json",
        "pageno": page,
    }

    if provider != "all":
        params["engines"] = provider

    response = requests.get(
        f"{config.searxng_url}/search",
        params=params,
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()
    raw_results = data.get("results", [])

    cleaned_results: list[dict] = []
    for item in raw_results[:page_size]:
        url = item.get("url")
        if not url:
            continue

        cleaned_results.append(
            {
                "title": item.get("title") or "<no title>",
                "link": url,
                "snippet": item.get("content") or "",
                "engine": item.get("engine") or "",
            }
        )

    return cleaned_results


def get_searxng_comparison(keyword: str, page: int = 1, page_size: int = UNIQUE_PAGE_SIZE) -> dict[str, list[dict]]:
    comparison_results: dict[str, list[dict]] = {}
    for engine in COMPARE_ENGINES:
        comparison_results[engine] = get_searxng_results(
            keyword, provider=engine, page=page, page_size=page_size
        )
    return comparison_results


def build_result_key(result: dict) -> str:
    return normalize_search_url(result["link"])


def find_unique_delta(engine_results: dict[str, list[dict]]) -> tuple[dict[str, list[dict]], list[tuple[set[str], dict]]]:
    seen_results: dict[str, dict] = {}
    result_engines: dict[str, set[str]] = {}

    for engine, results in engine_results.items():
        for result in results:
            key = build_result_key(result)
            if key not in seen_results:
                seen_results[key] = result
                result_engines[key] = set()
            result_engines[key].add(engine)

    unique_by_engine: dict[str, list[dict]] = {engine: [] for engine in engine_results}
    shared_results: list[tuple[set[str], dict]] = []

    for key, engines in result_engines.items():
        representative = seen_results[key]
        if len(engines) == 1:
            engine = next(iter(engines))
            unique_by_engine[engine].append(representative)
        else:
            shared_results.append((engines, representative))

    return unique_by_engine, shared_results


def print_search_delta(keyword: str, engine_results: dict[str, list[dict]]) -> None:
    unique_by_engine, shared_results = find_unique_delta(engine_results)

    print()
    print(f"[OK] SearXNG unique comparison for query: '{keyword}'")
    print(f"[INFO] Compared engines: {', '.join(engine_results)}")
    print(f"[INFO] Each engine first page size: {UNIQUE_PAGE_SIZE}")
    print()

    for engine, results in engine_results.items():
        print(f"[ENGINE] {engine} ({len(results)} results)")
        for idx, result in enumerate(results, start=1):
            print(f"  {idx}. {result['title']}")
            print(f"       {result['link']}")
            if result["snippet"]:
                print(f"       {result['snippet']}")
        print()

    for engine, unique_results in unique_by_engine.items():
        print(f"[UNIQUE] Results only found by {engine} ({len(unique_results)} items)")
        if unique_results:
            for idx, result in enumerate(unique_results, start=1):
                print(f"  {idx}. {result['title']}")
                print(f"       {result['link']}")
            print()
        else:
            print("  None\n")

    if shared_results:
        print(f"[COMMON] Results found by multiple engines ({len(shared_results)} items)")
        for engines, result in shared_results:
            engines_label = ", ".join(sorted(engines))
            print(f"  - {result['title']} [{engines_label}]")
            print(f"       {result['link']}")
        print()
    else:
        print("[COMMON] No overlapping results found among engines.")
        print()


def choose_searxng_result(keyword: str, provider: str) -> str:
    page = 1

    while True:
        results = get_searxng_results(keyword, provider=provider, page=page)

        if not results:
            if page == 1:
                raise RuntimeError(f"No usable results returned for provider '{provider}'.")
            print("[INFO] No more results.")
            page -= 1
            continue

        print()
        print(f"[OK] SearXNG results - page {page}")
        if provider != "all":
            print(f"[INFO] Engine filter: {provider}")
        print()

        for idx, result in enumerate(results, start=1):
            engine_label = f" [{result['engine']}]" if result["engine"] else ""
            print(f"[{idx}] {result['title']}{engine_label}")
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


def handle_search(user_input: str, provider: str = "all", dump: bool = False, unique: bool = False) -> int:
    print("[OK] Keyword detected")
    print("[INFO] Provider: searxng")
    print(f"[INFO] Search query: {user_input}")

    if unique:
        if provider != "all":
            raise ValueError("--unique can only be used with --provider all because it compares multiple engines.")

        engine_results = get_searxng_comparison(user_input)
        print_search_delta(user_input, engine_results)
        return 0

    if provider != "all":
        print(f"[INFO] Engine filter: {provider}")

    target_url = choose_searxng_result(user_input, provider)

    print()
    print(f"[INFO] Opening selected result: {target_url}")
    return open_with_lynx(target_url, dump=dump)