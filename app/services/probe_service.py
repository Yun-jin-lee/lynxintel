from app.adapters.qbittorrent_client import QBittorrentClient


def handle_probe(user_input: str) -> int:
    magnet = user_input.strip()

    if not magnet.startswith("magnet:?"):
        raise ValueError("Probe currently supports magnet links only.")

    client = QBittorrentClient()
    client.add_magnet(magnet)

    print("[OK] Magnet detected")
    print("[OK] Magnet added to qBittorrent")
    return 0