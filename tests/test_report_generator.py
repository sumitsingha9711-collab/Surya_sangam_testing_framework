from pathlib import Path

import utils.report_generator as report_generator_module
from utils.report_generator import ReportGenerator


def test_generate_report_keeps_only_unique_test_logs(tmp_path, monkeypatch):
    report_dir = tmp_path / "reports"
    report_file = report_dir / "execution_report.txt"

    monkeypatch.setattr(report_generator_module, "REPORT_DIR", report_dir)
    monkeypatch.setattr(report_generator_module, "REPORT_FILE", report_file)

    report = ReportGenerator("https://www.suryasangam.com/", "Chrome")
    result = {
        "name": "Homepage loads",
        "category": "Homepage",
        "status": "PASS",
        "duration": 1.25,
        "reason": "",
        "screenshot": "",
    }

    report.add_result(result)
    report.add_result(result)

    generated_report = report.generate()
    report_text = generated_report.read_text(encoding="utf-8")

    assert generated_report.parent == report_dir
    assert generated_report.exists()
    assert "Total Test Cases: 1" in report_text
    assert report_text.count("TC001 - Homepage loads") == 1
