def run_infohash_probe(infohash: str) -> dict:
    """
    Placeholder implementation for infohash-based probing.
    """
    return {
        "status": "not_implemented",
        "input_type": "infohash",
        "value": infohash,
        "adapter": "bittorrent_probe",
        "message": "BitTorrent metadata probing is not implemented yet.",
    }


def run_magnet_probe(magnet: str, btih: str | None = None) -> dict:
    """
    Placeholder implementation for magnet-based probing.
    """
    return {
        "status": "not_implemented",
        "input_type": "magnet",
        "value": magnet,
        "btih": btih,
        "adapter": "bittorrent_probe",
        "message": "BitTorrent metadata probing is not implemented yet.",
    }