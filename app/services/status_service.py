from app.adapters.qbittorrent_client import QBittorrentClient


def handle_status() -> int:
    client = QBittorrentClient()
    torrents = client.list_torrents()

    if not torrents:
        print("[INFO] No torrents found in qBittorrent.")
        return 0

    print("[OK] qBittorrent status")
    for idx, torrent in enumerate(torrents, start=1):
        name = torrent.get("name", "<unknown>")
        state = torrent.get("state", "<unknown>")
        progress = round(float(torrent.get("progress", 0)) * 100, 2)
        size = torrent.get("size", 0)

        print(f"[{idx}] {name}")
        print(f"     state: {state}")
        print(f"     progress: {progress}%")
        print(f"     size: {size}")
        print()

    return 0