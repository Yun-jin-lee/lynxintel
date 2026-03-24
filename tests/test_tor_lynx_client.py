from app.adapters.tor_lynx_client import build_lynx_command, run_tor_text_browse


def test_build_lynx_command_contains_target():
    target = "http://example.com"
    command = build_lynx_command(target)

    assert target in command
    assert command[0]
    assert "-dump" in command


def test_run_tor_text_browse_returns_expected_shape_in_dry_run():
    result = run_tor_text_browse("http://example.com", dry_run=True)

    assert result["input_type"] == "target"
    assert result["adapter"] == "tor_lynx_client"
    assert "prepared_command" in result
    assert result["dry_run"] is True
    assert "tor_reachable" in result


def test_run_tor_text_browse_execute_mode_returns_shape():
    result = run_tor_text_browse("http://example.com", dry_run=False)

    assert result["input_type"] == "target"
    assert result["adapter"] == "tor_lynx_client"
    assert "prepared_command" in result
    assert result["dry_run"] is False
    assert "tor_reachable" in result