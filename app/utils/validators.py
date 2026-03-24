import re


INFOHASH_40_HEX_RE = re.compile(r"^[A-Fa-f0-9]{40}$")
MAGNET_RE = re.compile(r"^magnet:\?.+", re.IGNORECASE)
BTIH_RE = re.compile(r"xt=urn:btih:([A-Za-z0-9]+)", re.IGNORECASE)


def is_valid_infohash(value: str) -> bool:
    """
    Validate whether the value is a 40-character hexadecimal BitTorrent infohash.
    """
    if not isinstance(value, str):
        return False
    return INFOHASH_40_HEX_RE.fullmatch(value.strip()) is not None


def is_valid_magnet(value: str) -> bool:
    """
    Basic validation for a magnet URI.
    Must start with 'magnet:?' and contain a btih value.
    """
    if not isinstance(value, str):
        return False

    value = value.strip()
    if MAGNET_RE.fullmatch(value) is None:
        return False

    return BTIH_RE.search(value) is not None


def extract_btih_from_magnet(magnet_uri: str) -> str | None:
    """
    Extract the btih value from a magnet URI.
    Returns the hash if found, otherwise None.
    """
    if not isinstance(magnet_uri, str):
        return None

    match = BTIH_RE.search(magnet_uri.strip())
    if not match:
        return None

    return match.group(1)


ONION_RE = re.compile(r"^https?://[a-z2-7]{16,56}\.onion(?:/.*)?$", re.IGNORECASE)
HTTP_URL_RE = re.compile(r"^https?://.+", re.IGNORECASE)


def is_valid_tor_target(value: str) -> bool:
    """
    Accept basic HTTP(S) targets, including .onion URLs.
    """
    if not isinstance(value, str):
        return False

    value = value.strip()
    if not value:
        return False

    return HTTP_URL_RE.fullmatch(value) is not None


def is_onion_url(value: str) -> bool:
    """
    Check whether the given URL is a .onion target.
    """
    if not isinstance(value, str):
        return False

    return ONION_RE.fullmatch(value.strip()) is not None