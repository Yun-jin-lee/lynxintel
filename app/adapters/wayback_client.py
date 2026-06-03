import requests
from bs4 import BeautifulSoup


class WaybackClient:
    def get_snapshots(self, site: str, limit: int = 5) -> list[dict]:
        response = requests.get(
            "https://web.archive.org/cdx/search/cdx",
            params={
                "url": site,
                "output": "json",
                "filter": "statuscode:200",
                "collapse": "digest",
                "limit": limit,
            },
            timeout=90,
        )
        response.raise_for_status()

        data = response.json()

        snapshots = []
        for row in data[1:]:
            snapshots.append(
                {
                    "timestamp": row[1],
                    "original_url": row[2],
                }
            )

        return snapshots

    def get_snapshot_text(self, timestamp: str, original_url: str) -> tuple[str, str]:
        wayback_url = f"https://web.archive.org/web/{timestamp}id_/{original_url}"

        response = requests.get(wayback_url, timeout=90)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        return text, wayback_url