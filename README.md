# Surya Sangam Selenium Automation

Python, Selenium, and Pytest automation for the Surya Sangam website using Page Object Model (POM).

## Coverage

- Homepage, hero content, images, footer, and CTAs
- About page content, images, navigation, and CTAs
- Header navigation
- Responsive layout checks
- Footer and social links
- Rooftop Solar Estimator validation and calculations
- Contact page form, security, contact-information, and button checks

## Structure

```text
pages/       Page objects and reusable components
locators/    Centralized Selenium locators
tests/       Independent Pytest scenarios
utils/       Driver, waits, screenshots, reports, and email support
docs/        Framework and learning documentation
conftest.py  Shared browser fixture and reporting hooks
pytest.ini   Test discovery and markers
```

The calculator uses the homepage anchor `#surya-calculator`. Valid address submissions select an autocomplete suggestion before calculation. The current page has address, average units, and average bill fields; optional dropdown, radio, checkbox, reset, validation, and result support remains in the page object for future UI changes.

## Setup

```powershell
pip install -r requirements.txt
```

## Run

```powershell
pytest
pytest -m calculator
pytest -m homepage
pytest -m about
pytest -m contact
```

The existing Pytest hook captures failure screenshots under `screenshots/` and generates `reports/execution_report.txt`. No test creates a separate reporting system.

## Email Reports

Set these variables only when email delivery is required:

```powershell
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "your_email@gmail.com"
$env:SMTP_PASSWORD = "your_app_password"
$env:SURYA_REPORT_EMAIL_TO = "first@example.com,second@example.com"
```

See `docs/FRAMEWORK_SUMMARY.md` and `docs/TECHNOLOGY_AND_LEARNING_GUIDE.md` for architecture and maintenance guidance.