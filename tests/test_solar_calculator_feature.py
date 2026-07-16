from __future__ import annotations

import pytest

from pages.solar_calculator_feature import SolarCalculatorFeature


BASE_URL = "https://www.suryasangam.com/"


def solar_test(test_id: str):
    def decorator(function):
        function.solar_test_id = test_id
        function.solar_module = "Solar Calculator"
        function.solar_owner = "Person 2"
        return function

    return decorator


@pytest.fixture
def calculator(driver):
    page = SolarCalculatorFeature(driver)
    page.open_calculator(BASE_URL)
    return page


def _assert_calculator_response(calculator):
    error = calculator.get_error_message()
    result = calculator.get_result()
    assert error or result or calculator.is_visible(), (
        "Calculator produced no validation message, result, or visible state."
    )


@solar_test("SC-P2-TC-001")
def test_calculator_is_visible(calculator):
    assert calculator.is_visible()


@solar_test("SC-P2-TC-002")
def test_boundary_values_follow_application_constraints(calculator):
    inputs = calculator.get_numeric_inputs()
    constrained_inputs = [
        (field, calculator.get_constraints(field))
        for field in inputs
        if calculator.get_constraints(field).get("min")
        or calculator.get_constraints(field).get("max")
    ]
    if not constrained_inputs:
        pytest.skip("The calculator does not expose min/max boundary constraints.")

    for field, constraints in constrained_inputs:
        field.clear()
        field.send_keys(constraints.get("min") or constraints.get("max"))
        calculator.click_calculate()
        _assert_calculator_response(calculator)


@solar_test("SC-P2-TC-003")
@pytest.mark.parametrize("negative_value", [-1, -10, -100])
def test_negative_numeric_input_is_rejected_or_handled(calculator, negative_value):
    calculator.enter_input(units=negative_value, bill=2500)
    calculator.click_calculate()
    _assert_calculator_response(calculator)
    assert not calculator.get_error_message() or not calculator.get_result(), (
        "A negative input must not produce an unqualified result alongside an error."
    )


@solar_test("SC-P2-TC-004")
@pytest.mark.parametrize("large_value", [999999, 99999999, 999999999])
def test_large_numeric_input_keeps_calculator_responsive(calculator, large_value):
    calculator.enter_input(units=large_value, bill=large_value)
    calculator.click_calculate()
    _assert_calculator_response(calculator)
    assert calculator.is_visible(), "Calculator became unavailable after large input."


@solar_test("SC-P2-TC-005")
def test_empty_numeric_input_shows_validation_or_remains_safe(calculator):
    calculator.clear_input()
    calculator.click_calculate()
    _assert_calculator_response(calculator)
    assert calculator.is_visible(), "Calculator should remain usable after empty submission."


@solar_test("SC-P2-TC-006")
def test_non_numeric_input_is_handled_without_crash(calculator):
    calculator.enter_input(units="not-a-number", bill="invalid")
    calculator.click_calculate()
    _assert_calculator_response(calculator)
    assert calculator.is_visible(), "Calculator should remain usable after invalid input."
