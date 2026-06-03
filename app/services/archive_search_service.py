from app.adapters.wayback_client import WaybackClient


def handle_archive_search(keyword: str, site: str, limit: int = 5) -> int:
    client = WaybackClient()

    print("[OK] Archive search started")
    print(f"[INFO] Keyword: {keyword}")
    print(f"[INFO] Site: {site}")
    print(f"[INFO] Limit: {limit}")
    print()

    snapshots = client.get_snapshots(site, limit=limit)

    if not snapshots:
        print("[INFO] No snapshots found.")
        return 0

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

        if keyword.lower() in text.lower():
            index = text.lower().find(keyword.lower())
            context = text[max(0, index - 100): index + 150]

            print()
            print("[FOUND]")
            print(f"Snapshot: {timestamp}")
            print(f"URL: {wayback_url}")
            print(f"Context: {context}")
            print()

            found_any = True

    if not found_any:
        print("[NOT FOUND] No matching snapshots found.")

    return 0