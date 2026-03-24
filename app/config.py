import os

from dotenv import load_dotenv


load_dotenv()


def get_jackett_base_url() -> str:
    return os.getenv("JACKETT_BASE_URL", "http://127.0.0.1:9117").rstrip("/")


def get_jackett_api_key() -> str:
    return os.getenv("JACKETT_API_KEY", "").strip()


def get_jackett_indexer() -> str:
    value = os.getenv("JACKETT_INDEXER", "all").strip()
    return value or "all"


def get_tor_socks_host() -> str:
    return os.getenv("TOR_SOCKS_HOST", "127.0.0.1").strip() or "127.0.0.1"


def get_tor_socks_port() -> str:
    return os.getenv("TOR_SOCKS_PORT", "9050").strip() or "9050"


def get_lynx_binary() -> str:
    return os.getenv("LYNX_BINARY", "lynx").strip() or "lynx"