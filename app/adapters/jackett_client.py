from __future__ import annotations

import requests

from app.config import load_config


class JackettClient:
    def __init__(self) -> None:
        config = load_config()
        self.base_url = config.jackett_url.rstrip("/")
        self.api_key = config.jackett_api_key
        self.session = requests.Session()

    def search(self, keyword: str, limit: int = 5) -> list[dict]:
        """
        Search for torrents via Jackett.
        Returns a list of torrent results with title, link, and magnet.
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/v2.0/indexers/all/results",
                params={
                    "apikey": self.api_key,
                    "Query": keyword,
                    "Limit": limit,
                },
                timeout=30,
            )
            response.raise_for_status()
            
            data = response.json()
            results = data.get("Results", [])
            
            cleaned_results: list[dict] = []
            for item in results[:limit]:
                cleaned_results.append(
                    {
                        "title": item.get("Title", "<no title>"),
                        "link": item.get("Link", ""),
                        "magnet": item.get("MagnetUri", ""),
                        "seeders": item.get("Seeders", 0),
                        "peers": item.get("Peers", 0),
                        "size": item.get("Size", 0),
                        "indexer": item.get("Tracker", ""),
                    }
                )
            
            return cleaned_results
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Jackett search failed: {str(e)}")
