from __future__ import annotations

from selenium.webdriver.common.by import By


class AboutInformationPageLocators:
    PAGE_HEADING = (By.XPATH, "//h1[contains(normalize-space(.), 'Welcome to Surya Sangam')]")
    PRIMARY_HEADING = (By.XPATH, "//h1[contains(normalize-space(.), 'Power Your Rooftop with Purpose')]")
    ABOUT_LINK = (By.XPATH, "//a[contains(normalize-space(.), 'About Us')]")
    CTA_BUTTONS = (
        By.XPATH,
        "//a[contains(normalize-space(.), 'Try Surya Calc Now')] | //button[contains(normalize-space(.), 'Try Surya Calc Now')]",
    )
    FOOTER_LINKS = (By.XPATH, "//footer//a")
