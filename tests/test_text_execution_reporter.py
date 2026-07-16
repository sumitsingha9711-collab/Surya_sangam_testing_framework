from __future__ import annotations

from datetime import datetime
from pathlib import Path

from utils.text_execution_reporter import generate_text_execution_report


def test_generate_text_execution_report_deduplicates_results(tmp_path: Path):
    results = [
        {
            "test_name": "duplicate_case",
            "status": "passed",
            "duration": 1.0,
            "error": "",
            "screenshot": "",
            "expected_result": "",
            "actual_result": "",
        },
        {
            "test_name": "duplicate_case",
            "status": "failed",
            "duration": 2.0,
            "error": "duplicate failure",
            "screenshot": "",
            "expected_result": "",
            "actual_result": "duplicate failure",
        },
        {
            "test_name": "other_case",
            "status": "passed",
            "duration": 3.0,
            "error": "",
            "screenshot": "",
            "expected_result": "",
            "actual_result": "",
        },
    ]

    report_path = generate_text_execution_report(
        results=results,
        website="https://www.suryasangam.com/",
        execution_start=datetime(2026, 1, 1, 10, 0, 0),
        execution_end=datetime(2026, 1, 1, 10, 0, 5),
        browser_name="Chrome",
        operating_system="Windows",
        output_dir=tmp_path,
    )

    content = report_path.read_text(encoding="utf-8")
    assert content.count("Test Case: duplicate_case") == 1
