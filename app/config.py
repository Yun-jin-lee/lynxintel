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
    searxng_url: str
    jackett_url: str
    jackett_api_key: str


def load_config() -> AppConfig:
    return AppConfig(
        lynx_bin=os.getenv("LYNX_BIN", "lynx"),
        qbittorrent_url=os.getenv("QBITTORRENT_URL", "http://localhost:8080").rstrip("/"),
        qbittorrent_username=os.getenv("QBITTORRENT_USERNAME", "admin"),
        qbittorrent_password=os.getenv("QBITTORRENT_PASSWORD", "adminadmin"),
        searxng_url=os.getenv("SEARXNG_URL", "http://localhost:8888").rstrip("/"),
        jackett_url=os.getenv("JACKETT_URL", "http://localhost:9117").rstrip("/"),
        jackett_api_key=os.getenv("JACKETT_API_KEY", ""),
    )