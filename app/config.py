import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class AppConfig:
    lynx_bin: str
    qbittorrent_url: str
    qbittorrent_username: str
    qbittorrent_password: str
    serpapi_api_key: str | None = None


def load_config() -> AppConfig:
    return AppConfig(
        lynx_bin=os.getenv("LYNX_BIN", "lynx"),
        qbittorrent_url=os.getenv("QBITTORRENT_URL", "http://127.0.0.1:8080").rstrip("/"),
        qbittorrent_username=os.getenv("QBITTORRENT_USERNAME", "admin"),
        qbittorrent_password=os.getenv("QBITTORRENT_PASSWORD", "adminadmin"),
        serpapi_api_key=os.getenv("SERPAPI_API_KEY") or None,
    )