"""Locators for the Surya Sangam site header."""

from selenium.webdriver.common.by import By


class HeaderLocators:
    """Centralized header locators."""

    LOGO = (
        By.XPATH,
        "//header//img[contains(translate(@alt, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'surya')]",
    )
    LOGO_LINK = (
        By.XPATH,
        "//header//a[.//img[contains(translate(@alt, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'surya')]]",
    )
    NAVIGATION = (By.CSS_SELECTOR, "header nav")
    NAVIGATION_LINKS = (By.CSS_SELECTOR, "header nav a")
    MENU_TOGGLE = (
        By.XPATH,
        "//button[contains(., 'Toggle menu') or @aria-label='Toggle menu']",
    )
    HOME_LINK = (By.XPATH, "//header//a[normalize-space()='Home']")
    STORE_LINK = (By.XPATH, "//header//a[normalize-space()='Store']")
    SMART_HUB_LINK = (By.XPATH, "//header//a[normalize-space()='Surya SmartHub']")
    ABOUT_US_LINK = (By.XPATH, "//header//a[normalize-space()='About Us']")
    CONTACT_US_LINK = (By.XPATH, "//header//a[normalize-space()='Contact Us']")
