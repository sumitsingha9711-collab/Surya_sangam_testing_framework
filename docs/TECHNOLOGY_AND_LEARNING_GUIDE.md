# Technology and Learning Guide

## Stack

- Python 3.x for page objects, tests, and utilities.
- Selenium for browser automation.
- Pytest for fixtures, parametrization, markers, assertions, and hooks.
- webdriver-manager for ChromeDriver installation and management.

## POM Design

The framework keeps selectors and browser actions out of tests:

1. Add or update selectors in `locators/`.
2. Put reusable browser behavior in `BasePage` or the relevant page object.
3. Keep tests focused on setup, actions, and meaningful assertions.
4. Reuse the shared driver fixture, screenshot hook, and text report.

The canonical calculator example is:

```python
calculator_page = CalculatorPage(driver)
calculator_page.open_calculator_page()
calculator_page.enter_location("Noida Sector 62")
calculator_page.enter_average_units("300")
calculator_page.enter_monthly_bill("2500")
calculator_page.click_calculate()
assert calculator_page.verify_result_displayed()
```

## Waits and Reliability

Use explicit waits through `BasePage` or `WebDriverWait`. Do not add `time.sleep()`. Prefer stable semantic selectors such as names, placeholders, accessible labels, and visible text. Keep XPath and CSS selectors in locator modules only.

The Solar Calculator address flow is asynchronous. `CalculatorPage` waits briefly for a visible autocomplete suggestion and selects it when available. Invalid or unmatched input is allowed to remain unselected so validation behavior can be tested.

## Reporting

`conftest.py` owns failure handling. When a test fails, the hook captures a screenshot and passes the result to `ReportGenerator`. Do not add a second reporter in an individual test module. The generated report is stored at `reports/execution_report.txt`.

## Adding a Feature

Use the existing architecture:

- Add a locator class under `locators/`.
- Add or extend a page object under `pages/`.
- Add independent tests under `tests/`.
- Register a marker in `pytest.ini` if the feature needs one.
- Update `docs/FRAMEWORK_SUMMARY.md` when behavior or structure changes.

Avoid creating parallel page objects for the same page. Extend the canonical page object or add a small reusable component when the behavior is genuinely shared.

## Useful Commands

```powershell
python -m compileall -q pages locators tests
pytest --collect-only
pytest -m calculator
pytest
```
## Contact Page Example

The Contact page follows the same page-object flow as the calculator:

```python
contact_page = ContactPage(driver)
contact_page.open_contact_page()
contact_page.enter_name("Automation Tester")
contact_page.enter_email("automation@example.com")
contact_page.enter_phone("9876543210")
contact_page.enter_message("Solar enquiry")
contact_page.submit_form()
```

The live form also requires average electricity bill and address values. Use `ContactPage.fill_required_fields()` when submitting a complete dataset. Tests should accept native validation, inline/alert feedback, or a safe in-page response when the external submission service does not return a success message.