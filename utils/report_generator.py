"""Structured and human-readable execution report generation."""

import json
import os
import platform
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest
import selenium


REPORT_DIR = Path(__file__).resolve().parents[1] / "reports"
REPORT_FILE = REPORT_DIR / "execution_report.txt"
REPORT_JSON_FILE = REPORT_DIR / "execution_report.json"


class ReportGenerator:
    """Collect test diagnostics and write text and JSON reports."""

    def __init__(self, website_url, browser):
        self.website_url = website_url
        self.browser = browser
        self.start_time = datetime.now().astimezone()
        self.test_results = []
        self._result_indexes = {}
        self.exit_status = None

    def add_result(self, result):
        """Add or update one test result using its stable node ID."""
        result = dict(result)
        result.setdefault("nodeid", result.get("name", ""))
        result_key = result["nodeid"] or self._legacy_result_key(result)

        if result_key in self._result_indexes:
            self.test_results[self._result_indexes[result_key]] = result
        else:
            self._result_indexes[result_key] = len(self.test_results)
            self.test_results.append(result)

    def generate(self, exit_status=None):
        """Write execution_report.txt and execution_report.json."""
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        if exit_status is not None:
            self.exit_status = int(exit_status)

        end_time = datetime.now().astimezone()
        duration = (end_time - self.start_time).total_seconds()
        summary = self._summary()
        payload = {
            "schema_version": "1.0",
            "run": {
                "started_at": self.start_time.isoformat(),
                "finished_at": end_time.isoformat(),
                "duration_seconds": round(duration, 3),
                "exit_status": self.exit_status,
                "website_url": self.website_url,
                "browser": self.browser,
                "python_version": platform.python_version(),
                "python_executable": sys.executable,
                "selenium_version": selenium.__version__,
                "pytest_version": pytest.__version__,
                "os": platform.platform(),
                "hostname": socket.gethostname(),
                "git_commit": _git_commit(),
                "ci_build": os.getenv("CI_BUILD_ID") or os.getenv("BUILD_NUMBER") or "",
            },
            "summary": summary,
            "categories": self._category_summary(),
            "tests": self.test_results,
        }
        REPORT_JSON_FILE.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        REPORT_FILE.write_text(self._build_text_report(payload), encoding="utf-8")
        return REPORT_FILE

    def _summary(self):
        total = len(self.test_results)
        passed = self._count_by_status("PASS")
        failed = self._count_by_status("FAIL")
        skipped = self._count_by_status("SKIP")
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_percentage": round(passed / total * 100, 2) if total else 0,
            "fail_percentage": round(failed / total * 100, 2) if total else 0,
        }

    def _category_summary(self):
        categories = {}
        for result in self.test_results:
            category = result.get("category", "General")
            entry = categories.setdefault(
                category, {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
            )
            entry["total"] += 1
            status_key = {"PASS": "passed", "FAIL": "failed", "SKIP": "skipped"}.get(result.get("status"), "failed")
            entry[status_key] += 1
        return dict(sorted(categories.items()))

    def _build_text_report(self, payload):
        run = payload["run"]
        summary = payload["summary"]
        lines = [
            "=======================================",
            "Surya Sangam Automation Report",
            "=======================================",
            f"Execution Start: {run['started_at']}",
            f"Execution End: {run['finished_at']}",
            f"Browser: {run['browser']}",
            f"Python Version: {run['python_version']}",
            f"Python Executable: {run['python_executable']}",
            f"Selenium Version: {run['selenium_version']}",
            f"Pytest Version: {run['pytest_version']}",
            f"Operating System: {run['os']}",
            f"Host: {run['hostname']}",
            f"Git Commit: {run['git_commit'] or 'unknown'}",
            f"Build: {run['ci_build'] or 'unknown'}",
            f"Website URL: {run['website_url']}",
            f"Exit Status: {run['exit_status']}",
            f"Total Test Cases: {summary['total']}",
            f"Passed: {summary['passed']}",
            f"Failed: {summary['failed']}",
            f"Skipped: {summary['skipped']}",
            f"Pass Percentage: {summary['pass_percentage']:.2f}%",
            f"Fail Percentage: {summary['fail_percentage']:.2f}%",
            f"Execution Duration: {run['duration_seconds']:.3f} sec",
            "",
            "=======================================",
            "Result Summary By Area",
            "=======================================",
        ]

        for category, values in payload["categories"].items():
            lines.append(
                f"{category}: Total={values['total']}, Passed={values['passed']}, "
                f"Failed={values['failed']}, Skipped={values['skipped']}"
            )

        lines.extend(
            [
                "",
                "=======================================",
                "Executed Test Cases",
                "=======================================",
            ]
        )
        for index, result in enumerate(self.test_results, start=1):
            lines.extend(self._format_test_result(index, result))

        lines.extend(
            [
                "=======================================",
                "Recommendations",
                "=======================================",
            ]
        )
        failed_tests = [item for item in self.test_results if item.get("status") == "FAIL"]
        if not failed_tests:
            lines.append("All recorded site checks passed.")
        else:
            for result in failed_tests:
                lines.append(
                    f"- Review '{result.get('name', result.get('nodeid', 'unknown'))}'. "
                    "Use the JSON fields and linked artifacts to reproduce the issue."
                )
        lines.append("")
        lines.append(f"Machine-readable report: {REPORT_JSON_FILE}")
        return "\n".join(lines)

    def _format_test_result(self, index, result):
        lines = [
            f"TC{index:03d} - {result.get('name', '')}",
            f"Node ID: {result.get('nodeid', '')}",
            f"Source: {result.get('source_file', '')}:{result.get('source_line', '')}",
            f"Area: {result.get('category', 'General')}",
            f"Phase: {result.get('phase', 'call')}",
            result.get("status", "FAIL"),
            f"Duration: {result.get('duration', 0):.3f} sec",
        ]
        for label, key in (
            ("Problem Details", "reason"),
            ("Exception Type", "exception_type"),
            ("URL At Failure", "url"),
            ("Page Title", "title"),
            ("Parameters", "parameters"),
            ("Screenshot Evidence", "screenshot"),
            ("Full Traceback", "traceback_path"),
            ("Page HTML Snapshot", "page_html_path"),
            ("Browser Console Log", "browser_console_log_path"),
            ("Performance Log", "performance_log_path"),
        ):
            value = result.get(key)
            if value:
                lines.extend([f"{label}:", str(value)])

        if result.get("traceback"):
            lines.extend(["Traceback Excerpt:", str(result["traceback"])[:2000]])
        if result.get("captured_stdout"):
            lines.extend(["Captured STDOUT:", str(result["captured_stdout"])[:1000]])
        if result.get("captured_stderr"):
            lines.extend(["Captured STDERR:", str(result["captured_stderr"])[:1000]])
        lines.extend(["---", ""])
        return lines

    def _count_by_status(self, status):
        return sum(1 for result in self.test_results if result.get("status") == status)

    @staticmethod
    def _legacy_result_key(result):
        return (
            result.get("name", ""),
            result.get("category", "General"),
            result.get("status", ""),
            result.get("reason", ""),
        )


def _git_commit():
    """Return the current commit without making reporting depend on Git."""
    configured = os.getenv("GIT_COMMIT") or os.getenv("CI_COMMIT_SHA")
    if configured:
        return configured
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""
