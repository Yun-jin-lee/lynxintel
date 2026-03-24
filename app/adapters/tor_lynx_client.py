import os
import shutil
import socket
import subprocess
from typing import Any

from app.config import get_lynx_binary, get_tor_socks_host, get_tor_socks_port
from app.utils.validators import is_onion_url


def build_lynx_command(target: str) -> list[str]:
    lynx_binary = get_lynx_binary()

    return [
        lynx_binary,
        "-accept_all_cookies",
        "-dump",
        target,
    ]


def _check_tor_socks_reachable(host: str, port: int, timeout: float = 3.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _build_proxy_env(use_tor: bool) -> dict[str, str]:
    env = os.environ.copy()

    if not use_tor:
        env.pop("SOCKS5_PROXY", None)
        env.pop("socks5_proxy", None)
        return env

    socks_host = get_tor_socks_host()
    socks_port = get_tor_socks_port()

    proxy_value = f"{socks_host}:{socks_port}"

    env["SOCKS5_PROXY"] = proxy_value
    env["socks5_proxy"] = proxy_value
    return env


def run_tor_text_browse(target: str, *, dry_run: bool = True) -> dict[str, Any]:
    """
    Tor/Lynx adapter.

    - Normal HTTP(S) targets run directly by default.
    - .onion targets use the configured Tor SOCKS proxy.
    - The adapter checks whether Tor SOCKS is reachable.
    """
    lynx_binary = get_lynx_binary()
    lynx_exists = shutil.which(lynx_binary) is not None
    onion_target = is_onion_url(target)
    command = build_lynx_command(target)
    use_tor = onion_target

    socks_host = get_tor_socks_host()
    socks_port_raw = get_tor_socks_port()

    try:
        socks_port = int(socks_port_raw)
    except ValueError:
        socks_port = 9050

    tor_reachable = _check_tor_socks_reachable(socks_host, socks_port)

    result: dict[str, Any] = {
        "status": "ok",
        "input_type": "target",
        "value": target,
        "adapter": "tor_lynx_client",
        "message": "Prepared Tor/Lynx browse workflow.",
        "lynx_binary": lynx_binary,
        "lynx_found": lynx_exists,
        "is_onion": onion_target,
        "dry_run": dry_run,
        "prepared_command": command,
        "proxy": f"{socks_host}:{socks_port}" if use_tor else None,
        "use_tor": use_tor,
        "tor_reachable": tor_reachable,
    }

    if not lynx_exists:
        result["status"] = "warning"
        result["message"] = "Lynx binary was not found on PATH. Command preparation still succeeded."
        return result

    if use_tor and not tor_reachable:
        result["status"] = "warning"
        result["message"] = "Target requires Tor, but the configured SOCKS proxy is not reachable."
        return result

    if dry_run:
        return result

    try:
        completed = subprocess.run(
            command,
            env=_build_proxy_env(use_tor=use_tor),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        result["stdout_preview"] = completed.stdout[:2000]
        result["stderr_preview"] = completed.stderr[:1000]
        result["returncode"] = completed.returncode

        if completed.returncode == 0:
            result["status"] = "ok"
            result["message"] = "Lynx browse executed successfully."
        else:
            result["status"] = "warning"
            result["message"] = "Lynx browse executed but returned a non-zero exit code."

    except subprocess.TimeoutExpired:
        result["status"] = "error"
        result["message"] = "Lynx browse timed out."
    except Exception as exc:
        result["status"] = "error"
        result["message"] = f"Lynx execution failed: {exc}"

    return result