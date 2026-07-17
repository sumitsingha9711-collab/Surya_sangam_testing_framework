"""Centralized locators for the Surya Sangam services module."""

from selenium.webdriver.common.by import By


class ServicesLocators:
    """Locators for the services hub and service detail pages."""

    MAIN_CONTENT = (By.TAG_NAME, "main")
    SERVICES_HEADING = (
        By.XPATH,
        "//main//h1[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'discover the best solar') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'services') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'offerings')]",
    )
    SERVICES_SUBHEADING = (
        By.XPATH,
        "//main//h2[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'filters') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'top-rated') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'popular products')]",
    )
    HERO_BANNER = (
        By.XPATH,
        "//main//img[contains(translate(@alt, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'solar')]",
    )
    SERVICE_GRID = (
        By.XPATH,
        "//main//*[self::section or self::div][.//h1 or .//h2 or .//h3 or .//h4]",
    )
    SERVICE_CARD_CONTAINERS = (
        By.XPATH,
        "//main//*[self::article or self::section or self::li or self::div][.//img and (.//a or .//button or @role='button')]",
    )
    SERVICE_CARD_TITLES = (
        By.XPATH,
        "//main//*[self::h2 or self::h3 or self::h4 or self::h5][normalize-space() and (contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'kw') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'solar system') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ongrid') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'offgrid') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'dcr'))]",
    )
    SERVICE_CARD_DESCRIPTION = (
        By.XPATH,
        ".//p[normalize-space()] | .//*[self::span or self::div][normalize-space() and not(self::button) and not(self::a)]",
    )
    SERVICE_CARD_IMAGE = (By.XPATH, ".//img")
    SERVICE_CARD_CTA_BUTTONS = (
        By.XPATH,
        ".//a[normalize-space() and @href] | .//button[normalize-space()] | .//*[@role='button'][normalize-space()]",
    )
    SERVICE_DETAIL_ROOT = (By.XPATH, "//main")
    SERVICE_DETAIL_HEADING = (
        By.XPATH,
        "//main//*[self::h1 or self::h2][normalize-space()]",
    )
    SERVICE_DETAIL_HERO_SECTION = (
        By.XPATH,
        "//main//*[self::section or self::div][.//*[self::h1 or self::h2][normalize-space()]][1]",
    )
    SERVICE_DETAIL_DESCRIPTION = (By.XPATH, "//main//p[normalize-space()]")
    SERVICE_DETAIL_FEATURE_LIST = (By.XPATH, "//main//ul[li] | //main//ol[li]")
    SERVICE_DETAIL_STATISTICS = (
        By.XPATH,
        "//main//*[contains(normalize-space(), '%') or contains(normalize-space(), '+') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'years') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'projects') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'clients')]",
    )
    SERVICE_DETAIL_CTA_SECTION = (
        By.XPATH,
        "//main//*[self::section or self::div][.//a[normalize-space() and @href] or .//button[normalize-space()]]",
    )
    SERVICE_DETAIL_IMAGES = (By.XPATH, "//main//img")
    SERVICE_DETAIL_ICONS = (
        By.XPATH,
        "//main//*[self::svg or self::i or @role='img' or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'icon')]",
    )
    SERVICE_INTERNAL_LINKS = (
        By.XPATH,
        "//a[@href and normalize-space() and not(starts-with(@href, 'mailto:')) and not(starts-with(@href, 'tel:')) and not(ancestor::header)]",
    )
    BREADCRUMB = (
        By.XPATH,
        "//nav[contains(@aria-label, 'breadcrumb') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'breadcrumb')] | //*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'breadcrumb')]",
    )
    FOOTER = (By.TAG_NAME, "footer")
