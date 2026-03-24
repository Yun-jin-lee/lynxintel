import shutil
from typing import Any

from app.config import get_lynx_binary, get_tor_socks_host, get_tor_socks_port
from app.utils.validators import is_onion_url


def build_lynx_command(target: str) -> list[str]:
    lynx_binary = get_lynx_binary()
    socks_host = get_tor_socks_host()
    socks_port = get_tor_socks_port()

    return [
        lynx_binary,
        "-cfg=NONE",
        "-accept_all_cookies",
        target,
        f"SOCKS5_PROXY=socks5://{socks_host}:{socks_port}",
    ]


def run_tor_text_browse(target: str, *, dry_run: bool = True) -> dict[str, Any]:
    """
    Safe preparation layer for Tor/Lynx browsing.
    For now this only validates local runtime assumptions and returns a dry-run command.
    """
    lynx_binary = get_lynx_binary()
    lynx_exists = shutil.which(lynx_binary) is not None

    result: dict[str, Any] = {
        "status": "ok",
        "input_type": "target",
        "value": target,
        "adapter": "tor_lynx_client",
        "message": "Prepared Tor/Lynx browse workflow.",
        "lynx_binary": lynx_binary,
        "lynx_found": lynx_exists,
        "is_onion": is_onion_url(target),
        "dry_run": dry_run,
        "prepared_command": build_lynx_command(target),
    }

    if not lynx_exists:
        result["status"] = "warning"
        result["message"] = "Lynx binary was not found on PATH. Command preparation still succeeded."

    return result