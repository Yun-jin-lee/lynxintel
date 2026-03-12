from app.utils.validators import (
    extract_btih_from_magnet,
    is_valid_infohash,
    is_valid_magnet,
)


def test_valid_infohash_returns_true():
    value = "0123456789abcdef0123456789abcdef01234567"
    assert is_valid_infohash(value) is True


def test_invalid_infohash_returns_false_when_too_short():
    value = "123"
    assert is_valid_infohash(value) is False


def test_invalid_infohash_returns_false_when_not_hex():
    value = "ZZZZ456789abcdef0123456789abcdef01234567"
    assert is_valid_infohash(value) is False


def test_valid_magnet_returns_true():
    magnet = "magnet:?xt=urn:btih:0123456789ABCDEF0123456789ABCDEF01234567&dn=test"
    assert is_valid_magnet(magnet) is True


def test_invalid_magnet_returns_false_when_missing_btih():
    magnet = "magnet:?dn=testfile"
    assert is_valid_magnet(magnet) is False


def test_invalid_magnet_returns_false_when_not_magnet_scheme():
    magnet = "http://example.com/file.torrent"
    assert is_valid_magnet(magnet) is False


def test_extract_btih_from_valid_magnet():
    magnet = "magnet:?xt=urn:btih:0123456789ABCDEF0123456789ABCDEF01234567&dn=test"
    result = extract_btih_from_magnet(magnet)
    assert result == "0123456789ABCDEF0123456789ABCDEF01234567"


def test_extract_btih_from_invalid_magnet_returns_none():
    magnet = "magnet:?dn=test"
    result = extract_btih_from_magnet(magnet)
    assert result is None
    

from app.utils.validators import is_onion_url, is_valid_tor_target


def test_valid_tor_target_returns_true_for_http_url():
    assert is_valid_tor_target("http://example.com") is True


def test_valid_tor_target_returns_true_for_https_onion_url():
    assert is_valid_tor_target(
        "http://exampleexample.onion"
    ) is True


def test_invalid_tor_target_returns_false_for_empty_value():
    assert is_valid_tor_target("   ") is False


def test_is_onion_url_returns_true_for_onion_target():
    assert is_onion_url("http://aaaaaaaaaaaaaaaa.onion") is True


def test_is_onion_url_returns_false_for_normal_url():
    assert is_onion_url("http://example.com") is False