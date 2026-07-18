"""Pytest configuration, diagnostics, screenshots, and reporting."""

import json
import re
import smtplib
from pathlib import Path

import pytest

from utils.driver_factory import DriverFactory
from utils.email_reporter import EmailReportConfigError, is_email_configured
from utils.email_reporter import send_report_email
from utils.report_generator import ReportGenerator
from utils.screenshot import capture_screenshot


WEBSITE_URL = "https://www.suryasangam.com/"
REPORTS_DIR = Path(__file__).resolve().parent / "reports"


def _safe_test_id(name: str) -> str:
    """Return a filesystem-safe short identifier for a test name."""
    safe = re.sub(r"[^0-9A-Za-z._-]", "_", name)
    return safe[:120]


def _safe_value(value):
    """Serialize test parameters without exposing common secrets."""
    if isinstance(value, dict):
        return {
            str(key): (
                "[REDACTED]"
                if re.search(r"password|secret|token|api[_-]?key", str(key), re.I)
                else _safe_value(item)
            )
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [_safe_value(item) for item in value]
    try:
        json.dumps(value)
        return value
    except TypeError:
        return repr(value)


def pytest_configure(config):
    """Initialize execution reporting state."""
    config.surya_report = ReportGenerator(WEBSITE_URL, "Chrome")


@pytest.fixture
def driver():
    """Create and reliably quit a headless Chrome browser for each test."""
    active_driver = DriverFactory.create_chrome_driver()
    try:
        yield active_driver
    finally:
        active_driver.quit()


def _driver_state(active_driver):
    """Read browser state and capabilities without hiding the test failure."""
    state = {
        "url": "",
        "title": "",
        "browser_version": "",
        "chromedriver_version": "",
    }
    if not active_driver:
        return state

    try:
        state["url"] = active_driver.current_url or ""
    except Exception:
        pass
    try:
        state["title"] = active_driver.title or ""
    except Exception:
        pass
    try:
        capabilities = getattr(active_driver, "capabilities", {}) or {}
        state["browser_version"] = (
            capabilities.get("browserVersion")
            or capabilities.get("version")
            or capabilities.get("browser_version")
            or ""
        )
        chrome_caps = capabilities.get("chrome", {})
        state["chromedriver_version"] = (
            capabilities.get("chromedriverVersion")
            or (
                chrome_caps.get("chromedriverVersion", "")
                if isinstance(chrome_caps, dict)
                else ""
            )
        )
    except Exception:
        pass
    return state


def _write_failure_artifacts(item, report, active_driver):
    """Capture failure evidence once for the current test node."""
    paths = {
        "screenshot": "",
        "page_html_path": "",
        "browser_console_log_path": "",
        "performance_log_path": "",
        "traceback_path": "",
    }
    if not active_driver:
        return paths

    artifacts_dir = REPORTS_DIR / "artifacts" / _safe_test_id(item.nodeid)
    try:
        artifacts_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return paths

    try:
        screenshot_path = capture_screenshot(active_driver, item.nodeid)
        paths["screenshot"] = str(screenshot_path)
    except Exception:
        pass

    try:
        page_html_file = artifacts_dir / "page.html"
        page_html_file.write_text(active_driver.page_source or "", encoding="utf-8")
        paths["page_html_path"] = str(page_html_file)
    except Exception:
        pass

    for log_type, key, filename in (
        ("browser", "browser_console_log_path", "console.json"),
        ("performance", "performance_log_path", "performance.json"),
    ):
        try:
            log_entries = active_driver.get_log(log_type)
            log_file = artifacts_dir / filename
            log_file.write_text(
                json.dumps(log_entries, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            paths[key] = str(log_file)
        except Exception:
            pass

    try:
        traceback_text = getattr(report, "longreprtext", None) or str(report.longrepr)
        if traceback_text:
            traceback_file = artifacts_dir / "traceback.txt"
            traceback_file.write_text(traceback_text, encoding="utf-8")
            paths["traceback_path"] = str(traceback_file)
    except Exception:
        pass

    return paths


def _result_name(item):
    name = (
        item.function.__doc__.strip()
        if item.function.__doc__
        else item.name.replace("_", " ").title()
    )
    if hasattr(item, "callspec"):
        name = f"{name} [{item.callspec.id}]"
    return name


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Record call results and failures from setup, call, and teardown phases."""
    outcome = yield
    report = outcome.get_result()

    # Keep normal call results and any setup/teardown failure. This prevents
    # fixture failures from disappearing from the production report.
    if report.when != "call" and not report.failed:
        return

    active_driver = item.funcargs.get("driver") if "driver" in item.fixturenames else None
    state = _driver_state(active_driver)
    paths = _write_failure_artifacts(item, report, active_driver) if report.failed else {
        "screenshot": "",
        "page_html_path": "",
        "browser_console_log_path": "",
        "performance_log_path": "",
        "traceback_path": "",
    }

    if report.failed:
        status = "FAIL"
    elif report.skipped:
        status = "SKIP"
    else:
        status = "PASS"

    location = getattr(item, "location", ("", 0, ""))
    excinfo = getattr(report, "excinfo", None)
    exception_type = ""
    if excinfo is not None and getattr(excinfo, "type", None) is not None:
        exception_type = excinfo.type.__name__

    result = {
        "name": _result_name(item),
        "nodeid": item.nodeid,
        "source_file": str(location[0]),
        "source_line": int(location[1]) + 1,
        "category": _test_category(item),
        "phase": report.when,
        "status": status,
        "duration": round(float(getattr(report, "duration", 0)), 3),
        "reason": "" if status == "PASS" else str(report.longrepr),
        "exception_type": exception_type,
        "parameters": _safe_value(dict(getattr(item.callspec, "params", {})))
        if hasattr(item, "callspec")
        else {},
        "url": state["url"],
        "title": state["title"],
        "screenshot": paths["screenshot"],
        "traceback": getattr(report, "longreprtext", "")
        or str(getattr(report, "longrepr", "")),
        "traceback_path": paths["traceback_path"],
        "captured_stdout": getattr(report, "capstdout", ""),
        "captured_stderr": getattr(report, "capstderr", ""),
        "page_html_path": paths["page_html_path"],
        "browser_console_log_path": paths["browser_console_log_path"],
        "performance_log_path": paths["performance_log_path"],
        "chromedriver_version": state["chromedriver_version"],
        "browser_version": state["browser_version"],
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
        "contact",
        "contact_validation",
        "blogs",
    ):
        if item.get_closest_marker(marker):
            if marker in {"blogs", "blog"}:
                return "Blogs" if marker == "blogs" else "Blog"
            if marker == "contact_validation":
                return "Contact Validation"
            return marker.replace("_", " ").title()
    return "General"


def pytest_sessionfinish(session, exitstatus):
    """Generate reports and optionally email the execution result."""
    report_file = session.config.surya_report.generate(exitstatus)
    if not is_email_configured():
        return

    try:
        send_report_email(report_file)
    except (EmailReportConfigError, OSError, smtplib.SMTPException) as error:
        terminal_reporter = session.config.pluginmanager.get_plugin("terminalreporter")
        if terminal_reporter:
            terminal_reporter.write_line(f"Report email was not sent: {error}")
