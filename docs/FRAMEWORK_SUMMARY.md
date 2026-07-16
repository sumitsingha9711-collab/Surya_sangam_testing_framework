# Surya Sangam Automation Framework Summary

## Purpose

This framework tests the Surya Sangam website using Python, Selenium, Pytest, and webdriver-manager. It currently covers the homepage, shared header navigation, CTA behavior, the About page, and the Solar Calculator section. It is built with the Page Object Model so the test cases stay readable while browser actions, waits, and locators remain reusable.

## How Each Folder Works

### `pages/`

This folder contains Page Object Model classes.

- `base_page.py` contains reusable Selenium actions such as click, type, clear, get text, scroll, wait for visibility, wait for clickable, and wait for page load.
- `home_page.py` represents the Surya Sangam homepage. It has methods for opening the homepage, checking the title and URL, verifying the hero section, validating CTA buttons, checking images, and validating the footer.
- `about_page.py` represents the Surya Sangam About page. It has methods for opening the About page, validating URL and title, checking the main heading and company description, validating About page images, CTA buttons, and internal navigation links.
- `calculator_page.py` represents the Solar Calculator section. It has methods for opening the calculator anchor, entering location, average units, and bill values, validating alerts/messages, checking result cards, clearing fields, and validating calculator buttons.
- `header.py` represents the website header. It handles logo clicks, navigation menu checks, menu item visibility, and navigation link clicks.

The benefit is that tests do not directly interact with Selenium details. Tests call readable methods like `verify_hero_section()` or `click_navigation_item()`.

### `locators/`

This folder stores all element locators.

- `home_locators.py` contains homepage element locators such as hero heading, CTA buttons, images, footer, and footer links.
- `about_locators.py` contains About page locators such as the main heading, company description, hero section, images, CTA buttons, breadcrumb, navigation links, and statistics section.
- `calculator_locators.py` contains Solar Calculator locators such as heading, address input, average units input, average bill input, calculate button, reset button, validation messages, result section, and calculator buttons.
- `header_locators.py` contains header locators such as logo, navigation menu, and menu links.

No XPath or CSS selector is written directly inside the test files. This makes maintenance easier if the website layout changes.

### `tests/`

This folder contains the actual Pytest test cases.

- `test_homepage.py` validates homepage load, URL, title, logo, hero banner, images, and footer.
- `test_about.py` validates About page load, URL, title, main heading, company description, images, CTA buttons, and internal navigation.
- `test_calculator.py` validates Solar Calculator load, URL, title, heading, required fields, empty input, invalid input, valid datasets, reset/clear behavior, and button behavior.
- `test_navigation.py` validates the header menu, logo click, and navigation links.
- `test_buttons.py` validates visible CTA buttons, checking that they are displayed, enabled, and clickable.

The test files are intentionally simple and readable because most browser logic is handled inside the page classes.

### `utils/`

This folder contains support utilities.

- `driver_factory.py` creates the Chrome browser using webdriver-manager and applies browser settings.
- `wait_utils.py` contains reusable explicit wait helpers.
- `screenshot.py` captures screenshots when tests fail.
- `report_generator.py` creates the plain text execution report.

### `reports/`

This folder stores the generated text report:

```text
execution_report.txt
```

The report includes execution date, browser, Python version, Selenium version, total tests, passed tests, failed tests, pass/fail percentage, result summary by area, duration, executed test cases, screenshot evidence for failed tests, and recommendations.

### `screenshots/`

This folder stores screenshots captured automatically when a test fails.

The screenshot filename contains the failed test name and timestamp, for example:

```text
test_all_visible_images_loaded_20260709_002908.png
```

### Root Files

- `conftest.py` manages pytest fixtures, browser setup and teardown, screenshot capture on failure, and report generation.
- `pytest.ini` configures pytest test discovery and markers.
- `requirements.txt` lists required Python packages.
- `README.md` explains how to install and run the framework.

## How Testing Was Managed Without HTML Tags

You did not provide the website's HTML code or element tags, so the live website was inspected through the browser and Selenium behavior.

The framework uses stable locator strategies based on visible page content and common semantic structure, such as:

- visible link text like `Home`, `Store`, `About Us`, and `Contact Us`
- visible button text like `Get Started`, `Get Advanced Quote`, `Select this System`, and `Become a Partner`
- image `alt` text like `Surya logo` and `Solar panels installation professional`
- page headings like `A Marketplace for Transparent & Cost-Effective Solar`
- About page content such as headings containing `About` and description text containing `Surya Sangam`
- common structural tags like `header`, `nav`, `footer`, `a`, `button`, and `img`

This approach avoids depending on unstable generated CSS class names, which are common in modern React or Next.js websites.

## How Buttons Were Tested

CTA buttons were identified using their visible text and page-level link/button structure. The framework checks that each visible CTA button is:

- displayed on the page
- enabled
- clickable
- able to produce a valid UI response

For buttons that redirect, the test checks that the browser URL changes or a new window opens. For buttons that do not navigate immediately, the test still verifies that the button remains enabled after the click and does not break the page.

This makes the button tests practical for homepage and About page CTA elements where some buttons may navigate and others may trigger interactive sections.

## About Page Coverage

Phase 3 adds About page automation without changing the framework architecture.

The About page module includes:

- page loading verification
- URL and title checks
- main heading visibility and non-empty text validation
- company description visibility and non-empty text validation
- visible image checks and broken-image validation
- CTA visibility, enabled state, clickability, and response validation
- internal navigation validation with return to the About page between link checks

All selectors remain in `locators/about_locators.py`; test files do not contain XPath or CSS selectors.

## Solar Calculator Coverage

Phase 4 adds Solar Calculator automation without changing the framework architecture.

The calculator module includes:

- calculator section loading verification
- URL, title, and heading checks
- mandatory field visibility checks
- empty input validation
- invalid numeric and location input validation
- valid dataset checks against visible estimator result cards
- reset or clear-field behavior
- calculator button visibility, enabled state, clickability, and validation response

The live calculator is available through the homepage anchor `https://www.suryasangam.com/#surya-calculator`. All selectors remain in `locators/calculator_locators.py`; test files do not contain XPath or CSS selectors.

## Report Troubleshooting

The text report now groups results by test area, such as Homepage, About, Calculator, Navigation, and Buttons.

When a test fails, the report writes these details directly under that test:

- problem details from Pytest
- screenshot path
- instruction to open the screenshot and inspect the exact browser state at failure

## How Forms Were Handled

The homepage includes form-like elements in the solar estimator section, such as address and billing-related inputs. Since the assignment focuses on homepage validation and not full calculator submission, the framework does not submit personal or location-based data.

The framework still supports form testing through reusable BasePage methods:

- `type()` for entering text
- `clear()` for clearing inputs
- `click()` for buttons
- `get_text()` for reading validation or result messages
- explicit waits for fields and buttons

This means future form tests can be added easily without changing the framework architecture.

## Waiting Strategy

The framework does not use `time.sleep()`.

It uses Selenium explicit waits for:

- element visibility
- element clickability
- page load completion
- image load completion

For lazy-loaded images, the framework scrolls through the page and waits for each visible image to finish loading before asserting.

## Why This Framework Is Scalable

New pages can be added by following the same structure:

1. Add locators in the `locators/` folder.
2. Add a page object class in the `pages/` folder.
3. Add readable test cases in the `tests/` folder.
4. Reuse utilities from `utils/`.

This keeps the framework clean, maintainable, and suitable for adding more Surya Sangam pages in later phases.
