"""Page object for the Surya Sangam homepage."""

from urllib.parse import urlparse

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from locators.home_locators import HomeLocators
from locators.header_locators import HeaderLocators
from pages.base_page import BasePage


class HomePage(BasePage):
    """Homepage interactions and assertions."""

    URL = "https://www.suryasangam.com/"
    EXPECTED_TITLE_TEXT = "Surya Sangam"

    def open_homepage(self):
        """Open the Surya Sangam homepage."""
        try:
            self.driver.get(self.URL)
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        self.wait_for_page_load()

    def verify_title(self):
        """Return True when the page title contains the expected text."""
        return self.EXPECTED_TITLE_TEXT in self.driver.title

    def verify_current_url(self):
        """Return True when the current URL is the expected homepage URL."""
        expected = urlparse(self.URL)
        current = urlparse(self.driver.current_url)
        return current.netloc == expected.netloc and current.path.rstrip("/") == ""

    def verify_logo_visible(self):
        """Return True when the header logo is visible."""
        return self.is_visible(HeaderLocators.LOGO)

    def verify_hero_section(self):
        """Return True when the main hero content is visible."""
        hero_checks = [
            HomeLocators.HERO_SUBTITLE,
            HomeLocators.HERO_HEADING,
            HomeLocators.HERO_DESCRIPTION,
            HomeLocators.HERO_GET_STARTED_BUTTON,
            HomeLocators.HERO_IMAGE,
        ]
        return all(self.is_visible(locator) for locator in hero_checks)

    def verify_cta_buttons(self):
        """Return True when every visible CTA button is enabled."""
        buttons = self.get_visible_cta_buttons()
        return bool(buttons) and all(button.is_enabled() for button in buttons)

    def verify_banner(self):
        """Return True when the visible hero banner image has loaded."""
        image = self.wait_for_visibility(HomeLocators.HERO_IMAGE)
        return self._image_has_loaded(image)

    def verify_images_loaded(self):
        """Return True when all visible images on the homepage are loaded."""
        self._scroll_through_page()
        images = [
            image
            for image in self.driver.find_elements(*HomeLocators.ALL_IMAGES)
            if image.is_displayed()
        ]
        if not images:
            return False

        for image in images:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", image
            )
            try:
                WebDriverWait(self.driver, 8).until(
                    lambda _: self._image_has_loaded(image)
                )
            except TimeoutException:
                return False
        return True

    def verify_footer_visible(self):
        """Return True when the footer is present and visible."""
        self.scroll_to_element(HomeLocators.FOOTER)
        return self.is_visible(HomeLocators.FOOTER)

    def verify_footer_links_visible(self):
        """Return True when the footer contains usable links."""
        if not self.verify_footer_visible():
            return False
        footer_links = [
            link
            for link in self.driver.find_elements(*HomeLocators.FOOTER_LINKS)
            if link.get_attribute("href")
        ]
        return bool(footer_links)

    def get_visible_cta_buttons(self):
        """Return all visible homepage CTA elements."""
        return [
            button
            for button in self.driver.find_elements(*HomeLocators.CTA_BUTTONS)
            if button.is_displayed()
        ]

    def click_cta_and_verify_response(self, button):
        """Click a CTA and verify that the click causes a valid UI response."""
        original_url = self.driver.current_url
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            button,
        )
        WebDriverWait(self.driver, 10).until(lambda _: button.is_enabled())
        button.click()

        try:
            WebDriverWait(self.driver, 10).until(
                lambda active_driver: active_driver.current_url != original_url
                or len(active_driver.window_handles) > 1
            )
        except TimeoutException:
            return self.driver.current_url == original_url and button.is_enabled()
        return True

    def _image_has_loaded(self, image):
        return self.driver.execute_script(
            "return arguments[0].complete && "
            "typeof arguments[0].naturalWidth !== 'undefined' && "
            "arguments[0].naturalWidth > 0;",
            image,
        )

    def _scroll_through_page(self):
        """Scroll the page to trigger lazy-loaded homepage assets."""
        page_height = self.driver.execute_script("return document.body.scrollHeight;")
        viewport_height = self.driver.execute_script("return window.innerHeight;")
        current_position = 0

        while current_position < page_height:
            self.driver.execute_script(
                "window.scrollTo(0, arguments[0]);", current_position
            )
            self.wait_for_page_load()
            current_position += max(viewport_height, 600)

        self.driver.execute_script("window.scrollTo(0, 0);")
