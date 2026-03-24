import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lynx-osint",
        description="Lightweight CLI-based OSINT probe engine for Tor, Jackett, and BitTorrent metadata workflows.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # probe
    probe_parser = subparsers.add_parser(
        "probe",
        help="Probe a BitTorrent target such as an infohash or magnet URI.",
    )

    probe_group = probe_parser.add_mutually_exclusive_group(required=True)
    probe_group.add_argument(
        "--infohash",
        type=str,
        help="40-character hexadecimal BitTorrent infohash.",
    )
    probe_group.add_argument(
        "--magnet",
        type=str,
        help="Magnet URI containing a btih value.",
    )

    # search
    search_parser = subparsers.add_parser(
        "search",
        help="Run a keyword-based search workflow.",
    )
    search_parser.add_argument(
        "--keyword",
        type=str,
        required=True,
        help="Keyword query to route to the search adapter.",
    )

    # browse
    browse_parser = subparsers.add_parser(
        "browse",
        help="Prepare a text-based browse workflow for a target URL.",
    )
    browse_parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="Target HTTP(S) URL, including .onion targets.",
    )
    browse_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the prepared Lynx/Tor command without executing it.",
    )

    return parser