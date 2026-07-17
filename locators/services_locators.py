"""Centralized locators for the Surya Sangam services module."""

from selenium.webdriver.common.by import By


class ServicesLocators:
    """Locators for the services hub and service detail pages."""

    SERVICES_HEADING = (
        By.XPATH,
        "//h1[contains(normalize-space(.), 'DISCOVER the Best Solar') or contains(normalize-space(.), 'Home or Business')]",
    )
    HERO_BANNER = (
        By.XPATH,
        "//img[contains(translate(@alt, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'solar components') or contains(translate(@alt, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'solar')]",
    )
    SERVICE_CARD_LINKS = (
        By.XPATH,
        "//a[contains(@href, '/productlistning/') and not(contains(@href, '?page='))]",
    )
    SERVICE_CARD_IMAGES = (By.XPATH, ".//img")
    SERVICE_CARD_TITLES = (
        By.XPATH,
        ".//*[self::span or self::div or self::h2 or self::h3][normalize-space()]",
    )
    SERVICE_CARD_TEXT = (
        By.XPATH,
        ".//*[normalize-space() and not(self::img) and not(self::svg)]",
    )
    SERVICE_DETAIL_IMAGES = (By.XPATH, "//img")
    SERVICE_DETAIL_BUTTONS = (
        By.XPATH,
        "//button[normalize-space()] | //a[normalize-space() and @href]",
    )
    SERVICE_DETAIL_LINKS = (
        By.XPATH,
        "//a[@href and not(starts-with(@href, 'mailto:')) and not(starts-with(@href, 'tel:'))]",
    )
    BREADCRUMB = (
        By.XPATH,
        "//nav[contains(@aria-label, 'breadcrumb') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'breadcrumb')] | //*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'breadcrumb')]",
    )
    FOOTER = (By.TAG_NAME, "footer")
