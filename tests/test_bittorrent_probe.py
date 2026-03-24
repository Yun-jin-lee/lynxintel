from app.adapters.bittorrent_probe import run_infohash_probe, run_magnet_probe


def test_run_infohash_probe_returns_expected_structure():
    infohash = "0123456789abcdef0123456789abcdef01234567"
    result = run_infohash_probe(infohash)

    assert result["status"] == "not_implemented"
    assert result["input_type"] == "infohash"
    assert result["adapter"] == "bittorrent_probe"
    assert result["btih"] == infohash
    assert result["metadata_only"] is True
    assert result["source"] == "local-placeholder"
    assert isinstance(result["files"], list)
    assert len(result["files"]) == 2


def test_run_magnet_probe_returns_expected_structure():
    magnet = "magnet:?xt=urn:btih:0123456789ABCDEF0123456789ABCDEF01234567&dn=test"
    btih = "0123456789ABCDEF0123456789ABCDEF01234567"
    result = run_magnet_probe(magnet, btih=btih)

    assert result["status"] == "not_implemented"
    assert result["input_type"] == "magnet"
    assert result["adapter"] == "bittorrent_probe"
    assert result["btih"] == btih
    assert result["metadata_only"] is True
    assert result["source"] == "local-placeholder"
    assert isinstance(result["files"], list)
    assert len(result["files"]) == 2