"""Page object for the Surya Sangam Contact page."""

from urllib.parse import urlparse

from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.contact_locators import ContactLocators
from pages.base_page import BasePage


class ContactPage(BasePage):
    """Contact page interactions and validation helpers."""

    URL = "https://www.suryasangam.com/contactus"
    EXPECTED_TITLE_TEXT = "Surya Sangam"

    def open_contact_page(self):
        """Open the Contact page and wait for its heading."""
        try:
            self.driver.get(self.URL)
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        self.wait_for_page_load()
        self.wait_for_visibility(ContactLocators.PAGE_HEADING)

    def verify_page_loaded(self):
        """Return True when the Contact page heading and form are visible."""
        return (
            self.verify_current_url()
            and self.is_visible(ContactLocators.PAGE_HEADING)
            and self.is_visible(ContactLocators.CONTACT_FORM)
        )

    def verify_page_title(self):
        """Return True when the page title contains the site name."""
        return self.EXPECTED_TITLE_TEXT in self.driver.title

    def verify_current_url(self):
        """Return True when the browser is on the Contact page."""
        current = urlparse(self.driver.current_url)
        expected = urlparse(self.URL)
        return (
            current.netloc.endswith("suryasangam.com")
            and current.path.rstrip("/") == expected.path
        )

    def enter_name(self, value):
        """Enter the contact name."""
        self._set_field(ContactLocators.NAME_INPUT, value)

    def enter_email(self, value):
        """Enter the contact email."""
        self._set_field(ContactLocators.EMAIL_INPUT, value)

    def enter_phone(self, value):
        """Enter the contact phone number."""
        self._set_field(ContactLocators.PHONE_INPUT, value)

    def enter_message(self, value):
        """Enter the contact message."""
        self._set_field(ContactLocators.MESSAGE_INPUT, value)

    def enter_bill(self, value):
        """Enter the required average electricity bill."""
        self._set_field(ContactLocators.BILL_INPUT, value)

    def enter_address(self, value):
        """Enter the required contact address."""
        self._set_field(ContactLocators.ADDRESS_INPUT, value)

    def fill_required_fields(self, name, email, phone, bill, address, message):
        """Fill all fields required by the current Contact form."""
        self.enter_name(name)
        self.enter_email(email)
        self.enter_phone(phone)
        self.enter_bill(bill)
        self.enter_address(address)
        self.enter_message(message)

    def submit_form(self):
        """Submit the form and return any browser alert text."""
        self.click(ContactLocators.SUBMIT_BUTTON)
        return self._consume_alert_text()

    def clear_form(self):
        """Clear every visible Contact form field."""
        for field in self.driver.find_elements(*ContactLocators.INPUT_FIELDS):
            if field.is_displayed() and field.is_enabled():
                field.clear()

        reset_buttons = [
            button
            for button in self.driver.find_elements(*ContactLocators.RESET_BUTTON)
            if button.is_displayed() and button.is_enabled()
        ]
        if reset_buttons:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(reset_buttons[0])
            ).click()

    def verify_success_message(self):
        """Return True when a success/status message is visible."""
        return self.is_visible(ContactLocators.SUCCESS_MESSAGE, timeout=5)

    def verify_validation_message(self):
        """Return True for native, inline, or alert validation."""
        if self._consume_alert_text():
            return True

        for field in self.get_form_fields():
            if field.get_attribute("validationMessage"):
                return True

        return any(
            element.is_displayed() and element.text.strip()
            for element in self.driver.find_elements(
                *ContactLocators.VALIDATION_MESSAGES
            )
        )

    def get_form_fields(self):
        """Return visible Contact form fields."""
        return [
            field
            for field in self.driver.find_elements(*ContactLocators.INPUT_FIELDS)
            if field.is_displayed()
        ]

    def get_contact_email(self):
        """Return the displayed contact email, if present."""
        return self.get_text(ContactLocators.CONTACT_EMAIL)

    def get_contact_phone(self):
        """Return the displayed contact phone, if present."""
        return self.get_text(ContactLocators.CONTACT_PHONE)

    def get_contact_address(self):
        """Return displayed address text, if present."""
        return self.get_text(ContactLocators.CONTACT_ADDRESS)

    def is_google_map_present(self):
        """Return whether a visible map element is present."""
        return self.is_visible(ContactLocators.GOOGLE_MAP, timeout=5)

    def get_contact_ctas(self):
        """Return visible Contact-related CTA elements."""
        return [
            cta
            for cta in self.driver.find_elements(*ContactLocators.CONTACT_CTA_BUTTONS)
            if cta.is_displayed()
        ]

    def _set_field(self, locator, value):
        field = self.wait_for_visibility(locator)
        field.clear()
        field.send_keys(str(value))

    def _consume_alert_text(self):
        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            text = alert.text.strip()
            alert.accept()
            return text
        except (NoAlertPresentException, TimeoutException):
            return ""