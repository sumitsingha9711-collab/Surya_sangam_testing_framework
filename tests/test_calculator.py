"""Solar calculator tests for Surya Sangam."""

import pytest

from pages.calculator_page import CalculatorPage


VALID_DATASETS = [
    ("Noida Sector 62", "300", "2500"),
    ("Ghaziabad", "450", "3600"),
    ("Delhi", "150.5", "1800.75"),
]

INVALID_NUMERIC_VALUES = [
    "abc",
    "!@#$",
    "-100",
    "999999999999",
]


@pytest.mark.calculator
def test_calculator_page_loads_successfully(driver):
    """Verify Solar Calculator page opens successfully"""
    calculator_page = CalculatorPage(driver)
    calculator_page.open_calculator_page()

    assert calculator_page.verify_page_loaded(), (
        "Solar Calculator section did not load successfully."
    )


@pytest.mark.calculator
def test_calculator_url_title_and_heading(driver):
    """Verify Solar Calculator URL title and heading"""
    calculator_page = CalculatorPage(driver)
    calculator_page.open_calculator_page()

    assert calculator_page.verify_current_url(), (
        f"Unexpected calculator URL: {driver.current_url}"
    )
    assert calculator_page.verify_page_title(), (
        f"Unexpected calculator page title: {driver.title}"
    )
    assert calculator_page.verify_calculator_heading(), (
        "Calculator heading was not visible."
    )


@pytest.mark.calculator
def test_calculator_required_fields_visible(driver):
    """Verify Solar Calculator mandatory fields visible"""
    calculator_page = CalculatorPage(driver)
    calculator_page.open_calculator_page()

    assert calculator_page.get_input_fields(), "Calculator input fields were not found."
    assert calculator_page.get_location_value() == "", (
        "Location field was not initially empty."
    )
    assert calculator_page.get_average_units_value() == "", (
        "Average units field was not initially empty."
    )
    assert calculator_page.get_monthly_bill_value() == "", (
        "Average bill field was not initially empty."
    )


@pytest.mark.calculator
def test_calculator_empty_values_show_validation(driver):
    """Verify Solar Calculator empty values validation"""
    calculator_page = CalculatorPage(driver)
    calculator_page.open_calculator_page()

    validation_message = calculator_page.click_calculate()

    assert validation_message or calculator_page.verify_validation_message(), (
        "Validation message was not displayed for empty calculator input."
    )
    assert calculator_page.verify_current_url(), (
        "User did not remain on the calculator page after empty submission."
    )


@pytest.mark.calculator
@pytest.mark.parametrize("invalid_value", INVALID_NUMERIC_VALUES)
def test_calculator_invalid_numeric_values_handled(driver, invalid_value):
    """Verify Solar Calculator invalid numeric values handled"""
    calculator_page = CalculatorPage(driver)
    calculator_page.open_calculator_page()

    calculator_page.enter_location("Noida")
    calculator_page.enter_average_units(invalid_value)
    calculator_page.enter_monthly_bill(invalid_value)
    validation_message = calculator_page.click_calculate()

    assert calculator_page.verify_current_url(), (
        "Calculator navigated away unexpectedly after invalid numeric input."
    )
    assert validation_message or calculator_page.verify_validation_message() or (
        calculator_page.get_average_units_value() != invalid_value
        and calculator_page.get_monthly_bill_value() != invalid_value
    ), f"Invalid numeric value '{invalid_value}' was not rejected or validated."


@pytest.mark.calculator
@pytest.mark.parametrize(
    "location",
    ["@@@", "   Noida   ", "Noida #12", ""],
)
def test_calculator_location_input_validation(driver, location):
    """Verify Solar Calculator location input validation"""
    calculator_page = CalculatorPage(driver)
    calculator_page.open_calculator_page()

    calculator_page.enter_location(location)
    calculator_page.enter_average_units("300")
    calculator_page.enter_monthly_bill("2500")
    validation_message = calculator_page.click_calculate()

    assert calculator_page.verify_current_url(), (
        "Calculator navigated away unexpectedly after location validation."
    )
    assert validation_message or calculator_page.verify_validation_message() or not (
        calculator_page.verify_result_displayed()
    ), (
        "Invalid location was accepted and produced a calculator result."
    )


@pytest.mark.calculator
@pytest.mark.parametrize("location, units, monthly_bill", VALID_DATASETS)
def test_calculator_valid_datasets_show_results(driver, location, units, monthly_bill):
    """Verify Solar Calculator valid datasets show estimator results"""
    calculator_page = CalculatorPage(driver)
    calculator_page.open_calculator_page()

    calculator_page.fill_required_fields(location, units, monthly_bill)

    assert calculator_page.get_location_value().strip(), "Location value was empty."
    assert calculator_page.get_average_units_value(), "Average units value was empty."
    assert calculator_page.get_monthly_bill_value(), "Average bill value was empty."
    validation_message = calculator_page.click_calculate()
    assert not validation_message, (
        f"Valid dataset produced validation: {validation_message}"
    )
    assert calculator_page.verify_result_displayed(), (
        "Solar estimator result cards were not displayed."
    )
    assert calculator_page.get_calculation_result(), (
        "Calculator result section text was empty."
    )
    assert not calculator_page.has_unexpected_error(), (
        "Unexpected calculator error was displayed for valid input."
    )


@pytest.mark.calculator
def test_calculator_reset_or_clear_fields(driver):
    """Verify Solar Calculator reset clears fields"""
    calculator_page = CalculatorPage(driver)
    calculator_page.open_calculator_page()
    calculator_page.fill_required_fields("Noida", "300", "2500")

    calculator_page.click_reset()

    assert calculator_page.get_location_value() == "", "Location field was not cleared."
    assert calculator_page.get_average_units_value() == "", (
        "Average units field was not cleared."
    )
    assert calculator_page.get_monthly_bill_value() == "", (
        "Average bill field was not cleared."
    )


@pytest.mark.calculator
def test_calculator_buttons_visible_enabled_clickable(driver):
    """Verify Solar Calculator buttons visible enabled and clickable"""
    calculator_page = CalculatorPage(driver)
    calculator_page.open_calculator_page()

    buttons = calculator_page.get_interactive_buttons()
    assert buttons, "No calculator buttons were found."

    for button in buttons:
        label = button.text.strip() or button.get_attribute("aria-label")
        assert button.is_displayed(), f"Calculator button '{label}' was not displayed."
        assert button.is_enabled(), f"Calculator button '{label}' was not enabled."

    validation_message = calculator_page.click_calculate()
    assert validation_message or calculator_page.verify_validation_message(), (
        "Calculate button did not produce the expected validation response."
    )
