from app.utils.validators import (
    extract_btih_from_magnet,
    is_valid_infohash,
    is_valid_magnet,
)


def run_probe_command(args) -> int:
    """
    Handle the 'probe' command.
    """
    if args.infohash:
        if not is_valid_infohash(args.infohash):
            print("[ERROR] Invalid infohash. Expected 40 hexadecimal characters.")
            return 1

        print("[OK] Input type: infohash")
        print(f"[OK] Value: {args.infohash}")
        print("[OK] Adapter selected: bittorrent_probe")
        print("[INFO] Network probing not implemented yet.")
        return 0

    if args.magnet:
        if not is_valid_magnet(args.magnet):
            print("[ERROR] Invalid magnet URI.")
            return 1

        btih = extract_btih_from_magnet(args.magnet)

        print("[OK] Input type: magnet")
        print(f"[OK] Value: {args.magnet}")
        if btih:
            print(f"[OK] Extracted btih: {btih}")
        print("[OK] Adapter selected: bittorrent_probe")
        print("[INFO] Network probing not implemented yet.")
        return 0

    print("[ERROR] No probe input provided.")
    return 1


def run_search_command(args) -> int:
    """
    Handle the 'search' command.
    """
    keyword = (args.keyword or "").strip()

    if not keyword:
        print("[ERROR] Keyword cannot be empty.")
        return 1

    print("[OK] Input type: keyword")
    print(f"[OK] Keyword: {keyword}")
    print("[OK] Adapter selected: jackett_client")
    print("[INFO] Search execution not implemented yet.")
    return 0