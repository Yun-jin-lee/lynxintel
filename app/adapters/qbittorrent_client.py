from __future__ import annotations

import requests

from app.config import load_config


class QBittorrentClient:
    def __init__(self) -> None:
        config = load_config()
        self.base_url = config.qbittorrent_url.rstrip("/")
        self.username = config.qbittorrent_username
        self.password = config.qbittorrent_password
        self.session = requests.Session()

    def login(self) -> None:
        response = self.session.post(
            f"{self.base_url}/api/v2/auth/login",
            data={
                "username": self.username,
                "password": self.password,
            },
            timeout=15,
        )
        response.raise_for_status()

        if response.text.strip() != "Ok.":
            raise RuntimeError("qBittorrent login failed. Check credentials in .env.")

    def add_magnet(self, magnet: str) -> None:
        self.login()
        response = self.session.post(
            f"{self.base_url}/api/v2/torrents/add",
            data={"urls": magnet},
            timeout=15,
        )
        response.raise_for_status()

    def list_torrents(self) -> list[dict]:
        self.login()
        response = self.session.get(
            f"{self.base_url}/api/v2/torrents/info",
            timeout=15,
        )
        response.raise_for_status()
        return response.json()