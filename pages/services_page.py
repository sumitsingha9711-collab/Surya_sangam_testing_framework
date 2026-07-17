"""Page object for the Surya Sangam services module."""

from urllib.parse import urlparse

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.header_locators import HeaderLocators
from locators.services_locators import ServicesLocators
from pages.base_page import BasePage


class ServicesPage(BasePage):
    """Services hub and service detail page interactions."""

    BASE_URL = "https://www.suryasangam.com/"
    URL = "https://www.suryasangam.com/productlisting?page=1"
    EXPECTED_TITLE_TEXT = "Surya Sangam"

    def open_services_page(self):
        """Open the primary services hub page."""
        try:
            self.driver.get(self.URL)
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        self.wait_for_page_load()
        # Prefer waiting for the services heading, but if the site uses a
        # different heading string, fall back to the main content area to
        # detect that the page has loaded.
        try:
            self.wait_for_visibility(ServicesLocators.SERVICES_HEADING)
        except TimeoutException:
            self.wait_for_visibility(ServicesLocators.MAIN_CONTENT)
        self._wait_for_service_cards()

    def verify_page_loaded(self):
        """Return True when the services hub page is fully visible."""
        return (
            self.verify_current_url()
            and self.verify_page_title()
            and self.is_visible(ServicesLocators.SERVICES_HEADING)
            and bool(self.get_all_service_cards())
        )

    def verify_page_title(self):
        """Return True when the browser title contains the site name."""
        return self.EXPECTED_TITLE_TEXT in self.driver.title

    def verify_current_url(self):
        """Return True when the browser is on the services hub page."""
        current = urlparse(self.driver.current_url)
        return (
            current.netloc.endswith("suryasangam.com")
            and "productlisting" in current.path.lower()
        )

    def verify_services_heading(self):
        """Return True when the services hub heading is visible."""
        return self.is_visible(ServicesLocators.SERVICES_HEADING)

    def verify_hero_section(self):
        """Return True when the hero banner and heading are visible."""
        return self.verify_services_heading() and self.is_visible(ServicesLocators.HERO_BANNER)

    def verify_header_navigation(self):
        """Return True when the site header navigation is visible."""
        if not self.is_visible(HeaderLocators.NAVIGATION):
            return False
        return all(
            self.is_visible(locator)
            for locator in (
                HeaderLocators.HOME_LINK,
                HeaderLocators.STORE_LINK,
                HeaderLocators.SMART_HUB_LINK,
                HeaderLocators.ABOUT_US_LINK,
                HeaderLocators.CONTACT_US_LINK,
            )
        )

    def verify_breadcrumb_navigation(self):
        """Return True when breadcrumb navigation is visible, if present."""
        breadcrumb = self.driver.find_elements(*ServicesLocators.BREADCRUMB)
        if not breadcrumb:
            return True
        return any(element.is_displayed() for element in breadcrumb)

    def verify_footer_visible(self):
        """Return True when the footer is visible."""
        return self.is_visible(ServicesLocators.FOOTER)

    def get_all_service_cards(self):
        """Return visible service card containers from the services hub."""
        cards = []
        seen = set()

        for card in self.driver.find_elements(*ServicesLocators.SERVICE_CARD_CONTAINERS):
            if not card.is_displayed():
                continue
            key = self._element_key(card)
            if key in seen:
                continue
            seen.add(key)
            cards.append(card)

        if cards:
            return cards

        for title in self.driver.find_elements(*ServicesLocators.SERVICE_CARD_TITLES):
            if not title.is_displayed():
                continue
            card = self._nearest_card_container(title)
            key = self._element_key(card)
            if key in seen:
                continue
            seen.add(key)
            cards.append(card)

        return cards

    def get_service_titles(self):
        """Return the visible titles from every discovered service card."""
        titles = []
        for card in self.get_all_service_cards():
            title = self.get_service_card_title(card)
            if title:
                titles.append(title)
        return titles

    def get_service_links(self):
        """Return visible internal links related to services content."""
        links = []
        seen = set()

        for link in self.driver.find_elements(*ServicesLocators.SERVICE_INTERNAL_LINKS):
            if not link.is_displayed():
                continue
            href = (link.get_attribute("href") or "").strip()
            if not self._is_internal_link(href):
                continue
            key = (href, (link.text or "").strip())
            if key in seen:
                continue
            seen.add(key)
            links.append(link)

        for button in self.get_cta_buttons():
            href = (button.get_attribute("href") or "").strip()
            if href and self._is_internal_link(href):
                key = (href, (button.text or "").strip())
                if key not in seen:
                    seen.add(key)
                    links.append(button)

        return links

    def open_service(self, index):
        """Open a service card by index and return the new URL."""
        cards = self.get_all_service_cards()
        if index < 0 or index >= len(cards):
            raise IndexError(f"Service card index out of range: {index}")

        original_url = self.driver.current_url
        card = cards[index]
        target = self._service_card_click_target(card)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            target,
        )
        WebDriverWait(self.driver, 10).until(lambda _: target.is_displayed())
        WebDriverWait(self.driver, 10).until(lambda _: target.is_enabled())
        target.click()
        self.wait_for_page_load()

        try:
            WebDriverWait(self.driver, 10).until(
                lambda active_driver: active_driver.current_url != original_url
                or len(active_driver.window_handles) > 1
            )
        except TimeoutException:
            pass
        return self.driver.current_url

    def open_service_by_name(self, name):
        """Open the first service card whose title contains the given text."""
        normalized_name = name.strip().lower()
        cards = self.get_all_service_cards()
        for index, card in enumerate(cards):
            title = self.get_service_card_title(card).lower()
            if normalized_name in title:
                return self.open_service(index)
        raise ValueError(f"No service card matched '{name}'.")

    def return_to_services_page(self):
        """Return to the services hub page after visiting a service detail page."""
        if self.verify_current_url():
            return True

        try:
            self.driver.back()
            self.wait_for_page_load()
        except TimeoutException:
            self.driver.get(self.URL)
            self.wait_for_page_load()

        if not self.verify_current_url():
            self.driver.get(self.URL)
            self.wait_for_page_load()

        try:
            self.wait_for_visibility(ServicesLocators.SERVICES_HEADING)
        except TimeoutException:
            return False
        return True

    def verify_service_heading(self):
        """Return True when a visible service detail heading is present."""
        heading = self.get_service_heading_text()
        return bool(heading) and self.is_visible(ServicesLocators.SERVICE_DETAIL_HEADING)

    def get_service_heading_text(self):
        """Return the main visible service page heading text."""
        heading = self._first_visible_text(ServicesLocators.SERVICE_DETAIL_HEADING)
        return heading.strip()

    def verify_service_description(self):
        """Return True when the service description is visible and non-empty."""
        return bool(self.get_service_description_text())

    def get_service_description_text(self):
        """Return the best visible description text from the service detail page."""
        paragraphs = self._visible_texts(ServicesLocators.SERVICE_DETAIL_DESCRIPTION)
        if paragraphs:
            return paragraphs[0].strip()
        return ""

    def verify_service_images(self):
        """Return True when all visible service images are loaded."""
        images = self.get_visible_service_images()
        if not images:
            return False

        for image in images:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                image,
            )
            try:
                WebDriverWait(self.driver, 8).until(
                    lambda _: self._image_has_loaded(image)
                )
            except TimeoutException:
                return False
        return True

    def verify_service_icons(self):
        """Return True when any visible iconography on the page is displayed."""
        icons = self.get_visible_service_icons()
        if not icons:
            return True
        return all(icon.is_displayed() for icon in icons)

    def verify_service_statistics(self):
        """Return True when statistics blocks are visible or absent."""
        statistics = self.get_service_statistics()
        if not statistics:
            return True
        return all(stat.is_displayed() for stat in statistics)

    def verify_service_sections(self):
        """Return True when the major service sections are populated."""
        return (
            self.verify_service_heading()
            and self.verify_service_description()
            and self.is_visible(ServicesLocators.SERVICE_DETAIL_HERO_SECTION)
            and self.verify_footer_visible()
        )

    def get_cta_buttons(self):
        """Return visible CTA buttons and links from the current service page."""
        controls = []
        for element in self.driver.find_elements(
            By.XPATH,
            "//main//a[normalize-space() and @href] | //main//button[normalize-space()]"):
            if not element.is_displayed():
                continue
            label = self._element_label(element)
            if self._looks_like_filter_control(label):
                continue
            controls.append(element)
        return controls

    def verify_cta_buttons(self):
        """Return True when visible CTA controls are enabled."""
        buttons = self.get_cta_buttons()
        return bool(buttons) and all(button.is_enabled() for button in buttons)

    def click_cta_button(self, button):
        """Click a CTA button and verify that the action is handled safely."""
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
                or not self._page_contains_error_terms()
            )
        except TimeoutException:
            return button.is_enabled() or self.driver.current_url != original_url
        return True

    def scroll_through_page(self):
        """Scroll through the current page to trigger lazy-loaded content."""
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

    def verify_no_empty_sections(self):
        """Return True when visible content sections do not look empty."""
        containers = self.driver.find_elements(
            By.XPATH,
            "//main//*[self::section or self::article or self::div][contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'section') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'card') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'feature') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'content') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'hero') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'grid') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'stat') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cta')]",
        )
        for container in containers:
            if not container.is_displayed():
                continue
            text = (container.text or "").strip()
            children = container.find_elements(
                By.XPATH,
                ".//img | .//a | .//button | .//ul/li | .//ol/li | .//svg | .//i",
            )
            if not text and not children:
                return False
        return True

    def verify_all_images_loaded(self):
        """Return True when every visible image on the page has loaded."""
        images = self.get_visible_service_images()
        if not images:
            return False

        for image in images:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                image,
            )
            try:
                WebDriverWait(self.driver, 8).until(
                    lambda _: self._image_has_loaded(image)
                )
            except TimeoutException:
                return False
        return True

    def get_visible_service_images(self):
        """Return visible image elements from the current service page."""
        return [
            image
            for image in self.driver.find_elements(*ServicesLocators.SERVICE_DETAIL_IMAGES)
            if image.is_displayed()
        ]

    def get_visible_service_icons(self):
        """Return visible icon elements from the current service page."""
        return [
            icon
            for icon in self.driver.find_elements(*ServicesLocators.SERVICE_DETAIL_ICONS)
            if icon.is_displayed()
        ]

    def get_service_statistics(self):
        """Return visible statistics elements from the current service page."""
        return [
            stat
            for stat in self.driver.find_elements(*ServicesLocators.SERVICE_DETAIL_STATISTICS)
            if stat.is_displayed() and (stat.text or "").strip()
        ]

    def verify_internal_link(self, link):
        """Click a visible internal link and verify that navigation succeeds."""
        original_url = self.driver.current_url
        expected_href = (link.get_attribute("href") or "").strip()
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            link,
        )
        WebDriverWait(self.driver, 10).until(lambda _: link.is_enabled())
        link.click()
        self.wait_for_page_load()

        current_url = self.driver.current_url
        if expected_href:
            return self._urls_match(current_url, expected_href)
        return current_url != original_url and self.verify_page_title()

    def get_service_card_title(self, card):
        """Return the most likely title text from a service card."""
        title = self._first_visible_text_from_card(
            card,
            "./*[self::h2 or self::h3 or self::h4 or self::h5] | .//*[self::h2 or self::h3 or self::h4 or self::h5]",
        )
        if title:
            return title.strip()
        return self._compact_text(card)

    def get_service_card_description(self, card):
        """Return a description snippet from a service card."""
        return self._first_visible_text_from_card(
            card,
            "./p[normalize-space()] | .//p[normalize-space()] | .//*[self::span or self::div][normalize-space()]",
        ).strip()

    def get_service_card_image(self, card):
        """Return the first visible image element from a service card."""
        for image in card.find_elements(*ServicesLocators.SERVICE_CARD_IMAGE):
            if image.is_displayed():
                return image
        return None

    def get_service_card_cta_buttons(self, card):
        """Return visible CTA controls from a service card."""
        return [
            control
            for control in card.find_elements(*ServicesLocators.SERVICE_CARD_CTA_BUTTONS)
            if control.is_displayed() and control.is_enabled()
        ]

    def _wait_for_service_cards(self):
        try:
            # Allow more time for lazy-loaded service cards to appear.
            WebDriverWait(self.driver, 30).until(
                lambda _: len(self.get_all_service_cards()) > 0
            )
        except TimeoutException:
            return False
        return True

    def _nearest_card_container(self, element):
        try:
            return element.find_element(
                By.XPATH,
                "ancestor::*[self::article or self::section or self::li or self::div][.//img and (.//a or .//button or @role='button')][1]",
            )
        except Exception:
            return element

    def _service_card_click_target(self, card):
        for candidate in card.find_elements(
            By.XPATH,
            ".//a[normalize-space() and @href] | .//button[normalize-space()] | .//*[@role='button'][normalize-space()]",
        ):
            if candidate.is_displayed() and candidate.is_enabled():
                return candidate
        return card

    def _first_visible_text(self, locator):
        elements = self.driver.find_elements(*locator)
        for element in elements:
            if element.is_displayed():
                text = (element.text or "").strip()
                if text:
                    return text
        return ""

    def _first_visible_text_from_card(self, card, xpath):
        try:
            for element in card.find_elements(By.XPATH, xpath):
                if element.is_displayed():
                    text = (element.text or "").strip()
                    if text:
                        return text
        except StaleElementReferenceException:
            return ""
        return ""

    def _visible_texts(self, locator):
        texts = []
        for element in self.driver.find_elements(*locator):
            if element.is_displayed():
                text = (element.text or "").strip()
                if text:
                    texts.append(text)
        return texts

    def _compact_text(self, element):
        try:
            return " ".join((element.text or "").split()).strip()
        except StaleElementReferenceException:
            return ""

    def _element_key(self, element):
        return getattr(element, "id", None) or getattr(element, "_id", None) or str(id(element))

    def _element_label(self, element):
        label = (element.text or "").strip()
        if label:
            return label
        aria_label = (element.get_attribute("aria-label") or "").strip()
        if aria_label:
            return aria_label
        title = (element.get_attribute("title") or "").strip()
        if title:
            return title
        return (element.get_attribute("href") or "").strip()

    def _looks_like_filter_control(self, label):
        normalized = label.strip().lower()
        return normalized in {
            "",
            "clear all",
            "panel type",
            "price range",
            "capacity",
            "sort by",
            "prev",
            "next",
            "login",
            "log in",
            "sign up",
        }

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

    def _image_has_loaded(self, image):
        return self.driver.execute_script(
            "return arguments[0].complete && "
            "typeof arguments[0].naturalWidth !== 'undefined' && "
            "arguments[0].naturalWidth > 0;",
            image,
        )

    def _page_contains_error_terms(self):
        page_text = (self.driver.find_element(By.TAG_NAME, "body").text or "").lower()
        return any(term in page_text for term in ("error", "failed", "invalid"))

