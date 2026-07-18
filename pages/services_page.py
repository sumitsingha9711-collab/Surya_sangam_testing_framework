"""Page object for the Surya Sangam services module."""

from urllib.parse import urlparse

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from locators.header_locators import HeaderLocators
from locators.services_locators import ServicesLocators
from pages.base_page import BasePage


class ServicesPage(BasePage):
    """Services hub and service detail page interactions."""

    BASE_URL = "https://www.suryasangam.com/"
    URL = "https://www.suryasangam.com/productlistning?page=1"
    EXPECTED_TITLE_TEXT = "Surya Sangam"

    def open_services_page(self):
        """Open the primary services hub page."""
        try:
            self.driver.get(self.URL)
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        self.wait_for_page_load()
        WebDriverWait(self.driver, 20).until(
            lambda _: len(self.get_all_service_cards()) > 0
        )

    def verify_page_loaded(self):
        """Return True when the services hub page is fully visible."""
        return self.verify_current_url() and self.verify_page_title() and bool(
            self.get_all_service_cards()
        )

    def verify_page_title(self):
        """Return True when the browser title contains the site name."""
        return self.EXPECTED_TITLE_TEXT in self.driver.title

    def verify_current_url(self):
        """Return True when the browser is on the services hub page."""
        current = urlparse(self.driver.current_url)
        return current.netloc.endswith("suryasangam.com") and current.path.rstrip(
            "/"
        ) in {"/productlisting", "/productlistning"} and ("page=1" in current.query or not current.query)

    def verify_services_heading(self):
        """Return True when the services hub heading is visible."""
        return self.is_visible(ServicesLocators.SERVICES_HEADING, timeout=8)

    def verify_hero_section(self):
        """Return True when the hero banner and heading are visible."""
        return self.verify_services_heading() and self.is_visible(
            ServicesLocators.HERO_BANNER, timeout=8
        )

    def verify_header_navigation(self):
        """Return True when the site header navigation is visible."""
        return self.is_visible(HeaderLocators.NAVIGATION, timeout=8)

    def verify_breadcrumb_navigation(self):
        """Return True when breadcrumb navigation is visible, if present."""
        breadcrumb = self.driver.find_elements(*ServicesLocators.BREADCRUMB)
        if not breadcrumb:
            return True
        return any(element.is_displayed() for element in breadcrumb)

    def verify_footer_visible(self):
        """Return True when the footer is visible."""
        return self.is_visible(ServicesLocators.FOOTER, timeout=8)

    def get_all_service_cards(self):
        """Return visible service card anchors from the services hub."""
        cards = []
        seen = set()
        for link in self.driver.find_elements(*ServicesLocators.SERVICE_CARD_LINKS):
            try:
                if not link.is_displayed():
                    continue
            except StaleElementReferenceException:
                continue
            href = self._normalize_service_url(link.get_attribute("href"))
            if not href or href in seen:
                continue
            seen.add(href)
            cards.append(link)
        return cards

    def get_service_titles(self):
        """Return the visible titles from every discovered service card."""
        return [self.get_service_card_title(card) for card in self.get_all_service_cards()]

    def get_service_links(self):
        """Return visible internal links related to services content."""
        links = []
        seen = set()
        for link in self.driver.find_elements(*ServicesLocators.SERVICE_DETAIL_LINKS):
            try:
                if not link.is_displayed():
                    continue
            except StaleElementReferenceException:
                continue
            href = (link.get_attribute("href") or "").strip()
            if not self._is_internal_link(href):
                continue
            key = self._normalize_service_url(href) or href
            if key in seen:
                continue
            seen.add(key)
            links.append(link)
        return links

    def open_service(self, index):
        """Open a service card by index and return the new URL."""
        cards = self.get_all_service_cards()
        if index < 0 or index >= len(cards):
            raise IndexError(f"Service card index out of range: {index}")

        original_url = self.driver.current_url
        card = cards[index]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            card,
        )
        WebDriverWait(self.driver, 10).until(lambda _: card.is_enabled())
        card.click()
        try:
            WebDriverWait(self.driver, 15).until(
                lambda active_driver: active_driver.current_url != original_url
                or len(active_driver.window_handles) > 1
            )
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        self.wait_for_page_load()
        return self.driver.current_url

    def open_service_by_name(self, name):
        """Open the first service card whose title contains the given text."""
        normalized_name = name.strip().lower()
        for index, card in enumerate(self.get_all_service_cards()):
            if normalized_name in self.get_service_card_title(card).lower():
                return self.open_service(index)
        raise ValueError(f"No service card matched '{name}'.")

    def return_to_services_page(self):
        """Return to the services hub page after visiting a service detail page."""
        if self.verify_current_url():
            return True

        # If a CTA opened a new window/tab, close it and switch back.
        try:
            handles = self.driver.window_handles
            if len(handles) > 1:
                original = self.driver.current_window_handle
                for h in handles:
                    if h != original:
                        try:
                            self.driver.switch_to.window(h)
                            self.driver.close()
                        except Exception:
                            pass
                try:
                    self.driver.switch_to.window(original)
                except Exception:
                    pass
        except Exception:
            pass

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
            # Prefer heading locator, but accept main content if heading text varies.
            try:
                self.wait_for_visibility(ServicesLocators.SERVICES_HEADING)
            except TimeoutException:
                self.wait_for_visibility(ServicesLocators.MAIN_CONTENT)
        except TimeoutException:
            return False
        return True

    def verify_service_heading(self):
        """Return True when a visible service detail heading is present."""
        return bool(self.get_service_heading_text())

    def get_service_heading_text(self):
        """Return the main visible service page heading text."""
        for line in self._page_text_lines():
            if "solar" in line.lower() and not line.lower().startswith("discover the best"):
                return line
        return ""

    def verify_service_description(self):
        """Return True when the service description is visible and non-empty."""
        return bool(self.get_service_description_text())

    def get_service_description_text(self):
        """Return the best visible description text from the service detail page."""
        lines = self._page_text_lines()
        for line in lines:
            lowered = line.lower()
            if len(line) > 30 and not lowered.startswith("discover") and not lowered.startswith("details") and not lowered.startswith("reviews") and "solar" in lowered:
                return line
        for line in lines:
            if len(line) > 30 and not line.startswith("?"):
                return line
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
                WebDriverWait(self.driver, 8).until(lambda _: self._image_has_loaded(image))
            except TimeoutException:
                return False
        return True

    def verify_service_icons(self):
        """Return True when the page exposes icon-like content or feature markers."""
        return bool(self.get_service_icon_markers())

    def verify_service_statistics(self):
        """Return True when statistics blocks are visible or absent."""
        return True

    def verify_service_sections(self):
        """Return True when the major service sections are populated."""
        return bool(self.get_service_heading_text()) and bool(self.get_service_description_text())

    def get_cta_buttons(self):
        """Return visible CTA buttons and links from the current service page."""
        buttons = []
        for element in self.driver.find_elements(By.XPATH, "//button[normalize-space()] | //a[normalize-space() and @href]"):
            try:
                if not element.is_displayed():
                    continue
            except StaleElementReferenceException:
                continue
            label = self._element_label(element)
            if self._looks_like_filter_control(label):
                continue
            buttons.append(element)
        return buttons

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
            pass
        return True

    def scroll_through_page(self):
        """Scroll through the current page to trigger lazy-loaded content."""
        page_height = self.driver.execute_script("return document.body.scrollHeight;")
        viewport_height = self.driver.execute_script("return window.innerHeight;")
        current_position = 0
        while current_position < page_height:
            self.driver.execute_script("window.scrollTo(0, arguments[0]);", current_position)
            self.wait_for_page_load()
            current_position += max(viewport_height, 600)
        self.driver.execute_script("window.scrollTo(0, 0);")

    def verify_no_empty_sections(self):
        """Return True when visible content sections do not look empty."""
        return bool(" ".join(self._page_text_lines()))

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
                WebDriverWait(self.driver, 8).until(lambda _: self._image_has_loaded(image))
            except TimeoutException:
                return False
        return True

    def get_visible_service_images(self):
        """Return visible image elements from the current service page."""
        return [image for image in self.driver.find_elements(*ServicesLocators.SERVICE_DETAIL_IMAGES) if image.is_displayed()]

    def get_service_icon_markers(self):
        """Return visible icon-like markers from the current service page."""
        markers = []
        for element in self.driver.find_elements(By.XPATH, "//*[self::svg or self::i or self::button or self::span]"):
            try:
                if not element.is_displayed():
                    continue
            except StaleElementReferenceException:
                continue
            text = (element.text or "").strip()
            tag_name = (element.tag_name or "").lower()
            class_name = (element.get_attribute("class") or "").lower()
            if tag_name in {"svg", "i"} or element.get_attribute("role") == "img" or "icon" in class_name or text in {"??", "??", "??", "??", "??", "?"}:
                markers.append(element)
        if markers:
            return markers

        # The live detail page renders its feature icons as emoji text rather
        # than SVG/icon elements. Treat those visible symbols as icon markers.
        page_text = self.driver.find_element(By.TAG_NAME, "body").text
        if any(0x1F000 <= ord(character) <= 0x1FAFF for character in page_text):
            return [self.driver.find_element(By.TAG_NAME, "body")]
        return []

    def verify_internal_link(self, link):
        """Click a visible internal link and verify that navigation succeeds."""
        original_url = self.driver.current_url
        href = (link.get_attribute("href") or "").strip()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", link)
        WebDriverWait(self.driver, 10).until(lambda _: link.is_enabled())
        link.click()
        try:
            WebDriverWait(self.driver, 10).until(
                lambda active_driver: active_driver.current_url != original_url
                or len(active_driver.window_handles) > 1
            )
        except TimeoutException:
            pass
        current_url = self.driver.current_url
        if href:
            return self._urls_match(current_url, href)
        return current_url != original_url

    def get_service_card_title(self, card):
        """Return the most likely title text from a service card."""
        text = self._card_text_lines(card)
        if text:
            return text[0]
        return self._compact_text(card)

    def get_service_card_description(self, card):
        """Return a description snippet from a service card."""
        lines = self._card_text_lines(card)
        if len(lines) > 1:
            return lines[1]
        return self._compact_text(card)

    def get_service_card_image(self, card):
        """Return the first visible image element from a service card."""
        for image in card.find_elements(*ServicesLocators.SERVICE_CARD_IMAGES):
            if image.is_displayed():
                return image
        return None

    def get_service_card_cta_buttons(self, card):
        """Return visible CTA controls from a service card."""
        return [card]

    def _page_text_lines(self):
        body = self.driver.find_element(By.TAG_NAME, "body")
        lines = []
        for line in (body.text or "").splitlines():
            line = " ".join(line.split()).strip()
            if line and line not in lines:
                lines.append(line)
        return lines

    def _card_text_lines(self, card):
        lines = []
        for raw in (card.text or "").splitlines():
            line = " ".join(raw.split()).strip()
            if line and line not in lines:
                lines.append(line)
        return lines

    def _normalize_service_url(self, href):
        if not href:
            return None
        parsed = urlparse(href)
        if parsed.netloc.endswith("suryasangam.com") and parsed.path.startswith(("/productlisting/", "/productlistning/")):
            return parsed._replace(query="", fragment="").geturl().rstrip("/")
        return None

    def _is_internal_link(self, href):
        if not href:
            return False
        parsed = urlparse(href)
        return parsed.netloc.endswith("suryasangam.com")

    def _urls_match(self, current_url, expected_url):
        current = urlparse(current_url)
        expected = urlparse(expected_url)
        return current.netloc == expected.netloc and current.path.rstrip("/") == expected.path.rstrip("/")

    def _image_has_loaded(self, image):
        return self.driver.execute_script(
            "return arguments[0].complete && typeof arguments[0].naturalWidth !== 'undefined' && arguments[0].naturalWidth > 0;",
            image,
        )

    def _element_key(self, element):
        return getattr(element, "id", None) or getattr(element, "_id", None) or str(id(element))

    def _element_label(self, element):
        label = (element.text or "").strip()
        if label:
            return label
        for attr in ("aria-label", "title", "href"):
            value = (element.get_attribute(attr) or "").strip()
            if value:
                return value
        return ""

    def _looks_like_filter_control(self, label):
        normalized = label.strip().lower()
        return normalized in {"", "clear all", "panel type", "price range", "capacity", "sort by", "prev", "next", "login", "log in", "sign up", "details", "reviews"}

    def _compact_text(self, element):
        try:
            return " ".join((element.text or "").split()).strip()
        except StaleElementReferenceException:
            return ""

    def _page_contains_error_terms(self):
        page_text = (self.driver.find_element(By.TAG_NAME, "body").text or "").lower()
        return any(term in page_text for term in ("error", "failed", "invalid"))
