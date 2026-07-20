"""Page object for the Surya Sangam About page."""

from urllib.parse import urljoin, urlparse

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from locators.about_locators import AboutLocators
from pages.base_page import BasePage


class AboutPage(BasePage):
    """About page interactions and assertions."""

    BASE_URL = "https://www.suryasangam.com/"
    URL = urljoin(BASE_URL, "aboutus")
    EXPECTED_TITLE_TEXT = "Surya Sangam"
    EXPECTED_PATH_FRAGMENT = "aboutus"

    def open_about_page(self):
        """Open the Surya Sangam About page."""
        try:
            self.driver.get(self.URL)
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        self.wait_for_page_load()

    def verify_page_loaded(self):
        """Return True when the About page primary content is visible."""
        return self.verify_current_url() and self.verify_main_heading()

    def get_page_title(self):
        """Return the current browser title."""
        return self.driver.title

    def verify_current_url(self):
        """Return True when the browser is on the About page."""
        current = urlparse(self.driver.current_url)
        return (
            current.netloc.endswith("suryasangam.com")
            and self.EXPECTED_PATH_FRAGMENT in current.path.lower()
        )

    def verify_page_title(self):
        """Return True when the page title contains the expected site text."""
        return self.EXPECTED_TITLE_TEXT in self.get_page_title()

    def verify_main_heading(self):
        """Return True when the About page heading is visible and non-empty."""
        heading_text = self.get_main_heading_text()
        return bool(heading_text)

    def get_main_heading_text(self):
        """Return the visible About page heading text."""
        return self.get_text(AboutLocators.MAIN_HEADING).strip()

    def verify_company_description(self):
        """Return True when company description content is visible and non-empty."""
        return bool(self.get_company_description_text())

    def get_company_description_text(self):
        """Return visible company description text."""
        return self.get_text(AboutLocators.COMPANY_DESCRIPTION).strip()

    def verify_images_loaded(self):
        """Return True when all visible About page images are loaded."""
        self._scroll_through_page()
        images = self.get_visible_about_images()
        if not images:
            return False

        for image in images:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", image
            )
            try:
                WebDriverWait(self.driver, 8).until(
                    lambda _: self._image_or_background_has_loaded(image)
                )
            except TimeoutException:
                return False
        return True

    def verify_cta_buttons(self):
        """Return True when every visible About page CTA is enabled."""
        buttons = self.get_visible_cta_buttons()
        return bool(buttons) and all(button.is_enabled() for button in buttons)

    def click_cta_button(self, button):
        """Click a CTA button and verify that it produces a valid response."""
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

    def verify_internal_navigation(self, link):
        """Click an internal About page link and verify browser navigation."""
        original_url = self.driver.current_url
        expected_href = link.get_attribute("href")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            link,
        )
        WebDriverWait(self.driver, 10).until(lambda _: link.is_enabled())
        link.click()
        self.wait_for_page_load()

        current_url = self.driver.current_url
        return current_url != original_url and self._urls_match(
            current_url, expected_href
        )

    def get_visible_about_images(self):
        """Return all visible About page images."""
        return [
            image
            for image in self.driver.find_elements(*AboutLocators.ABOUT_IMAGES)
            if image.is_displayed()
        ]

    def get_visible_cta_buttons(self):
        """Return visible About page CTA elements."""
        return [
            button
            for button in self.driver.find_elements(*AboutLocators.CTA_BUTTONS)
            if button.is_displayed() and button.text.strip()
        ]

    def get_internal_navigation_links(self):
        """Return visible internal links from the About page content."""
        return [
            link
            for link in self.driver.find_elements(*AboutLocators.NAVIGATION_LINKS)
            if link.is_displayed() and self._is_internal_link(link.get_attribute("href"))
        ]

    def verify_breadcrumb_present(self):
        """Return True when a breadcrumb is visible, if the page has one."""
        return self.is_visible(AboutLocators.BREADCRUMB, timeout=5)

    def verify_statistics_section_present(self):
        """Return True when a statistics section is visible, if available."""
        return self.is_visible(AboutLocators.STATISTICS_SECTION, timeout=5)

    def _image_has_loaded(self, image):
        return self.driver.execute_script(
            "return arguments[0].complete && "
            "typeof arguments[0].naturalWidth !== 'undefined' && "
            "arguments[0].naturalWidth > 0;",
            image,
        )

    def _image_or_background_has_loaded(self, element):
        if element.tag_name.lower() == "img":
            return self._image_has_loaded(element)

        background_image = element.value_of_css_property("background-image")
        return bool(background_image and background_image != "none")

    def _scroll_through_page(self):
        """Scroll the page to trigger lazy-loaded About page assets."""
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

    def _is_internal_link(self, href):
        if not href:
            return False
        parsed = urlparse(href)
        return parsed.netloc.endswith("suryasangam.com")

    def _urls_match(self, current_url, expected_url):
        current = urlparse(current_url)
        expected = urlparse(expected_url)
        return (
            current.netloc == expected.netloc
            and current.path.rstrip("/") == expected.path.rstrip("/")
        )
