import os
import shutil
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


def _build_proxy_env() -> dict[str, str]:
    env = os.environ.copy()
    socks_host = get_tor_socks_host()
    socks_port = get_tor_socks_port()
    proxy_value = f"socks5://{socks_host}:{socks_port}"

    env["SOCKS5_PROXY"] = proxy_value
    env["socks5_proxy"] = proxy_value
    return env


def run_tor_text_browse(target: str, *, dry_run: bool = True) -> dict[str, Any]:
    """
    Tor/Lynx adapter.
    In dry-run mode it only prepares the command.
    In execute mode it runs Lynx and returns the output.
    """
    lynx_binary = get_lynx_binary()
    lynx_exists = shutil.which(lynx_binary) is not None
    command = build_lynx_command(target)

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
        "prepared_command": command,
        "proxy": f"socks5://{get_tor_socks_host()}:{get_tor_socks_port()}",
    }

    if not lynx_exists:
        result["status"] = "warning"
        result["message"] = "Lynx binary was not found on PATH. Command preparation still succeeded."
        return result

    if dry_run:
        return result

    try:
        completed = subprocess.run(
            command,
            env=_build_proxy_env(),
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
            result["message"] = "Tor/Lynx browse executed successfully."
        else:
            result["status"] = "warning"
            result["message"] = "Tor/Lynx browse executed but returned a non-zero exit code."

    except subprocess.TimeoutExpired:
        result["status"] = "error"
        result["message"] = "Tor/Lynx browse timed out."
    except Exception as exc:
        result["status"] = "error"
        result["message"] = f"Tor/Lynx execution failed: {exc}"

    return result