"""Locators for the Surya Sangam homepage."""

from selenium.webdriver.common.by import By


class HomeLocators:
    """Centralized homepage locators."""

    HERO_SECTION = (
        By.XPATH,
        "//h1[contains(normalize-space(), 'A Marketplace for Transparent')]/ancestor::section[1]",
    )
    HERO_SUBTITLE = (
        By.XPATH,
        "//h2[contains(normalize-space(), \"Powering India's Solar Revolution\")]",
    )
    HERO_HEADING = (
        By.XPATH,
        "//h1[contains(normalize-space(), 'A Marketplace for Transparent')]",
    )
    HERO_DESCRIPTION = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Join thousands of homeowners and businesses')]",
    )
    HERO_GET_STARTED_BUTTON = (
        By.XPATH,
        "//a[normalize-space()='Get Started'] | //button[normalize-space()='Get Started']",
    )
    HERO_IMAGE = (
        By.XPATH,
        "//img[contains(@alt, 'Solar panels installation professional')]",
    )
    SOLAR_CALC_SECTION = (
        By.XPATH,
        "//h1[normalize-space()='Rooftop Solar Estimator']/ancestor::section[1]",
    )
    ADVANCED_QUOTE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Get Advanced Quote'] | //a[normalize-space()='Get Advanced Quote']",
    )
    SELECT_SYSTEM_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(), 'Select this System')] | "
        "//a[contains(normalize-space(), 'Select this System')]",
    )
    BECOME_PARTNER_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Become a Partner'] | //a[normalize-space()='Become a Partner']",
    )
    CTA_BUTTONS = (
        By.XPATH,
        "//a[normalize-space()='Get Started' or normalize-space()='Become a Partner' "
        "or contains(normalize-space(), 'Select this System')] | "
        "//button[normalize-space()='Get Started' or normalize-space()='Become a Partner' "
        "or normalize-space()='Get Advanced Quote' or contains(normalize-space(), 'Select this System')]",
    )
    ALL_IMAGES = (By.TAG_NAME, "img")
    FOOTER = (By.TAG_NAME, "footer")
    FOOTER_LINKS = (By.CSS_SELECTOR, "footer a")
