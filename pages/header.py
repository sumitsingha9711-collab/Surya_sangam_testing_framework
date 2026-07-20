"""Page object for the Surya Sangam header."""

from selenium.webdriver.common.by import By

from locators.header_locators import HeaderLocators
from pages.base_page import BasePage


class Header(BasePage):
    """Header interactions and assertions."""

    MENU_ITEMS = {
        "Home": HeaderLocators.HOME_LINK,
        "Store": HeaderLocators.STORE_LINK,
        "Surya SmartHub": HeaderLocators.SMART_HUB_LINK,
        "About Us": HeaderLocators.ABOUT_US_LINK,
        "Contact Us": HeaderLocators.CONTACT_US_LINK,
    }

    def click_logo(self):
        """Click the header logo."""
        self.click(HeaderLocators.LOGO_LINK)
        self.wait_for_page_load()

    def verify_navigation_menu(self):
        """Return True when the navigation menu and expected links are visible."""
        if not self.is_visible(HeaderLocators.NAVIGATION):
            return False
        return all(self.verify_menu_item_visible(item) for item in self.MENU_ITEMS)

    def click_navigation_item(self, item_name):
        """Click a navigation item by its visible label."""
        self.click(self._locator_for_menu_item(item_name))
        self.wait_for_page_load()

    def verify_menu_item_visible(self, item_name):
        """Return True when a named menu item is visible."""
        return self.is_visible(self._locator_for_menu_item(item_name))

    def get_navigation_links(self):
        """Return visible navigation link elements."""
        return [
            link
            for link in self.driver.find_elements(*HeaderLocators.NAVIGATION_LINKS)
            if link.is_displayed() and link.text.strip()
        ]

    def _locator_for_menu_item(self, item_name):
        if item_name in self.MENU_ITEMS:
            return self.MENU_ITEMS[item_name]
        return (By.XPATH, f"//header//a[normalize-space()='{item_name}']")
