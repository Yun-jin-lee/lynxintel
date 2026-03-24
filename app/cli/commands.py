from app.adapters.bittorrent_probe import run_infohash_probe, run_magnet_probe
from app.adapters.jackett_client import run_keyword_search
from app.adapters.tor_lynx_client import run_tor_text_browse
from app.core.router import route_browse_input, route_probe_input, route_search_input
from app.reporting.text_reporter import print_adapter_result, print_route_decision
from app.utils.validators import (
    extract_btih_from_magnet,
    is_valid_infohash,
    is_valid_magnet,
    is_valid_tor_target,
)


def run_probe_command(args) -> int:
    if args.infohash:
        if not is_valid_infohash(args.infohash):
            print("[ERROR] Invalid infohash. Expected 40 hexadecimal characters.")
            return 1

        decision = route_probe_input(infohash=args.infohash)
        print_route_decision(
            input_type=decision.input_type,
            adapter_name=decision.adapter_name,
            reason=decision.reason,
        )

        result = run_infohash_probe(args.infohash)
        print_adapter_result(result)
        return 0

    if args.magnet:
        if not is_valid_magnet(args.magnet):
            print("[ERROR] Invalid magnet URI.")
            return 1

        btih = extract_btih_from_magnet(args.magnet)
        decision = route_probe_input(magnet=args.magnet)

        print_route_decision(
            input_type=decision.input_type,
            adapter_name=decision.adapter_name,
            reason=decision.reason,
        )

        result = run_magnet_probe(args.magnet, btih=btih)
        print_adapter_result(result)
        return 0

    print("[ERROR] No probe input provided.")
    return 1


def run_search_command(args) -> int:
    keyword = (args.keyword or "").strip()

    if not keyword:
        print("[ERROR] Keyword cannot be empty.")
        return 1

    decision = route_search_input(keyword=keyword)
    print_route_decision(
        input_type=decision.input_type,
        adapter_name=decision.adapter_name,
        reason=decision.reason,
    )

    result = run_keyword_search(keyword)
    print_adapter_result(result)
    return 0


def run_browse_command(args) -> int:
    target = (args.target or "").strip()

    if not is_valid_tor_target(target):
        print("[ERROR] Invalid browse target. Expected an HTTP(S) URL.")
        return 1

    decision = route_browse_input(target=target)
    print_route_decision(
        input_type=decision.input_type,
        adapter_name=decision.adapter_name,
        reason=decision.reason,
    )

    result = run_tor_text_browse(target, dry_run=args.dry_run)
    print_adapter_result(result)
    return 0