"""Page object for efficient Phase 7 Person 2 Blog validation."""

from urllib.parse import urljoin, urlparse, urldefrag

from selenium.common.exceptions import TimeoutException

from locators.blogs_person2_locators import BlogsPerson2Locators
from pages.base_page import BasePage


class BlogsPerson2Page(BasePage):
    """Discovers Blog URLs once and supports one-pass article checks."""

    BASE_URL = "https://www.suryasangam.com/"
    LISTING_URL = urljoin(BASE_URL, "blogs")
    BLOG_PATH_PREFIX = "/blogs/"
    ERROR_MARKERS = ("blog not found", "network error", "404", "internal server error")

    def open_listing(self):
        try:
            self.driver.get(self.LISTING_URL)
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        self.wait_for_page_load()

    def discover_blog_urls(self):
        """Return unique same-site article URLs from the listing DOM."""
        urls = []
        for link in self.driver.find_elements(*BlogsPerson2Locators.BLOG_LINKS):
            href = link.get_attribute("href")
            normalized = self._normalize_blog_url(href)
            if normalized and normalized not in urls:
                urls.append(normalized)
        return urls

    def open_blog(self, url):
        try:
            self.driver.get(url)
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        self.wait_for_page_load()

    def page_is_valid_blog(self, expected_url):
        current = urlparse(self.driver.current_url)
        body = self.driver.find_element("tag name", "body").text.lower()
        return (
            current.netloc.endswith("suryasangam.com")
            and current.path.startswith(self.BLOG_PATH_PREFIX)
            and not any(marker in body for marker in self.ERROR_MARKERS)
            and bool(self.driver.find_elements(*BlogsPerson2Locators.BLOG_HEADING))
            and urlparse(expected_url).path == current.path
        )

    def image_findings(self):
        """Return unique broken image URLs, checking browser load state."""
        findings = []
        for image in self.driver.find_elements(*BlogsPerson2Locators.CONTENT_IMAGES):
            src = image.get_attribute("currentSrc") or image.get_attribute("src") or "<missing src>"
            loaded = self.driver.execute_script(
                "return arguments[0].complete && arguments[0].naturalWidth > 0;", image
            )
            if not loaded and src not in findings:
                findings.append(src)
        return findings

    def share_controls(self):
        return [
            control
            for control in self.driver.find_elements(*BlogsPerson2Locators.SHARE_CONTROLS)
            if control.is_displayed()
        ]

    def related_links(self):
        headings = self.driver.find_elements(*BlogsPerson2Locators.RELATED_HEADING)
        links = []
        for heading in headings:
            section = heading.find_element("xpath", "ancestor::*[self::section or self::div][1]")
            for link in section.find_elements("css selector", "a[href]"):
                normalized = self._normalize_blog_url(link.get_attribute("href"))
                if normalized and normalized not in links:
                    links.append(normalized)
        return links

    def content_links(self):
        links = []
        for link in self.driver.find_elements(*BlogsPerson2Locators.CONTENT_LINKS):
            href = link.get_attribute("href")
            if href and href not in links:
                links.append(href)
        return links

    def share_destination_is_valid(self, control, blog_url):
        href = control.get_attribute("href")
        if href:
            parsed = urlparse(href)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                return False
            return any(token in href.lower() for token in ("share", "sharer", "intent", "send", "t.me"))
        return control.tag_name.lower() == "button" and control.is_enabled()

    def _normalize_blog_url(self, href):
        if not href:
            return None
        absolute = urldefrag(urljoin(self.BASE_URL, href))[0].rstrip("/")
        parsed = urlparse(absolute)
        if parsed.netloc.endswith("suryasangam.com") and parsed.path.startswith(self.BLOG_PATH_PREFIX):
            return absolute
        return None
