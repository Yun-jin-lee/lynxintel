from app.adapters.wayback_client import WaybackClient
from app.services.search_service import get_searxng_results


def find_keyword_context(text: str, keyword: str, context_size: int = 100) -> str | None:
    index = text.lower().find(keyword.lower())

    if index == -1:
        return None

    return text[max(0, index - context_size): index + len(keyword) + context_size]


def scan_site(keyword: str, site: str, snapshot_limit: int, client: WaybackClient) -> bool:
    print()
    print("=" * 80)
    print(f"[SITE] {site}")
    print("=" * 80)

    snapshots = client.get_snapshots(site, limit=snapshot_limit)

    if not snapshots:
        print("[INFO] No snapshots found.")
        return False

    found_any = False

    for snapshot in snapshots:
        timestamp = snapshot["timestamp"]
        original_url = snapshot["original_url"]

        print(f"[INFO] Checking snapshot: {timestamp}")

        try:
            text, wayback_url = client.get_snapshot_text(timestamp, original_url)
        except Exception as exc:
            print(f"[SKIP] Could not read snapshot: {exc}")
            continue

        context = find_keyword_context(text, keyword)

        if context:
            print()
            print("[FOUND]")
            print(f"Snapshot: {timestamp}")
            print(f"URL: {wayback_url}")
            print(f"Context: {context}")
            print()

            found_any = True

    if not found_any:
        print("[NOT FOUND] No matching snapshots found for this site.")

    return found_any


def get_sites_from_search(keyword: str, search_limit: int) -> list[str]:
    print("[INFO] No --site provided.")
    print("[INFO] Running SearXNG first to collect candidate URLs.")
    print(f"[INFO] Search limit: {search_limit}")
    print()

    results = get_searxng_results(
        keyword,
        provider="all",
        page=1,
        page_size=search_limit,
    )

    sites = []

    for result in results:
        link = result.get("link")

        if not link:
            continue

        print(f"[SEARCH RESULT] {result.get('title', '<no title>')}")
        print(f"    {link}")

        sites.append(link)

    return sites


def handle_archive_search(
    keyword: str,
    site: str | None = None,
    limit: int = 5,
    search_limit: int = 3,
) -> int:
    client = WaybackClient()

    print("[OK] Archive search started")
    print(f"[INFO] Keyword: {keyword}")
    print(f"[INFO] Snapshot limit per site: {limit}")

    if site:
        print(f"[INFO] Site: {site}")
        found_any = scan_site(keyword, site, limit, client)
    else:
        sites = get_sites_from_search(keyword, search_limit)

        if not sites:
            print("[INFO] No candidate URLs found from SearXNG.")
            return 0

        found_any = False

        for candidate_site in sites:
            try:
                if scan_site(keyword, candidate_site, limit, client):
                    found_any = True
            except Exception as exc:
                print()
                print(f"[SKIP] {candidate_site}")
                print(f"[REASON] {exc}")
                print()
                continue

    print()
    if found_any:
        print("[OK] Archive search completed with matches.")
    else:
        print("[NOT FOUND] Archive search completed without matches.")

    return 0