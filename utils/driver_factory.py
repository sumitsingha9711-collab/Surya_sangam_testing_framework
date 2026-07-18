"""Browser driver creation for Selenium tests."""

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DriverFactory:
    """Factory for creating configured WebDriver instances."""

    @staticmethod
    def create_chrome_driver():
        """Create a Selenium-Manager-managed Chrome WebDriver.

        Chrome is visible by default for local runs. Set ``SELENIUM_HEADLESS=1``
        for CI or other environments without a GUI.
        """
        chrome_options = Options()
        if os.getenv("SELENIUM_HEADLESS", "0").strip().lower() in {"1", "true", "yes", "on"}:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--remote-allow-origins=*")
        chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL', 'performance': 'ALL'})

        # Selenium 4.6+ invokes Selenium Manager automatically when no service
        # executable is supplied. This avoids a separate driver download tool.
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(45)
        driver.set_script_timeout(20)
        return driver
