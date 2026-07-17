"""Locators for the Surya Sangam Contact page."""

from selenium.webdriver.common.by import By


class ContactLocators:
    """Centralized Contact page locators."""

    PAGE_HEADING = (By.XPATH, "//h1[contains(normalize-space(.), 'Get In Touch')]")
    CONTACT_FORM = (By.XPATH, "//form[.//button[@type='submit']]")
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "email")
    PHONE_INPUT = (By.ID, "phone")
    BILL_INPUT = (By.ID, "avgElectricityBill")
    ADDRESS_INPUT = (By.ID, "address")
    MESSAGE_INPUT = (By.ID, "message")
    INPUT_FIELDS = (
        By.XPATH,
        "//form[.//button[@type='submit']]//input | "
        "//form[.//button[@type='submit']]//textarea",
    )
    SUBMIT_BUTTON = (By.XPATH, "//form//button[@type='submit']")
    RESET_BUTTON = (By.XPATH, "//form//button[@type='reset']")
    VALIDATION_MESSAGES = (
        By.XPATH,
        "//form//*[contains(@role, 'alert') or "
        "contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'error') or "
        "contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'invalid')]",
    )
    SUCCESS_MESSAGE = (
        By.XPATH,
        "//*[contains(@role, 'status') or "
        "contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'success') or "
        "contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'thank you') or "
        "contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'successfully')]",
    )
    CONTACT_EMAIL = (By.CSS_SELECTOR, "a[href^='mailto:']")
    CONTACT_PHONE = (By.CSS_SELECTOR, "a[href^='tel:']")
    CONTACT_ADDRESS = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'Aditya World City') or "
        "contains(normalize-space(.), 'Ghaziabad')]",
    )
    GOOGLE_MAP = (
        By.XPATH,
        "//iframe[contains(translate(@src, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'google') and "
        "not(contains(@src, 'googletagmanager'))] | "
        "//*[@aria-label='Google Map' or contains(@class, 'map')]",
    )
    CONTACT_CTA_BUTTONS = (
        By.XPATH,
        "//a[contains(@href, '/contactus')] | "
        "//button[contains(normalize-space(.), 'Contact')]",
    )