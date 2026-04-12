import shutil
import subprocess
from urllib.parse import urlparse

from app.config import load_config


def is_valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def open_with_lynx(url: str, dump: bool = False) -> int:
    if not is_valid_url(url):
        raise ValueError("Invalid URL. Use a full http:// or https:// URL.")

    config = load_config()
    lynx_bin = config.lynx_bin

    if shutil.which(lynx_bin) is None:
        raise RuntimeError(
            f"Lynx binary '{lynx_bin}' was not found on PATH. "
            "Install lynx or set LYNX_BIN in .env."
        )

    if dump:
        command = [lynx_bin, "-accept_all_cookies", "-dump", url]
        print("[OK] Opening URL in Lynx dump mode")
        print(f"[INFO] Command: {' '.join(command)}")
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        print(completed.stdout)
        if completed.stderr.strip():
            print("[INFO] STDERR:")
            print(completed.stderr)
        return completed.returncode

    command = [lynx_bin, "-cookies", "-accept_all_cookies", url]
    print("[OK] Opening URL in Lynx interactive mode")
    print(f"[INFO] Command: {' '.join(command)}")
    return subprocess.call(command)