from __future__ import annotations

from selenium.webdriver.common.by import By


class ContactFormComponentLocators:
    PAGE_HEADING = (By.XPATH, "//h1[contains(normalize-space(.), 'Get In Touch')]")
    FORM = (By.XPATH, "//form[.//button[contains(normalize-space(.), 'Send Message')]]")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Send Message')]")
    SUCCESS_MESSAGE = (
        By.XPATH,
        "//*[contains(@class, 'success') or contains(@class, 'alert-success') or "
        "contains(normalize-space(.), 'Thank you') or contains(normalize-space(.), 'successfully')]",
    )
    ERROR_MESSAGE = (
        By.XPATH,
        "//*[contains(@class, 'error') or contains(@class, 'invalid') or contains(@role, 'alert')]",
    )
    FIELD_LABELS = {
        "name": "Name",
        "email": "Email",
        "phone": "Phone Number",
        "bill": "Avg. Electricity Bill",
        "address": "Address",
        "message": "Message",
    }
