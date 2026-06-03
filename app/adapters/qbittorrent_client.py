# app/adapters/qbittorrent_client.py

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

    def search_torrents(self, keyword: str, limit: int = 5) -> list[dict]:
        """Search torrents using qBittorrent's search plugins."""
        self.login()
        
        response = self.session.post(
            f"{self.base_url}/api/v2/search/start",
            data={
                "pattern": keyword,
                "plugins": "all",
                "category": "all",
            },
            timeout=30,
        )
        response.raise_for_status()
        
        search_id = response.json().get("id")
        if not search_id:
            raise RuntimeError("Failed to start search in qBittorrent.")
        
        # Get search results
        results_response = self.session.get(
            f"{self.base_url}/api/v2/search/results",
            params={
                "id": search_id,
                "limit": limit,
            },
            timeout=15,
        )
        results_response.raise_for_status()
        
        raw_results = results_response.json().get("results", [])
        
        cleaned_results = []
        for item in raw_results:
            cleaned_results.append(
                {
                    "title": item.get("title", "<no title>"),
                    "link": item.get("link", ""),
                    "magnet": item.get("magnet", ""),
                    "seeders": item.get("seeders", 0),
                    "peers": item.get("peers", 0),
                    "size": item.get("fileSize", 0),
                    "indexer": item.get("engine_url", "qBittorrent"),
                }
            )
        
        return cleaned_results

    def list_torrents(self) -> list[dict]:
        self.login()
        response = self.session.get(
            f"{self.base_url}/api/v2/torrents/info",
            timeout=15,
        )
        response.raise_for_status()
        return response.json()