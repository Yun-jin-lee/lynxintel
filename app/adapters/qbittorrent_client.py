import time
from typing import Any

import requests

from app.config import (
    get_qbittorrent_base_url,
    get_qbittorrent_password,
    get_qbittorrent_username,
)


class QBittorrentClient:
    def __init__(self) -> None:
        self.base_url = get_qbittorrent_base_url()
        self.username = get_qbittorrent_username()
        self.password = get_qbittorrent_password()
        self.session = requests.Session()

    def login(self) -> None:
        url = f"{self.base_url}/api/v2/auth/login"
        response = self.session.post(
            url,
            data={"username": self.username, "password": self.password},
            timeout=15,
        )
        response.raise_for_status()

        if response.text.strip() != "Ok.":
            raise RuntimeError("qBittorrent login failed.")

    def add_magnet(self, magnet_uri: str, paused: bool = True) -> None:
        url = f"{self.base_url}/api/v2/torrents/add"
        response = self.session.post(
            url,
            data={
                "urls": magnet_uri,
                "paused": "true" if paused else "false",
            },
            timeout=20,
        )
        response.raise_for_status()

    def list_torrents(self) -> list[dict[str, Any]]:
        url = f"{self.base_url}/api/v2/torrents/info"
        response = self.session.get(url, timeout=20)
        response.raise_for_status()
        return response.json()

    def list_files(self, torrent_hash: str) -> list[dict[str, Any]]:
        url = f"{self.base_url}/api/v2/torrents/files"
        response = self.session.get(url, params={"hash": torrent_hash}, timeout=20)
        response.raise_for_status()
        return response.json()

    def delete_torrent(self, torrent_hash: str, delete_files: bool = False) -> None:
        url = f"{self.base_url}/api/v2/torrents/delete"
        response = self.session.post(
            url,
            data={
                "hashes": torrent_hash,
                "deleteFiles": "true" if delete_files else "false",
            },
            timeout=20,
        )
        response.raise_for_status()

    def find_torrent_by_btih(
        self,
        btih: str,
        retries: int = 10,
        delay: float = 1.5,
    ) -> dict[str, Any] | None:
        btih_lower = btih.lower()

        for _ in range(retries):
            torrents = self.list_torrents()
            for torrent in torrents:
                torrent_hash = str(torrent.get("hash", "")).lower()
                if torrent_hash == btih_lower:
                    return torrent
            time.sleep(delay)

        return None