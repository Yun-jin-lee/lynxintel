import pytest

from app.core.router import route_probe_input, route_search_input


def test_route_probe_input_with_infohash_returns_bittorrent_probe():
    decision = route_probe_input(
        infohash="0123456789abcdef0123456789abcdef01234567"
    )

    assert decision.input_type == "infohash"
    assert decision.adapter_name == "bittorrent_probe"
    assert "BitTorrent metadata probe adapter" in decision.reason


def test_route_probe_input_with_magnet_returns_bittorrent_probe():
    decision = route_probe_input(
        magnet="magnet:?xt=urn:btih:0123456789ABCDEF0123456789ABCDEF01234567&dn=test"
    )

    assert decision.input_type == "magnet"
    assert decision.adapter_name == "bittorrent_probe"
    assert "BitTorrent metadata probe adapter" in decision.reason


def test_route_probe_input_without_values_raises_value_error():
    with pytest.raises(ValueError, match="No valid probe input was provided."):
        route_probe_input()


def test_route_search_input_with_keyword_returns_jackett_client():
    decision = route_search_input(keyword="cyber security pdf")

    assert decision.input_type == "keyword"
    assert decision.adapter_name == "jackett_client"
    assert "Jackett adapter" in decision.reason


def test_route_search_input_with_empty_keyword_raises_value_error():
    with pytest.raises(ValueError, match="Keyword cannot be empty."):
        route_search_input(keyword="   ")