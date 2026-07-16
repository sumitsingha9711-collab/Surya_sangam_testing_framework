# Surya Sangam Selenium Automation

This project is a Python Selenium + Pytest automation framework for testing the Surya Sangam homepage, About page, header navigation, CTA buttons, and Solar Calculator section.

## Tech Stack

- Python 3.x
- Selenium
- Pytest
- webdriver-manager

## Project Structure

```text
surya_sangam_testing/
├── pages/
├── locators/
├── tests/
├── utils/
├── reports/
├── screenshots/
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run all tests:

```bash
pytest
```

Run a specific marker:

```bash
pytest -m homepage
pytest -m about
pytest -m calculator
pytest -m navigation
pytest -m buttons
```

## Features

- Page Object Model design
- Locators stored outside test files
- Explicit waits only
- Chrome driver management through webdriver-manager
- Screenshots captured automatically on test failure
- Plain text report generated at `reports/execution_report.txt`
- Report includes an area-wise summary and screenshot evidence under failed tests
- Tests focused on homepage, About page, navigation, CTA buttons, and Solar Calculator validation

## Reports and Screenshots

After each run, the framework writes a text report to:

```text
reports/execution_report.txt
```

Failure screenshots are saved in:

```text
screenshots/
```

Screenshot filenames include the failed test name and timestamp.

The report also prints the screenshot path directly below each failed test so the problem can be inspected quickly.

## Email Report

The report can be emailed automatically after a pytest run. Set these environment
variables before running `pytest`:

```powershell
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "your_email@gmail.com"
$env:SMTP_PASSWORD = "your_app_password"
$env:SURYA_REPORT_EMAIL_TO = "first@example.com,second@example.com"
```

Optional variables:

```powershell
$env:SMTP_FROM = "your_email@gmail.com"
$env:SURYA_REPORT_EMAIL_CC = "manager@example.com"
$env:SURYA_REPORT_EMAIL_BCC = "audit@example.com"
$env:SURYA_REPORT_EMAIL_SUBJECT = "Automation Report"
$env:SMTP_USE_TLS = "true"
```

If the email variables are not set, tests still run normally and only generate
`reports/execution_report.txt`.
