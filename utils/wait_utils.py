"""Explicit wait helper functions."""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


DEFAULT_TIMEOUT = 15


def wait_for_element_visible(driver, locator, timeout=DEFAULT_TIMEOUT):
    """Wait until an element is visible and return it."""
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def wait_for_element_clickable(driver, locator, timeout=DEFAULT_TIMEOUT):
    """Wait until an element is clickable and return it."""
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def wait_for_all_elements_present(driver, locator, timeout=DEFAULT_TIMEOUT):
    """Wait until all matching elements are present and return them."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located(locator)
    )


def wait_for_document_ready(driver, timeout=DEFAULT_TIMEOUT):
    """Wait until the DOM is ready for Selenium interactions.

    The driver deliberately uses Selenium's ``eager`` page-load strategy, so
    waiting for ``complete`` here would reintroduce timeouts from unrelated
    third-party resources. ``interactive`` guarantees the DOM is available;
    ``complete`` remains valid when it is reached.
    """
    WebDriverWait(driver, timeout).until(
        lambda active_driver: active_driver.execute_script(
            "return document.readyState"
        )
        in {"interactive", "complete"}
    )
