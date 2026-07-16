"""Base page object with reusable Selenium actions."""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from utils.wait_utils import (
    wait_for_document_ready,
    wait_for_element_clickable,
    wait_for_element_visible,
)


class BasePage:
    """Common page object behavior shared by all pages."""

    def __init__(self, driver):
        """Store the active WebDriver instance."""
        self.driver = driver

    def click(self, locator):
        """Click an element after waiting for it to be clickable."""
        element = self.wait_for_clickable(locator)
        self.scroll_to_element(locator)
        element.click()

    def type(self, locator, text):
        """Type text into a visible field."""
        element = self.wait_for_visibility(locator)
        element.send_keys(text)

    def clear(self, locator):
        """Clear a visible field."""
        element = self.wait_for_visibility(locator)
        element.clear()

    def get_text(self, locator):
        """Return visible text from an element."""
        return self.wait_for_visibility(locator).text

    def is_visible(self, locator, timeout=10):
        """Return True when an element is visible within the timeout."""
        try:
            wait_for_element_visible(self.driver, locator, timeout)
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, locator):
        """Scroll the target element into the center of the viewport."""
        element = self.wait_for_visibility(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )
        return element

    def wait_for_visibility(self, locator, timeout=15):
        """Wait for an element to become visible."""
        return wait_for_element_visible(self.driver, locator, timeout)

    def wait_for_clickable(self, locator, timeout=15):
        """Wait for an element to become clickable."""
        return wait_for_element_clickable(self.driver, locator, timeout)

    def wait_for_page_load(self, timeout=15):
        """Wait for the current document to finish loading."""
        wait_for_document_ready(self.driver, timeout)

    def hover(self, locator):
        """Move the mouse over an element."""
        element = self.wait_for_visibility(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        return element
