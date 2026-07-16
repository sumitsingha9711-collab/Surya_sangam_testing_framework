"""Locators for the Surya Sangam solar calculator section."""

from selenium.webdriver.common.by import By


class CalculatorLocators:
    """Centralized solar calculator locators."""

    CALCULATOR_SECTION = (
        By.XPATH,
        "//h1[normalize-space()='Rooftop Solar Estimator']/ancestor::section[1]",
    )
    CALCULATOR_HEADING = (
        By.XPATH,
        "//h1[normalize-space()='Rooftop Solar Estimator']",
    )
    LOCATION_INPUT = (
        By.XPATH,
        "//input[@placeholder='Search your location or address']",
    )
    AVERAGE_UNITS_INPUT = (By.NAME, "avg_unit")
    MONTHLY_BILL_INPUT = (By.NAME, "avg_bill")
    INPUT_FIELDS = (
        By.XPATH,
        "//input[@placeholder='Search your location or address'] | "
        "//input[@name='avg_unit'] | //input[@name='avg_bill']",
    )
    DROPDOWNS = (
        By.XPATH,
        "//h1[normalize-space()='Rooftop Solar Estimator']/ancestor::section[1]//select",
    )
    RADIO_BUTTONS = (
        By.XPATH,
        "//h1[normalize-space()='Rooftop Solar Estimator']/ancestor::section[1]"
        "//input[@type='radio']",
    )
    CHECKBOXES = (
        By.XPATH,
        "//h1[normalize-space()='Rooftop Solar Estimator']/ancestor::section[1]"
        "//input[@type='checkbox']",
    )
    CURRENT_LOCATION_BUTTON = (
        By.XPATH,
        "//button[@aria-label='Get current location']",
    )
    CALCULATE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Get Advanced Quote']",
    )
    RESET_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Reset' or normalize-space()='Clear']",
    )
    VALIDATION_MESSAGES = (
        By.XPATH,
        "//*[contains(translate(normalize-space(), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'required') "
        "or contains(translate(normalize-space(), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'please enter') "
        "or contains(translate(normalize-space(), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'invalid')]",
    )
    ERROR_MESSAGES = (
        By.XPATH,
        "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
        "'error') or contains(translate(normalize-space(), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'error')]",
    )
    SUCCESS_MESSAGES = (
        By.XPATH,
        "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
        "'success') or contains(translate(normalize-space(), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'success')]",
    )
    RESULT_SECTION = (
        By.XPATH,
        "//h1[normalize-space()='Discover YOUR Perfect Fit']/ancestor::*[self::section or self::div][1] | "
        "//button[contains(normalize-space(), 'Select this System')]/ancestor::*[self::section or self::div][1]",
    )
    RESULT_CARDS = (
        By.XPATH,
        "//button[contains(normalize-space(), 'Surya Max DCR') "
        "or contains(normalize-space(), 'Surya Dual DCR') "
        "or contains(normalize-space(), 'Surya Core DCR') "
        "or contains(normalize-space(), 'Surya Flex N-DCR')]",
    )
    INTERACTIVE_BUTTONS = (
        By.XPATH,
        "//button[@aria-label='Get current location'] | "
        "//button[normalize-space()='Get Advanced Quote']",
    )
