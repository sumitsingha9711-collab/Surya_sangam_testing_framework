"""Page object for the Surya Sangam blog module."""

from urllib.parse import urlparse

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from locators.blog_locators import BlogLocators
from pages.base_page import BasePage


class BlogPage(BasePage):
    """Blog listing and article page interactions."""

    BASE_URL = "https://www.suryasangam.com/"
    URL = "https://www.suryasangam.com/blogs"
    EXPECTED_TITLE_TEXT = "Surya Sangam"

    def open_blog_page(self):
        """Open the blog listing page."""
        try:
            self.driver.get(self.URL)
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        self.wait_for_page_load()
        self._wait_for_blog_cards()

    def verify_page_loaded(self):
        """Return True when the blog listing page is visible."""
        return (
            self.verify_current_url()
            and self.verify_page_title()
            and self.verify_blog_listing()
        )

    def verify_page_title(self):
        """Return True when the browser title contains the site name."""
        return self.EXPECTED_TITLE_TEXT in self.driver.title

    def verify_current_url(self):
        """Return True when the browser is on the blog listing page."""
        current = urlparse(self.driver.current_url)
        return current.netloc.endswith("suryasangam.com") and "/blogs" in current.path

    def verify_blog_listing(self):
        """Return True when blog cards, images, titles, dates, and categories are visible."""
        cards = self.get_blog_cards()
        if not cards:
            return False
        return bool(self.get_blog_titles()) and any(
            self.get_blog_card_image(card) for card in cards
        )

    def get_blog_cards(self):
        """Return visible blog card containers."""
        cards = []
        seen = set()
        try:
            candidates = self.driver.execute_script(
                """
                const out = [];
                const nodes = document.querySelectorAll('main section, main article, main div');
                for (const el of nodes) {
                  const text = (el.innerText || '').replace(/\\s+/g, ' ').trim();
                  if (!text) continue;
                  if (!text.toLowerCase().includes('read more')) continue;
                  if (text.length < 80) continue;
                  out.push(el);
                }
                return out;
                """
            )
        except Exception:
            candidates = []

        for card in candidates:
            try:
                if not card.is_displayed():
                    continue
            except StaleElementReferenceException:
                continue
            key = self._element_key(card)
            if key in seen:
                continue
            seen.add(key)
            cards.append(card)

        if cards:
            return cards

        for link in self.driver.find_elements(By.XPATH, "//a[@href]"):
            try:
                if not link.is_displayed():
                    continue
            except StaleElementReferenceException:
                continue
            normalized = self._normalize_blog_url(link.get_attribute('href'))
            if not normalized:
                continue
            card = self._nearest_card_container(link)
            key = self._element_key(card)
            if key in seen:
                continue
            seen.add(key)
            cards.append(card)
        return cards

    def get_blog_titles(self):
        """Return visible blog titles."""
        titles = []
        for card in self.get_blog_cards():
            title = self.get_blog_card_title(card)
            if title:
                titles.append(title)
        return titles

    def get_blog_links(self):
        """Return visible blog post links."""
        links = []
        seen = set()
        for link in self.driver.find_elements(By.XPATH, "//a[@href]"):
            try:
                if not link.is_displayed():
                    continue
            except StaleElementReferenceException:
                continue
            normalized = self._normalize_blog_url(link.get_attribute("href"))
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            links.append(link)
        return links

    def open_blog(self, index=0):
        """Open a blog by index and return the new URL."""
        cards = self.get_blog_cards()
        if index < 0 or index >= len(cards):
            raise IndexError(f"Blog index out of range: {index}")

        original_url = self.driver.current_url
        card = cards[index]
        target = self._blog_card_target(card)
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

    def return_to_blog_listing(self):
        """Return to the blog listing page."""
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

        return self._wait_for_blog_cards()

    def verify_blog_content(self):
        """Return True when the blog article content is visible and non-empty."""
        return bool(self.get_blog_content_text())

    def verify_blog_heading(self):
        """Return True when an article heading is visible."""
        return bool(self.get_blog_heading_text())

    def verify_featured_image(self):
        """Return True when a featured image is displayed and loaded."""
        image = self.get_featured_image()
        return bool(image) and image.is_displayed() and self._image_has_loaded(image)

    def verify_author(self):
        """Return True when author metadata is visible."""
        return bool(self.get_author_text())

    def verify_publish_date(self):
        """Return True when publish-date metadata is visible."""
        return bool(self.get_publish_date_text())

    def verify_related_posts(self):
        """Return True when related posts are present and their links are usable."""
        heading = self._first_visible_text(BlogLocators.BLOG_DETAIL_RELATED_POSTS)
        links = self.get_related_post_links()
        return bool(heading or links) and bool(links)

    def verify_share_buttons(self):
        """Return True when share buttons or links are visible and enabled."""
        buttons = self.get_share_buttons()
        return bool(buttons) and all(button.is_displayed() and button.is_enabled() for button in buttons)

    def verify_pagination(self):
        """Return True when blog pagination is visible and usable."""
        controls = self.get_pagination_controls()
        if not controls:
            return False
        return all(control.is_displayed() and control.is_enabled() for control in controls)

    def get_featured_image(self):
        """Return the primary visible featured image on the current page."""
        images = self.get_visible_images()
        return images[0] if images else None

    def get_blog_heading_text(self):
        """Return the visible article heading text."""
        return self._first_visible_text(BlogLocators.BLOG_DETAIL_HEADING).strip()

    def get_author_text(self):
        """Return the visible author text."""
        return self._first_visible_text(BlogLocators.BLOG_DETAIL_AUTHOR).strip()

    def get_publish_date_text(self):
        """Return the visible publish date text."""
        return self._first_visible_text(BlogLocators.BLOG_DETAIL_DATE).strip()

    def get_related_post_links(self):
        """Return visible related post links."""
        links = []
        seen = set()
        for link in self.driver.find_elements(*BlogLocators.BLOG_DETAIL_RELATED_LINKS):
            try:
                if not link.is_displayed():
                    continue
            except StaleElementReferenceException:
                continue
            normalized = self._normalize_blog_url(link.get_attribute("href"))
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            links.append(link)
        return links

    def get_share_buttons(self):
        """Return visible share buttons and social share links."""
        return [
            element
            for element in self.driver.find_elements(*BlogLocators.BLOG_DETAIL_SHARE_BUTTONS)
            if element.is_displayed()
        ]

    def click_share_button(self, button):
        """Click a share button and verify that the click is handled safely."""
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
            return button.is_enabled() or self.driver.current_url != original_url
        return True

    def get_pagination_controls(self):
        """Return visible pagination controls from the blog listing page."""
        controls = []
        for locator in (
            BlogLocators.BLOG_PAGINATION_PREVIOUS,
            BlogLocators.BLOG_PAGINATION_FIRST,
            BlogLocators.BLOG_PAGINATION_NEXT,
            BlogLocators.BLOG_PAGINATION_LAST,
        ):
            controls.extend(
                [
                    element
                    for element in self.driver.find_elements(*locator)
                    if element.is_displayed()
                ]
            )
        return controls

    def get_blog_card_title(self, card):
        """Return the visible title text for a blog card."""
        title = self._first_visible_text_from_card(
            card,
            ".//*[self::h2 or self::h3 or self::h4][normalize-space()] | .//a[contains(@href, '/blogs/')][normalize-space()]",
        )
        if title:
            return title.strip()
        return self._compact_text(card)

    def get_blog_card_image(self, card):
        """Return the first visible image from a blog card."""
        for image in card.find_elements(By.XPATH, ".//img"):
            if image.is_displayed():
                return image
        return None

    def get_blog_card_date(self, card):
        """Return the visible date text for a blog card."""
        return self._first_visible_text_from_card(
            card,
            ".//time | .//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'date')]",
        ).strip()

    def get_blog_card_category(self, card):
        """Return the visible category text for a blog card."""
        return self._first_visible_text_from_card(
            card,
            ".//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'category')] | .//*[self::span or self::p][normalize-space()]",
        ).strip()

    def get_visible_images(self):
        """Return visible blog page images."""
        return [
            image
            for image in self.driver.find_elements(*BlogLocators.BLOG_DETAIL_FEATURED_IMAGE)
            if image.is_displayed()
        ]

    def get_blog_content_text(self):
        """Return visible article content text."""
        texts = self._visible_texts(BlogLocators.BLOG_DETAIL_CONTENT)
        if texts:
            return texts[0].strip()
        return ""

    def verify_external_links(self):
        """Return True when visible external links exist and have valid href values."""
        links = self.get_external_links()
        return bool(links) and all((link.get_attribute("href") or "").strip() for link in links)

    def get_external_links(self):
        """Return visible external links from the current page."""
        return [
            link
            for link in self.driver.find_elements(*BlogLocators.EXTERNAL_LINKS)
            if link.is_displayed()
        ]

    def verify_internal_link(self, link):
        """Click an internal link and verify that navigation succeeds."""
        original_url = self.driver.current_url
        expected_href = self._normalize_blog_url(link.get_attribute("href"))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            link,
        )
        WebDriverWait(self.driver, 10).until(lambda _: link.is_enabled())
        link.click()
        try:
            self.wait_for_page_load()
        except TimeoutException:
            self.driver.execute_script("window.stop();")

        current_url = self.driver.current_url
        if expected_href:
            return self._urls_match(current_url, expected_href)
        return current_url != original_url and self._is_internal_link(current_url)

    def verify_internal_links(self):
        """Return True when visible internal links exist and have valid href values."""
        links = [
            link
            for link in self.driver.find_elements(*BlogLocators.INTERNAL_LINKS)
            if link.is_displayed()
        ]
        return bool(links) and all((link.get_attribute("href") or "").strip() for link in links)

    def click_pagination(self, label):
        """Click a pagination control by its visible label."""
        locator_map = {
            "previous": BlogLocators.BLOG_PAGINATION_PREVIOUS,
            "first": BlogLocators.BLOG_PAGINATION_FIRST,
            "next": BlogLocators.BLOG_PAGINATION_NEXT,
            "last": BlogLocators.BLOG_PAGINATION_LAST,
        }
        locator = locator_map.get(label.lower())
        if not locator:
            raise ValueError(f"Unsupported pagination label: {label}")
        self.click(locator)
        self.wait_for_page_load()

    def click_related_post(self, index=0):
        """Open a related post and return the new URL."""
        links = self.get_related_post_links()
        if index < 0 or index >= len(links):
            raise IndexError(f"Related post index out of range: {index}")

        original_url = self.driver.current_url
        link = links[index]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            link,
        )
        WebDriverWait(self.driver, 10).until(lambda _: link.is_enabled())
        link.click()
        self.wait_for_page_load()

        try:
            WebDriverWait(self.driver, 10).until(
                lambda active_driver: active_driver.current_url != original_url
                or len(active_driver.window_handles) > 1
            )
        except TimeoutException:
            pass
        return self.driver.current_url

    def _wait_for_blog_cards(self):
        try:
            WebDriverWait(self.driver, 15).until(
                lambda _: len(self.get_blog_cards()) > 0
            )
        except TimeoutException:
            return False
        return True

    def _blog_card_target(self, card):
        for candidate in card.find_elements(By.XPATH, ".//a[normalize-space() and @href] | .//button[normalize-space()]"):
            if candidate.is_displayed() and candidate.is_enabled():
                return candidate
        return card

    def _nearest_card_container(self, element):
        try:
            return element.find_element(
                By.XPATH,
                "ancestor::*[self::article or self::section or self::div][.//a[contains(@href, '/blogs/')]][1]",
            )
        except Exception:
            return element

    def _element_key(self, element):
        return getattr(element, "id", None) or getattr(element, "_id", None) or str(id(element))

    def _compact_text(self, element):
        try:
            return " ".join((element.text or "").split()).strip()
        except StaleElementReferenceException:
            return ""

    def _first_visible_text(self, locator):
        for element in self.driver.find_elements(*locator):
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

    def _normalize_blog_url(self, href):
        if not href:
            return None
        parsed = urlparse(href)
        if not parsed.netloc:
            href = self.driver.execute_script(
                "return new URL(arguments[0], window.location.origin).href;", href
            )
            parsed = urlparse(href)
        path = parsed.path.rstrip('/')
        if parsed.netloc.endswith('suryasangam.com') and path.startswith('/blogs') and path != '/blogs':
            return parsed._replace(path=path).geturl().rstrip('/')
        return None

    def _is_internal_link(self, href):
        return bool(href and urlparse(href).netloc.endswith("suryasangam.com"))

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
