from app.adapters.baidu_search_client import run_baidu_search
from app.adapters.bittorrent_probe import (
    run_infohash_probe,
    run_magnet_probe,
    run_torrent_file_probe,
)
from app.adapters.google_search_client import run_google_search
from app.adapters.jackett_client import run_keyword_search
from app.adapters.tor_lynx_client import run_tor_text_browse
from app.adapters.yandex_search_client import run_yandex_search
from app.core.comparison_builder import build_provider_comparison
from app.core.router import (
    route_browse_input,
    route_probe_input,
    route_search_input,
    route_websearch_input,
)
from app.core.search_models import SearchRequest
from app.core.search_profiles import apply_use_case
from app.reporting.json_reporter import save_json_report, to_pretty_json
from app.reporting.text_reporter import print_adapter_result, print_route_decision
from app.utils.validators import (
    extract_btih_from_magnet,
    is_valid_infohash,
    is_valid_magnet,
    is_valid_tor_target,
)


def _handle_optional_json_output(result: dict, args) -> None:
    if getattr(args, "json", False):
        print("[INFO] JSON output:")
        print(to_pretty_json(result))

    if getattr(args, "output", None):
        saved_path = save_json_report(result, args.output)
        print(f"[INFO] JSON report saved to: {saved_path}")


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

        result = run_infohash_probe(args.infohash, filetype=args.filetype)
        print_adapter_result(result)
        _handle_optional_json_output(result, args)
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

        result = run_magnet_probe(args.magnet, btih=btih, filetype=args.filetype)
        print_adapter_result(result)
        _handle_optional_json_output(result, args)
        return 0

    if args.torrent_file:
        print_route_decision(
            input_type="torrent_file",
            adapter_name="bittorrent_probe",
            reason="Local .torrent file should be handled by the BitTorrent metadata probe adapter.",
        )

        result = run_torrent_file_probe(args.torrent_file, filetype=args.filetype)
        print_adapter_result(result)
        _handle_optional_json_output(result, args)
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
    _handle_optional_json_output(result, args)
    return 0


def run_websearch_command(args) -> int:
    keyword = (args.keyword or "").strip()
    provider = (args.provider or "").strip().lower()

    if not keyword:
        print("[ERROR] Web search keyword cannot be empty.")
        return 1

    decision = route_websearch_input(provider=provider, keyword=keyword)
    print_route_decision(
        input_type=decision.input_type,
        adapter_name=decision.adapter_name,
        reason=decision.reason,
    )

    profile = apply_use_case(keyword, args.use_case)

    request = SearchRequest(
        provider=provider,
        keyword=profile["keyword"],
        use_case=args.use_case,
        site=args.site or profile.get("site"),
        filetype=args.filetype or profile.get("filetype"),
        exact_phrase=args.exact_phrase or profile.get("exact_phrase"),
        exclude_terms=args.exclude or profile.get("exclude_terms", []),
        additional_terms=(args.add or []) + profile.get("additional_terms", []),
    )

    if provider == "google":
        result = run_google_search(request)
    elif provider == "yandex":
        result = run_yandex_search(request)
    elif provider == "baidu":
        result = run_baidu_search(request)
    else:
        print(f"[ERROR] Unsupported provider: {provider}")
        return 1

    print_adapter_result(result)
    _handle_optional_json_output(result, args)
    return 0


def run_comparesearch_command(args) -> int:
    keyword = (args.keyword or "").strip()

    if not keyword:
        print("[ERROR] Compare search keyword cannot be empty.")
        return 1

    profile = apply_use_case(keyword, args.use_case)

    request = SearchRequest(
        provider="comparison",
        keyword=profile["keyword"],
        use_case=args.use_case,
        site=args.site or profile.get("site"),
        filetype=args.filetype or profile.get("filetype"),
        exact_phrase=args.exact_phrase or profile.get("exact_phrase"),
        exclude_terms=args.exclude or profile.get("exclude_terms", []),
        additional_terms=(args.add or []) + profile.get("additional_terms", []),
    )

    print_route_decision(
        input_type="comparesearch",
        adapter_name="comparison_builder",
        reason="Cross-provider query comparison was selected.",
    )

    result = build_provider_comparison(request)
    print_adapter_result(result)
    _handle_optional_json_output(result, args)
    return 0