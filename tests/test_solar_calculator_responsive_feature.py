from __future__ import annotations

import pytest

from pages.solar_calculator_feature import SolarCalculatorFeature
from locators.solar_calculator_feature_locators import SolarCalculatorFeatureLocators


BASE_URL = "https://www.suryasangam.com/"
VIEWPORTS = {
    "desktop": (1920, 1080),
    "laptop": (1366, 768),
    "tablet": (768, 1024),
    "mobile": (390, 844),
}


def solar_test(test_id: str):
    def decorator(function):
        function.solar_test_id = test_id
        function.solar_module = "Solar Calculator"
        function.solar_owner = "Person 2"
        return function

    return decorator


@pytest.mark.parametrize("viewport_name", VIEWPORTS)
@solar_test("SC-P2-TC-007")
def test_solar_calculator_responsive_layout(driver, viewport_name):
    width, height = VIEWPORTS[viewport_name]
    driver.set_window_size(width, height)
    calculator = SolarCalculatorFeature(driver)
    calculator.open_calculator(BASE_URL)

    assert calculator.is_visible(), f"Calculator is not visible at {viewport_name}."
    assert all(field.is_displayed() for field in calculator.get_numeric_inputs())
    assert driver.execute_script(
        "return Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) "
        "<= window.innerWidth + 1;"
    ), f"Horizontal overflow detected at {viewport_name}."

    button = driver.find_element(
        *SolarCalculatorFeatureLocators.CALCULATE_BUTTON
    )
    assert button.is_displayed() and button.is_enabled()
