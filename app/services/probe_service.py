from app.adapters.qbittorrent_client import QBittorrentClient


def handle_probe(user_input: str) -> int:
    value = user_input.strip()

    if not (
        value.startswith("magnet:?")
        or value.startswith("http://")
        or value.startswith("https://")
    ):
        raise ValueError("Probe supports magnet links and torrent URLs.")

    client = QBittorrentClient()
    client.add_magnet(value)

    print("[OK] Torrent input detected")
    print("[OK] Input sent to qBittorrent")
    return 0