from __future__ import annotations

from collections.abc import Iterable

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.solar_calculator_feature_locators import (
    SolarCalculatorFeatureLocators,
)


class SolarCalculatorFeature:
    """Page object for the homepage Rooftop Solar Estimator."""

    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, condition):
        return WebDriverWait(self.driver, self.timeout).until(condition)

    def _find_first(self, locators: Iterable[tuple[str, str]]) -> WebElement:
        for locator in locators:
            elements = self.driver.find_elements(*locator)
            if elements:
                return elements[0]
        raise TimeoutException("Solar Calculator element was not found.")

    def open_calculator(self, base_url: str):
        self.driver.get(base_url)
        return self._wait(
            EC.visibility_of_element_located(
                SolarCalculatorFeatureLocators.CALCULATOR_HEADING
            )
        )

    def is_visible(self) -> bool:
        try:
            return self._wait(
                EC.visibility_of_element_located(
                    SolarCalculatorFeatureLocators.CALCULATOR_HEADING
                )
            ).is_displayed()
        except TimeoutException:
            return False

    def get_input_fields(self) -> list[WebElement]:
        container = self._wait(
            EC.presence_of_element_located(
                SolarCalculatorFeatureLocators.CALCULATOR_CONTAINER
            )
        )
        return container.find_elements(By.TAG_NAME, "input")

    def get_numeric_inputs(self) -> list[WebElement]:
        return [
            element
            for element in self.get_input_fields()
            if (element.get_attribute("type") or "").lower() in {"number", "", "text"}
            and element.get_attribute("placeholder") in {"e.g. 300", "e.g. 2500"}
        ]

    def get_average_units_input(self) -> WebElement:
        return self._wait(
            EC.presence_of_element_located(
                SolarCalculatorFeatureLocators.AVERAGE_UNITS_INPUT
            )
        )

    def get_average_bill_input(self) -> WebElement:
        return self._wait(
            EC.presence_of_element_located(
                SolarCalculatorFeatureLocators.AVERAGE_BILL_INPUT
            )
        )

    def enter_input(self, units: str | int | None = None, bill: str | int | None = None):
        fields = (
            (self.get_average_units_input(), units),
            (self.get_average_bill_input(), bill),
        )
        for element, value in fields:
            if value is not None:
                element.clear()
                element.send_keys(str(value))

    def clear_input(self):
        for element in self.get_numeric_inputs():
            element.clear()

    def click_calculate(self):
        button = self._wait(
            EC.element_to_be_clickable(
                SolarCalculatorFeatureLocators.CALCULATE_BUTTON
            )
        )
        button.click()

    def get_error_message(self) -> str:
        messages = self.driver.find_elements(
            *SolarCalculatorFeatureLocators.VALIDATION_MESSAGE
        )
        return " ".join(
            message.text.strip() for message in messages if message.is_displayed() and message.text.strip()
        )

    def is_error_message_visible(self) -> bool:
        return bool(self.get_error_message())

    def get_result(self) -> str:
        messages = self.driver.find_elements(
            *SolarCalculatorFeatureLocators.RESULT_MESSAGE
        )
        return " ".join(
            message.text.strip() for message in messages if message.is_displayed() and message.text.strip()
        )

    def get_constraints(self, element: WebElement) -> dict[str, str]:
        return {
            name: (element.get_attribute(name) or "").strip()
            for name in ("min", "max", "maxlength", "pattern", "step", "type")
        }

    def reset_calculator(self):
        self.clear_input()
        address_fields = self.driver.find_elements(
            *SolarCalculatorFeatureLocators.ADDRESS_INPUT
        )
        if address_fields:
            address_fields[0].clear()
