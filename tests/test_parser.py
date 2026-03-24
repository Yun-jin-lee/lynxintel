from app.cli.parser import build_parser


def test_probe_infohash_arguments_are_parsed_correctly():
    parser = build_parser()
    args = parser.parse_args(
        ["probe", "--infohash", "0123456789abcdef0123456789abcdef01234567"]
    )

    assert args.command == "probe"
    assert args.infohash == "0123456789abcdef0123456789abcdef01234567"
    assert args.magnet is None


def test_probe_magnet_arguments_are_parsed_correctly():
    parser = build_parser()
    magnet = "magnet:?xt=urn:btih:0123456789ABCDEF0123456789ABCDEF01234567&dn=test"
    args = parser.parse_args(["probe", "--magnet", magnet])

    assert args.command == "probe"
    assert args.magnet == magnet
    assert args.infohash is None


def test_search_keyword_arguments_are_parsed_correctly():
    parser = build_parser()
    args = parser.parse_args(["search", "--keyword", "cyber security pdf"])

    assert args.command == "search"
    assert args.keyword == "cyber security pdf"
    
    
def test_browse_target_arguments_are_parsed_correctly():
    parser = build_parser()
    args = parser.parse_args(["browse", "--target", "http://example.com", "--dry-run"])

    assert args.command == "browse"
    assert args.target == "http://example.com"
    assert args.dry_run is True