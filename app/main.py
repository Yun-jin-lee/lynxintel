import argparse
import sys

from app.router import dispatch


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="liris",
        description="CLI-first tool for text browsing and torrent backend routing.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    open_parser = subparsers.add_parser(
        "open",
        help="Open a direct URL with Lynx.",
    )
    open_parser.add_argument(
        "input",
        help="Direct URL to open.",
    )
    open_parser.add_argument(
        "--dump",
        action="store_true",
        help="Render page as plain text instead of interactive mode.",
    )

    search_parser = subparsers.add_parser(
        "search",
        help="Search through the local SearXNG backend and open the chosen result in Lynx.",
    )
    search_parser.add_argument(
        "input",
        help="Keyword to search for.",
    )
    search_parser.add_argument(
        "--provider",
        choices=["all", "google", "yandex", "baidu"],
        default="all",
        help="Search provider filter inside SearXNG. Default: all",
    )
    search_parser.add_argument(
        "--dump",
        action="store_true",
        help="Render the chosen result page as plain text instead of interactive mode.",
    )
    search_parser.add_argument(
        "--unique",
        action="store_true",
        help="Compare the first page of results from multiple SearXNG engines and show unique browser-specific hits.",
    )
    search_parser.add_argument(
        "--delta",
        action="store_true",
        help="Show only unique results per engine and common shared results in a concise delta view.",
    )

    probe_parser = subparsers.add_parser(
        "probe",
        help="Send a magnet link or torrent URL to qBittorrent.",
    )
    probe_parser.add_argument(
        "input",
        help="Magnet link or torrent URL.",
    )

    subparsers.add_parser(
        "status",
        help="Show qBittorrent backend status.",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        return dispatch(args)
    except KeyboardInterrupt:
        print("[INFO] Interrupted by user.")
        return 130
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())