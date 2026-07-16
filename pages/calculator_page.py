"""Page object for the Surya Sangam solar calculator section."""

from urllib.parse import urlparse

from selenium.common.exceptions import (
    NoAlertPresentException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from locators.calculator_locators import CalculatorLocators
from pages.base_page import BasePage


class CalculatorPage(BasePage):
    """Solar calculator interactions and assertions."""

    URL = "https://www.suryasangam.com/#surya-calculator"
    EXPECTED_TITLE_TEXT = "Surya Sangam"
    EXPECTED_HASH = "surya-calculator"

    def open_calculator_page(self):
        """Open the homepage directly at the solar calculator section."""
        try:
            self.driver.get(self.URL)
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        self.wait_for_page_load()
        self.scroll_to_element(CalculatorLocators.CALCULATOR_HEADING)

    def verify_page_loaded(self):
        """Return True when the calculator section is visible."""
        return self.verify_current_url() and self.verify_calculator_heading()

    def verify_current_url(self):
        """Return True when the browser is on the calculator anchor."""
        current = urlparse(self.driver.current_url)
        return (
            current.netloc.endswith("suryasangam.com")
            and current.fragment == self.EXPECTED_HASH
        )

    def verify_page_title(self):
        """Return True when the browser title contains the expected site text."""
        return self.EXPECTED_TITLE_TEXT in self.driver.title

    def verify_calculator_heading(self):
        """Return True when the calculator heading is visible."""
        return self.is_visible(CalculatorLocators.CALCULATOR_HEADING)

    def enter_location(self, location):
        """Enter an address and select an autocomplete suggestion when present."""
        self._set_input_value(CalculatorLocators.LOCATION_INPUT, location)
        self.select_location_suggestion()

    def select_location_suggestion(self):
        """Select the first visible address suggestion, if the site provides one."""
        try:
            suggestion = WebDriverWait(self.driver, 4).until(
                lambda active_driver: next(
                    (
                        item
                        for item in active_driver.find_elements(
                            *CalculatorLocators.LOCATION_SUGGESTIONS
                        )
                        if item.is_displayed() and item.is_enabled()
                    ),
                    False,
                )
            )
            if suggestion:
                suggestion.click()
                return True
        except (TimeoutException, WebDriverException):
            pass

        # Autocomplete can render outside the calculator section or miss the
        # visibility wait. Keyboard selection commits the first suggestion.
        try:
            field = self.wait_for_visibility(CalculatorLocators.LOCATION_INPUT, timeout=3)
            field.send_keys(Keys.ARROW_DOWN, Keys.ENTER)
            return True
        except WebDriverException:
            return False

    def enter_monthly_bill(self, amount):
        """Enter the average monthly bill value."""
        self._set_input_value(CalculatorLocators.MONTHLY_BILL_INPUT, amount)

    def enter_average_units(self, units):
        """Enter the average monthly unit consumption value."""
        self._set_input_value(CalculatorLocators.AVERAGE_UNITS_INPUT, units)

    def select_property_type(self, option_text=None):
        """Select property type when the field is available."""
        return self._select_dropdown_option(0, option_text)

    def select_roof_type(self, option_text=None):
        """Select roof type when the field is available."""
        return self._select_dropdown_option(1, option_text)

    def select_any_other_required_inputs(self):
        """Select the first unchecked radio or checkbox when present."""
        for locator in (
            CalculatorLocators.RADIO_BUTTONS,
            CalculatorLocators.CHECKBOXES,
        ):
            for option in self.driver.find_elements(*locator):
                if option.is_displayed() and option.is_enabled() and not option.is_selected():
                    option.click()
                    return True
        return False

    def click_calculate(self):
        """Click calculate and retry once when address autocomplete is late."""
        self.click(CalculatorLocators.CALCULATE_BUTTON)
        validation = self._consume_alert_text()
        if validation and "enter an address" in validation.lower():
            if self.select_location_suggestion():
                self.click(CalculatorLocators.CALCULATE_BUTTON)
                return self._consume_alert_text()
        return validation

    def click_reset(self):
        """Click reset when available, otherwise clear all fields."""
        reset_buttons = self.driver.find_elements(*CalculatorLocators.RESET_BUTTON)
        visible_reset_buttons = [
            button for button in reset_buttons if button.is_displayed()
        ]
        if visible_reset_buttons:
            self.click(CalculatorLocators.RESET_BUTTON)
            return True

        self.clear_all_fields()
        return False

    def get_calculation_result(self):
        """Return visible calculator result text."""
        if not self.verify_result_displayed():
            return ""
        return self.get_text(CalculatorLocators.RESULT_SECTION).strip()

    def verify_result_displayed(self):
        """Return True when the estimator result cards are visible."""
        self.driver.execute_script(
            "window.scrollTo(0, Math.max(0, document.body.scrollHeight / 3));"
        )
        if not self.is_visible(CalculatorLocators.RESULT_SECTION, timeout=10):
            return False
        cards = [
            card
            for card in self.driver.find_elements(*CalculatorLocators.RESULT_CARDS)
            if card.is_displayed()
        ]
        return bool(cards)

    def verify_validation_message(self):
        """Return True when inline or alert validation is available."""
        return bool(self.get_validation_message())

    def get_validation_message(self):
        """Return alert or inline validation text."""
        alert_text = self._consume_alert_text()
        if alert_text:
            return alert_text

        # Browser-native validation covers required and number fields even
        # when the application does not render an inline error element.
        for field in self.get_input_fields():
            message = field.get_attribute("validationMessage")
            if message:
                return message.strip()

        messages = [
            element.text.strip()
            for element in self.driver.find_elements(*CalculatorLocators.VALIDATION_MESSAGES)
            if element.is_displayed() and element.text.strip()
        ]
        return messages[0] if messages else ""

    def clear_all_fields(self):
        """Clear all calculator input fields."""
        for field in self.get_input_fields():
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", field
            )
            field.clear()
            field.send_keys(Keys.CONTROL, "a")
            field.send_keys(Keys.BACKSPACE)
            self.driver.execute_script(
                "arguments[0].value = '';"
                "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));"
                "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
                field,
            )

        # The current page has no reset control, but keep optional controls
        # reusable if they are added to the calculator later.
        for locator in (CalculatorLocators.RADIO_BUTTONS, CalculatorLocators.CHECKBOXES):
            for option in self.driver.find_elements(*locator):
                if option.is_selected():
                    self.driver.execute_script(
                        "arguments[0].checked = false;"
                        "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
                        option,
                    )

    def get_location_value(self):
        """Return the location field value."""
        return self.wait_for_visibility(
            CalculatorLocators.LOCATION_INPUT
        ).get_attribute("value")

    def get_monthly_bill_value(self):
        """Return the average bill field value."""
        return self.wait_for_visibility(
            CalculatorLocators.MONTHLY_BILL_INPUT
        ).get_attribute("value")

    def get_average_units_value(self):
        """Return the average units field value."""
        return self.wait_for_visibility(
            CalculatorLocators.AVERAGE_UNITS_INPUT
        ).get_attribute("value")

    def get_input_fields(self):
        """Return all calculator input elements."""
        return [
            field
            for field in self.driver.find_elements(*CalculatorLocators.INPUT_FIELDS)
            if field.is_displayed()
        ]

    def get_interactive_buttons(self):
        """Return visible buttons in the calculator section."""
        return [
            button
            for button in self.driver.find_elements(
                *CalculatorLocators.INTERACTIVE_BUTTONS
            )
            if button.is_displayed()
        ]

    def fill_required_fields(self, location, units, monthly_bill):
        """Fill the current required calculator inputs."""
        self.enter_location(location)
        self.enter_average_units(units)
        self.enter_monthly_bill(monthly_bill)
        self.select_any_other_required_inputs()

    def has_unexpected_error(self):
        """Return True when an unexpected visible error appears."""
        error_terms = ("error", "invalid", "failed")
        for element in self.driver.find_elements(*CalculatorLocators.ERROR_MESSAGES):
            text = element.text.strip().lower()
            if element.is_displayed() and any(term in text for term in error_terms):
                return True
        return False

    def _set_input_value(self, locator, value):
        field = self.wait_for_visibility(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            field,
        )
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.BACKSPACE)
        field.send_keys(str(value))
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));",
            field,
        )

    def _select_dropdown_option(self, index, option_text=None):
        dropdowns = [
            dropdown
            for dropdown in self.driver.find_elements(*CalculatorLocators.DROPDOWNS)
            if dropdown.is_displayed() and dropdown.is_enabled()
        ]
        if index >= len(dropdowns):
            return False

        select = Select(dropdowns[index])
        if option_text:
            select.select_by_visible_text(option_text)
        elif len(select.options) > 1:
            select.select_by_index(1)
        return True

    def _consume_alert_text(self):
        try:
            alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            return text
        except (NoAlertPresentException, TimeoutException):
            return ""
