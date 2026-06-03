# app/services/search_service.py

import requests

from app.adapters.jackett_client import JackettClient
from app.adapters.lynx_client import open_with_lynx
from app.adapters.qbittorrent_client import QBittorrentClient
from app.config import load_config


PAGE_SIZE = 5


def get_searxng_results(keyword: str, provider: str = "all", page: int = 1) -> list[dict]:
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
    for item in raw_results[:PAGE_SIZE]:
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


def get_bittorrent_results(keyword: str) -> list[dict]:
    """Get torrent search results from qBittorrent."""
    client = QBittorrentClient()
    return client.search_torrents(keyword, limit=PAGE_SIZE)


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


def choose_bittorrent_result(keyword: str) -> str:
    """Choose a torrent result and optionally add it to qBittorrent."""
    results = get_bittorrent_results(keyword)

    if not results:
        raise RuntimeError("No torrent results found.")

    print()
    print("[OK] BitTorrent (qBittorrent Search) results")
    print()

    for idx, result in enumerate(results, start=1):
        seeders = result.get("seeders", 0)
        peers = result.get("peers", 0)
        size_str = format_size(result.get("size", 0))
        indexer = result.get("indexer", "Unknown")
        print(f"[{idx}] {result['title']}")
        print(f"    Size: {size_str} | Seeds: {seeders} | Peers: {peers}")
        print(f"    Source: {indexer}")
        print()

    print("Commands: 1-5=add to qBittorrent, o=open in Lynx, q=quit")
    choice = input("Choose: ").strip().lower()

    if choice == "q":
        raise KeyboardInterrupt

    if choice == "o":
        for idx, result in enumerate(results, start=1):
            if result.get("link"):
                return result["link"]
        raise RuntimeError("No valid links found.")

    if choice.isdigit():
        number = int(choice)
        if 1 <= number <= len(results):
            selected = results[number - 1]
            magnet = selected.get("magnet")

            if magnet:
                print(f"[INFO] Adding torrent to qBittorrent: {selected['title']}")
                try:
                    qb_client = QBittorrentClient()
                    qb_client.add_magnet(magnet)
                    print("[OK] Torrent added successfully!")
                    return f"Added: {selected['title']}"
                except Exception as e:
                    print(f"[ERROR] Failed to add torrent: {str(e)}")
                    raise
            else:
                link = selected.get("link", "")
                if link:
                    return link
                raise RuntimeError("No magnet or link available for this torrent.")

    print("[ERROR] Invalid choice.")
    raise ValueError("Invalid choice selected.")


def format_size(bytes_size: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} PB"


def handle_search(user_input: str, provider: str = "all", dump: bool = False) -> int:
    print("[OK] Keyword detected")
    print(f"[INFO] Search query: {user_input}")

    # Determine which search backend to use
    if provider == "torrent":
        print("[INFO] Provider: qBittorrent Search")
        try:
            result = choose_bittorrent_result(user_input)
            if result.startswith("Added:"):
                print(result)
                return 0
            else:
                print()
                print(f"[INFO] Opening selected result: {result}")
                return open_with_lynx(result, dump=dump)
        except Exception as e:
            print(f"[ERROR] qBittorrent search failed: {str(e)}")
            return 1
    else:
        print("[INFO] Provider: SearXNG")
        if provider != "all":
            print(f"[INFO] Engine filter: {provider}")
        try:
            target_url = choose_searxng_result(user_input, provider)
            print()
            print(f"[INFO] Opening selected result: {target_url}")
            return open_with_lynx(target_url, dump=dump)
        except Exception as e:
            print(f"[ERROR] SearXNG search failed: {str(e)}")
            return 1