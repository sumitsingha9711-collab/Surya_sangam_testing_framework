from __future__ import annotations

from selenium.webdriver.common.by import By


class FooterComponentLocators:
    FOOTER = (By.TAG_NAME, "footer")
    FALLBACK_FOOTER = (
        By.XPATH,
        "//*[self::footer or (self::div or self::section)"
        " and .//*[contains(normalize-space(.), 'Follow Us')]"
        " and .//*[contains(normalize-space(.), 'Contact Us')]]",
    )
    SECTION_HEADINGS = (
        "Follow Us",
        "Our Offerings",
        "Resources",
        "About Us",
        "Help",
        "Contact Us",
        "Registered Office",
    )
    SOCIAL_MEDIA_DOMAINS = ("linkedin.com", "instagram.com", "x.com", "twitter.com")
