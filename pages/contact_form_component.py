from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.contact_form_component_locators import ContactFormComponentLocators


class ContactFormComponent:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))

    def get_page_heading(self):
        return self._wait(ContactFormComponentLocators.PAGE_HEADING)

    def get_form(self):
        return self._wait(ContactFormComponentLocators.FORM)

    def is_visible(self) -> bool:
        return self.get_form().is_displayed()

    def get_submit_button(self):
        return self._wait(ContactFormComponentLocators.SUBMIT_BUTTON)

    def _field_by_label_text(self, label_text: str):
        form = self.get_form()
        candidates = [
            f".//label[contains(normalize-space(.), '{label_text}')]/following::input[1]",
            f".//label[contains(normalize-space(.), '{label_text}')]/following::textarea[1]",
            f".//input[contains(@placeholder, '{label_text}')]",
            f".//textarea[contains(@placeholder, '{label_text}')]",
            f".//*[@aria-label='{label_text}']",
        ]
        for xpath in candidates:
            try:
                field = form.find_element(By.XPATH, xpath)
                if field.is_displayed():
                    return field
            except NoSuchElementException:
                continue
        raise NoSuchElementException(f"Field not found for label text: {label_text}")

    def get_required_fields(self):
        required_fields = {}
        for key, label in ContactFormComponentLocators.FIELD_LABELS.items():
            try:
                required_fields[key] = self._field_by_label_text(label)
            except NoSuchElementException:
                continue
        return required_fields

    def fill_form(
        self,
        *,
        name: str = "",
        email: str = "",
        phone: str = "",
        bill: str = "",
        address: str = "",
        message: str = "",
    ):
        values = {
            "name": name,
            "email": email,
            "phone": phone,
            "bill": bill,
            "address": address,
            "message": message,
        }
        for key, value in values.items():
            if not value:
                continue
            field = self._field_by_label_text(ContactFormComponentLocators.FIELD_LABELS[key])
            field.clear()
            field.send_keys(value)

    def submit(self):
        self.get_submit_button().click()

    def get_validation_errors(self) -> list[str]:
        errors = []
        try:
            error_elements = self.driver.find_elements(*ContactFormComponentLocators.ERROR_MESSAGE)
            errors.extend([element.text.strip() for element in error_elements if element.is_displayed() and element.text.strip()])
        except Exception:
            pass

        for key, field in self.get_required_fields().items():
            validity = self.driver.execute_script("return arguments[0].validationMessage || '';", field)
            if validity and validity not in errors:
                errors.append(validity)
        return errors

    def has_native_validation(self) -> bool:
        try:
            form = self.get_form()
            return not bool(self.driver.execute_script("return arguments[0].checkValidity();", form))
        except Exception:
            return False

    def success_message(self) -> str:
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(ContactFormComponentLocators.SUCCESS_MESSAGE)
            )
            return element.text.strip()
        except TimeoutException:
            return ""
