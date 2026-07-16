"""Locators for the Surya Sangam About page."""

from selenium.webdriver.common.by import By


class AboutLocators:
    """Centralized About page locators."""

    HERO_SECTION = (
        By.XPATH,
        "//*[self::h1 or self::h2][contains(normalize-space(), 'Rooftop') "
        "or contains(normalize-space(), 'Surya Sangam')]/ancestor::section[1]",
    )
    MAIN_HEADING = (
        By.XPATH,
        "//h1[contains(normalize-space(), 'Power Your Rooftop') or "
        "contains(normalize-space(), 'Welcome to Surya Sangam')]",
    )
    COMPANY_DESCRIPTION = (
        By.XPATH,
        "//p[contains(normalize-space(), 'Smart, Transparent') "
        "or contains(normalize-space(), 'Personalized Solar Solutions')]",
    )
    ABOUT_IMAGES = (
        By.XPATH,
        "//img[not(ancestor::header) and not(ancestor::footer)] | "
        "//*[self::section or self::div][contains(@class, 'about-bg') "
        "or contains(@class, '/images/')]",
    )
    CTA_BUTTONS = (
        By.XPATH,
        "//a[normalize-space() and not(ancestor::header) and not(ancestor::footer) "
        "and (contains(@href, '/') or starts-with(@href, 'http'))] | "
        "//button[normalize-space() and not(ancestor::header) and not(ancestor::footer)]",
    )
    BREADCRUMB = (
        By.XPATH,
        "//nav[contains(@aria-label, 'breadcrumb') or contains(@class, 'breadcrumb')] | "
        "//*[contains(@class, 'breadcrumb')]",
    )
    NAVIGATION_LINKS = (
        By.XPATH,
        "//a[@href and normalize-space() and not(ancestor::header) "
        "and not(ancestor::footer) and not(starts-with(@href, 'mailto:')) "
        "and not(starts-with(@href, 'tel:'))]",
    )
    STATISTICS_SECTION = (
        By.XPATH,
        "//*[contains("
        "translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
        "'mw') or contains("
        "translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
        "'customer') or contains("
        "translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
        "'partner') or contains(normalize-space(), '+')]/ancestor::section[1]",
    )
