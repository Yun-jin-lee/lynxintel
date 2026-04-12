from urllib.parse import quote_plus

from app.adapters.lynx_client import open_with_lynx


def handle_search(user_input: str, dump: bool = False) -> int:
    query = quote_plus(user_input)
    # DuckDuckGo Lite works much better with text browsers than Google/Yandex.
    search_url = f"https://lite.duckduckgo.com/lite/?q={query}"

    print("[OK] Keyword detected")
    print(f"[INFO] Search query: {user_input}")
    print(f"[INFO] Search URL: {search_url}")

    return open_with_lynx(search_url, dump=dump)