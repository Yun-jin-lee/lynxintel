from app.adapters.qbittorrent_client import QBittorrentClient


def main() -> None:
    client = QBittorrentClient()
    client.login()
    print("qBittorrent login successful.")


if __name__ == "__main__":
    main()