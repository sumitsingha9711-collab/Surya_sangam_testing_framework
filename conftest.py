"""Pytest configuration, screenshots, and text reporting."""

import smtplib

import pytest

from utils.driver_factory import DriverFactory
from utils.email_reporter import EmailReportConfigError, is_email_configured
from utils.email_reporter import send_report_email
from utils.report_generator import ReportGenerator
from utils.screenshot import capture_screenshot


WEBSITE_URL = "https://www.suryasangam.com/"


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
    if report.failed and "driver" in item.fixturenames:
        active_driver = item.funcargs.get("driver")
        if active_driver:
            screenshot_path = capture_screenshot(active_driver, item.name)

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

    item.config.surya_report.add_result(
        {
            "name": result_name,
            "category": _test_category(item),
            "status": status,
            "duration": report.duration,
            "reason": reason,
            "screenshot": str(screenshot_path) if screenshot_path else "",
        }
    )


def _test_category(item):
    """Return the primary functional area marker for report grouping."""
    for marker in (
        "calculator",
        "services",
        "about",
        "homepage",
        "navigation",
        "buttons",
        "contact_validation",
    ):
        if item.get_closest_marker(marker):
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
