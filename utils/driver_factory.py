"""Browser driver creation for Selenium tests."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:
    """Factory for creating configured WebDriver instances."""

    @staticmethod
    def create_chrome_driver():
        """Create and return a maximized Chrome WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--remote-allow-origins=*")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        driver.set_page_load_timeout(45)
        driver.set_script_timeout(20)
        return driver
