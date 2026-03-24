def print_route_decision(input_type: str, adapter_name: str, reason: str) -> None:
    print(f"[OK] Input type: {input_type}")
    print(f"[OK] Adapter selected: {adapter_name}")
    print(f"[INFO] Routing reason: {reason}")


def print_adapter_result(result: dict) -> None:
    print(f"[INFO] Adapter status: {result.get('status')}")
    print(f"[INFO] Adapter: {result.get('adapter')}")
    print(f"[INFO] Message: {result.get('message')}")

    if "value" in result:
        print(f"[OK] Value: {result.get('value')}")

    if result.get("btih"):
        print(f"[OK] Extracted btih: {result.get('btih')}")

    if result.get("metadata_only") is not None:
        print(f"[INFO] Metadata only: {result.get('metadata_only')}")

    if result.get("source"):
        print(f"[INFO] Source: {result.get('source')}")

    if result.get("files"):
        print("[INFO] Files:")
        for file_entry in result.get("files", []):
            print(f" - {file_entry}")

    if result.get("extra"):
        print(f"[INFO] Extra: {result.get('extra')}")

    if result.get("http_status") is not None:
        print(f"[INFO] HTTP status: {result.get('http_status')}")

    if result.get("request_url"):
        print(f"[INFO] Request URL: {result.get('request_url')}")

    if result.get("response_preview"):
        print("[INFO] Response preview:")
        print(result.get("response_preview"))

    if result.get("lynx_binary"):
        print(f"[INFO] Lynx binary: {result.get('lynx_binary')}")

    if result.get("lynx_found") is not None:
        print(f"[INFO] Lynx found on PATH: {result.get('lynx_found')}")

    if result.get("is_onion") is not None:
        print(f"[INFO] Onion target: {result.get('is_onion')}")

    if result.get("proxy"):
        print(f"[INFO] Proxy: {result.get('proxy')}")

    if result.get("use_tor") is not None:
        print(f"[INFO] Use Tor: {result.get('use_tor')}")

    if result.get("prepared_command"):
        print("[INFO] Prepared command:")
        print(" ".join(result.get("prepared_command")))

    if result.get("returncode") is not None:
        print(f"[INFO] Return code: {result.get('returncode')}")

    if result.get("stdout_preview"):
        print("[INFO] STDOUT preview:")
        print(result.get("stdout_preview"))

    if result.get("stderr_preview"):
        print("[INFO] STDERR preview:")
        print(result.get("stderr_preview"))

    if result.get("provider"):
        print(f"[INFO] Provider: {result.get('provider')}")

    if result.get("use_case") is not None:
        print(f"[INFO] Use case: {result.get('use_case')}")

    if result.get("query"):
        print(f"[INFO] Built query: {result.get('query')}")

    if result.get("manual_search_url"):
        print(f"[INFO] Manual search URL: {result.get('manual_search_url')}")

    if result.get("filters"):
        print(f"[INFO] Filters: {result.get('filters')}")

    if result.get("comparisons"):
        print("[INFO] Provider comparison:")
        for provider_name, provider_data in result["comparisons"].items():
            print(f"--- {provider_name.upper()} ---")
            print(f"Query: {provider_data.get('query')}")
            print(f"URL: {provider_data.get('manual_search_url')}")