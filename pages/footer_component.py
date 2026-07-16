from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.footer_component_locators import FooterComponentLocators


class FooterComponent:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))

    def get_root(self):
        try:
            return self._wait(FooterComponentLocators.FOOTER)
        except Exception:
            return self._wait(FooterComponentLocators.FALLBACK_FOOTER)

    def is_visible(self) -> bool:
        root = self.get_root()
        return root.is_displayed()

    def get_text(self) -> str:
        return self.get_root().text.strip()

    def get_section_headings(self) -> list[str]:
        text = self.get_text()
        return [heading for heading in FooterComponentLocators.SECTION_HEADINGS if heading in text]

    def get_footer_links(self):
        root = self.get_root()
        return root.find_elements(By.TAG_NAME, "a")

    def get_visible_footer_links(self):
        return [link for link in self.get_footer_links() if link.is_displayed()]

    def click_footer_link(self, link_text: str):
        root = self.get_root()
        link = root.find_element(By.XPATH, f".//a[contains(normalize-space(.), '{link_text}')]")
        link.click()
        return link

    def get_contact_information(self) -> str:
        text = self.get_text()
        return "\n".join(
            line for line in text.splitlines() if "@" in line or "+91" in line or "Ghaziabad" in line
        )

    def get_copyright_text(self) -> str:
        text = self.get_text()
        for line in text.splitlines():
            if "All Rights Reserved" in line or line.strip().startswith("©"):
                return line.strip()
        return ""

    def get_social_media_links(self):
        root = self.get_root()
        anchors = root.find_elements(By.TAG_NAME, "a")
        social_links = []
        for anchor in anchors:
            href = (anchor.get_attribute("href") or "").lower()
            if any(domain in href for domain in FooterComponentLocators.SOCIAL_MEDIA_DOMAINS):
                social_links.append(anchor)
        return social_links

    def get_visible_social_media_links(self):
        return [link for link in self.get_social_media_links() if link.is_displayed()]

    def get_link_href(self, link):
        try:
            return link.get_attribute("href") or ""
        except StaleElementReferenceException:
            return ""

    def find_link_by_text(self, link_text: str):
        try:
            return self.get_root().find_element(By.XPATH, f".//a[contains(normalize-space(.), '{link_text}')]")
        except NoSuchElementException:
            return None
