from dataclasses import dataclass


@dataclass
class RouteDecision:
    input_type: str
    adapter_name: str
    reason: str


def route_probe_input(*, infohash: str | None = None, magnet: str | None = None) -> RouteDecision:
    """
    Decide which adapter should handle probe-style input.
    """
    if infohash:
        return RouteDecision(
            input_type="infohash",
            adapter_name="bittorrent_probe",
            reason="Infohash input should be handled by the BitTorrent metadata probe adapter.",
        )

    if magnet:
        return RouteDecision(
            input_type="magnet",
            adapter_name="bittorrent_probe",
            reason="Magnet input should be handled by the BitTorrent metadata probe adapter.",
        )

    raise ValueError("No valid probe input was provided.")


def route_search_input(*, keyword: str) -> RouteDecision:
    """
    Decide which adapter should handle search-style input.
    """
    if keyword.strip():
        return RouteDecision(
            input_type="keyword",
            adapter_name="jackett_client",
            reason="Keyword search should be routed to the Jackett adapter.",
        )

    raise ValueError("Keyword cannot be empty.")