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
    probe_parser.add_argument(
        "--filetype",
        type=str,
        choices=["pdf", "image", "text", "archive"],
        help="Optional file type filter for probe results.",
    )
    probe_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the adapter result as JSON.",
    )
    probe_parser.add_argument(
        "--output",
        type=str,
        help="Optional path to save the result as a JSON file.",
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
        help="Prepare or execute a text-based browse workflow for a target URL.",
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
    browse_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the browse result as JSON.",
    )
    browse_parser.add_argument(
        "--output",
        type=str,
        help="Optional path to save the browse result as a JSON file.",
    )

    # websearch
    websearch_parser = subparsers.add_parser(
        "websearch",
        help="Build a provider-specific web search request and manual search URL.",
    )
    websearch_parser.add_argument(
        "--provider",
        type=str,
        required=True,
        choices=["google", "yandex", "baidu"],
        help="Search provider to target.",
    )
    websearch_parser.add_argument(
        "--keyword",
        type=str,
        required=True,
        help="Main search keyword.",
    )
    websearch_parser.add_argument(
        "--use-case",
        type=str,
        choices=["apk", "documents", "images", "leaks"],
        help="Optional predefined search use case.",
    )
    websearch_parser.add_argument(
        "--site",
        type=str,
        help="Optional site/domain restriction.",
    )
    websearch_parser.add_argument(
        "--filetype",
        type=str,
        help="Optional file type restriction.",
    )
    websearch_parser.add_argument(
        "--exact-phrase",
        type=str,
        help="Optional exact phrase.",
    )
    websearch_parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help="Optional terms to exclude.",
    )
    websearch_parser.add_argument(
        "--add",
        nargs="*",
        default=[],
        help="Optional additional terms to include.",
    )
    websearch_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the provider result as JSON.",
    )
    websearch_parser.add_argument(
        "--output",
        type=str,
        help="Optional path to save the result as a JSON file.",
    )

    # comparesearch
    compare_parser = subparsers.add_parser(
        "comparesearch",
        help="Compare generated search queries across Google, Yandex, and Baidu.",
    )
    compare_parser.add_argument(
        "--keyword",
        type=str,
        required=True,
        help="Main search keyword.",
    )
    compare_parser.add_argument(
        "--use-case",
        type=str,
        choices=["apk", "documents", "images", "leaks"],
        help="Optional predefined search use case.",
    )
    compare_parser.add_argument(
        "--site",
        type=str,
        help="Optional site/domain restriction.",
    )
    compare_parser.add_argument(
        "--filetype",
        type=str,
        help="Optional file type restriction.",
    )
    compare_parser.add_argument(
        "--exact-phrase",
        type=str,
        help="Optional exact phrase.",
    )
    compare_parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help="Optional terms to exclude.",
    )
    compare_parser.add_argument(
        "--add",
        nargs="*",
        default=[],
        help="Optional additional terms to include.",
    )
    compare_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the comparison result as JSON.",
    )
    compare_parser.add_argument(
        "--output",
        type=str,
        help="Optional path to save the comparison result as a JSON file.",
    )

    return parser