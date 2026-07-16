from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.about_information_page_locators import AboutInformationPageLocators


class AboutInformationPage:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))

    def open_from_homepage(self, base_url: str):
        self.driver.get(base_url)
        self._wait(AboutInformationPageLocators.ABOUT_LINK).click()

    def wait_for_loaded(self):
        self._wait(AboutInformationPageLocators.PRIMARY_HEADING)
        return self

    def is_loaded(self) -> bool:
        try:
            return self.wait_for_loaded().get_primary_heading().is_displayed()
        except TimeoutException:
            return False

    def get_primary_heading(self):
        return self._wait(AboutInformationPageLocators.PRIMARY_HEADING)

    def get_page_heading(self):
        return self._wait(AboutInformationPageLocators.PAGE_HEADING)

    def get_visible_text(self) -> str:
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_images(self):
        return self.driver.find_elements(By.TAG_NAME, "img")

    def get_cta_buttons(self):
        return self.driver.find_elements(*AboutInformationPageLocators.CTA_BUTTONS)

    def get_internal_links(self):
        anchors = self.driver.find_elements(By.TAG_NAME, "a")
        return [
            anchor
            for anchor in anchors
            if (anchor.get_attribute("href") or "").startswith(self.driver.current_url.split("/aboutus")[0])
        ]

    def go_back(self):
        self.driver.back()

    def get_footer_links(self):
        return self.driver.find_elements(*AboutInformationPageLocators.FOOTER_LINKS)

    def has_expected_content(self) -> bool:
        text = self.get_visible_text()
        expected_phrases = [
            "Who are we?",
            "Our Mission",
            "What We Offer",
            "Why Choose Surya Sangam?",
            "Our Commitment",
            "Start Your Solar Journey with Surya Sangam",
        ]
        return any(phrase in text for phrase in expected_phrases)

    def has_non_empty_text(self) -> bool:
        return bool(self.get_visible_text().strip())

    def image_sources(self) -> list[str]:
        return [(image.get_attribute("src") or "").strip() for image in self.get_images()]

    def broken_images(self) -> list[str]:
        broken = []
        for image in self.get_images():
            src = (image.get_attribute("src") or "").strip()
            if not src:
                broken.append("<empty src>")
                continue
            loaded = self.driver.execute_script(
                "return arguments[0].complete && arguments[0].naturalWidth > 0;",
                image,
            )
            if not loaded:
                broken.append(src)
        return broken
