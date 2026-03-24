import json
from pathlib import Path

from app.reporting.json_reporter import save_json_report, to_pretty_json


def test_to_pretty_json_returns_string():
    data = {"status": "ok", "value": "test"}
    result = to_pretty_json(data)

    assert isinstance(result, str)
    assert '"status": "ok"' in result


def test_save_json_report_writes_file(tmp_path: Path):
    data = {"status": "ok", "value": "test"}
    output_file = tmp_path / "report.json"

    saved_path = save_json_report(data, str(output_file))

    assert saved_path == str(output_file)
    assert output_file.exists()

    loaded = json.loads(output_file.read_text(encoding="utf-8"))
    assert loaded["status"] == "ok"
    assert loaded["value"] == "test"