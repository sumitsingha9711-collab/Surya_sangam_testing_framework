"""Pytest configuration, screenshots, and text reporting."""

import json
import re
import shutil
import smtplib
from pathlib import Path

import pytest

from utils.driver_factory import DriverFactory
from utils.email_reporter import EmailReportConfigError, is_email_configured
from utils.email_reporter import send_report_email
from utils.report_generator import ReportGenerator
from utils.screenshot import capture_screenshot


WEBSITE_URL = "https://www.suryasangam.com/"


def _safe_test_id(name: str) -> str:
    """Return a filesystem-safe short identifier for a test name."""
    safe = re.sub(r"[^0-9A-Za-z._-]", "_", name)
    return safe[:120]


def pytest_configure(config):
    """Initialize execution reporting state."""
    config.surya_report = ReportGenerator(WEBSITE_URL, "Chrome")


@pytest.fixture
def driver():
    """Create and quit a Chrome browser for each test."""
    active_driver = DriverFactory.create_chrome_driver()
    yield active_driver
    active_driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshots on failures and collect report data."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    screenshot_path = None
    page_html_path = ""
    console_log_path = ""
    traceback_path = ""
    chromedriver_version = ""
    browser_version = ""

    if report.failed and "driver" in item.fixturenames:
        active_driver = item.funcargs.get("driver")
        if active_driver:
            # Screenshot (existing helper)
            try:
                screenshot_path = capture_screenshot(active_driver, item.name)
            except Exception:
                screenshot_path = None

            # Artifacts directory per test
                # Artifacts directory (project root / reports)
                base_reports = Path(__file__).resolve().parent / "reports"
            artifacts_dir = base_reports / "artifacts" / _safe_test_id(item.nodeid or item.name)
            try:
                artifacts_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                artifacts_dir = base_reports / "artifacts"

            # Page HTML snapshot
            try:
                page_html_file = artifacts_dir / "page.html"
                page_html_file.write_text(active_driver.page_source or "", encoding="utf-8")
                page_html_path = str(page_html_file)
            except Exception:
                page_html_path = ""

            # Browser console logs (best-effort)
            try:
                logs = []
                try:
                    logs = active_driver.get_log("browser")
                except Exception:
                    logs = []
                console_file = artifacts_dir / "console.json"
                with open(console_file, "w", encoding="utf-8") as fh:
                    json.dump(logs, fh, ensure_ascii=False, indent=2)
                console_log_path = str(console_file)
            except Exception:
                console_log_path = ""

            # Full traceback text
            try:
                tb = getattr(report, "longreprtext", None) or str(report.longrepr)
                if tb:
                    tb_file = artifacts_dir / "traceback.txt"
                    tb_file.write_text(tb, encoding="utf-8")
                    traceback_path = str(tb_file)
            except Exception:
                traceback_path = ""

            # Driver/browser capabilities
            try:
                caps = getattr(active_driver, "capabilities", {}) or {}
                browser_version = caps.get("browserVersion") or caps.get("version") or caps.get("browser_version") or ""
                chromedriver_version = caps.get("chromedriverVersion") or (caps.get("chrome", {}).get("chromedriverVersion", "") if isinstance(caps.get("chrome", {}), dict) else caps.get("chromedriverVersion", ""))
            except Exception:
                chromedriver_version = ""
                browser_version = ""

    if report.passed:
        status = "PASS"
        reason = ""
    elif report.skipped:
        status = "SKIP"
        reason = str(report.longrepr)
    else:
        status = "FAIL"
        reason = str(report.longrepr)

    result_name = (
        item.function.__doc__.strip()
        if item.function.__doc__
        else item.name.replace("_", " ").title()
    )
    if hasattr(item, "callspec"):
        result_name = f"{result_name} [{item.callspec.id}]"

    result = {
        "name": result_name,
        "category": _test_category(item),
        "status": status,
        "duration": getattr(report, "duration", 0),
        "reason": reason,
        "screenshot": str(screenshot_path) if screenshot_path else "",
        "traceback": getattr(report, "longreprtext", "") or str(getattr(report, "longrepr", "")),
        "traceback_path": traceback_path,
        "captured_stdout": getattr(report, "capstdout", ""),
        "captured_stderr": getattr(report, "capstderr", ""),
        "page_html_path": page_html_path,
        "browser_console_log_path": console_log_path,
        "chromedriver_version": chromedriver_version,
        "browser_version": browser_version,
    }

    item.config.surya_report.add_result(result)


def _test_category(item):
    """Return the primary functional area marker for report grouping."""
    for marker in (
        "calculator",
        "services",
        "blog",
        "about",
        "homepage",
        "navigation",
        "buttons",
        "contact_validation",
        "blogs",
    ):
        if item.get_closest_marker(marker):
            if marker == "blogs":
                return "Blogs"
            return "Contact Validation" if marker == "contact_validation" else marker.title()
    return "General"


def pytest_sessionfinish(session, exitstatus):
    """Generate and optionally email the execution report at the end of the run."""
    report_file = session.config.surya_report.generate()
    if not is_email_configured():
        return

    try:
        send_report_email(report_file)
    except (EmailReportConfigError, OSError, smtplib.SMTPException) as error:
        terminal_reporter = session.config.pluginmanager.get_plugin("terminalreporter")
        if terminal_reporter:
            terminal_reporter.write_line(f"Report email was not sent: {error}")
