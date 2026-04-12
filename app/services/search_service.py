from urllib.parse import quote_plus

from app.adapters.lynx_client import open_with_lynx


def build_search_url(keyword: str, provider: str) -> str:
    query = quote_plus(keyword)

    provider = provider.lower()

    if provider == "ddg":
        return f"https://lite.duckduckgo.com/lite/?q={query}"

    if provider == "google":
        return f"https://www.google.com/search?q={query}"

    if provider == "yandex":
        return f"https://yandex.com/search/?text={query}"

    if provider == "baidu":
        return f"https://www.baidu.com/s?wd={query}"

    raise ValueError(
        "Unsupported provider. Choose one of: ddg, google, yandex, baidu."
    )


def handle_search(user_input: str, provider: str = "ddg", dump: bool = False) -> int:
    search_url = build_search_url(user_input, provider)

    print("[OK] Keyword detected")
    print(f"[INFO] Provider: {provider}")
    print(f"[INFO] Search query: {user_input}")
    print(f"[INFO] Search URL: {search_url}")

    if provider != "ddg":
        print("[INFO] External provider selected.")
        print("[INFO] This may reduce privacy and may be blocked by the provider.")

    return open_with_lynx(search_url, dump=dump)