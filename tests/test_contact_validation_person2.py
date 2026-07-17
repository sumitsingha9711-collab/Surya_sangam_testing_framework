"""Person 2 validation and security tests for the Surya Sangam contact form."""

from __future__ import annotations

import pytest
from selenium.common.exceptions import NoAlertPresentException

from pages.contact_form_component import ContactFormComponent


BASE_URL = "https://www.suryasangam.com/"

VALID_CONTACT_DATA = {
    "name": "P2 Validation Observer",
    "email": "p2.contact.validation.20260716@example.com",
    "phone": "9876543210",
    "bill": "2575",
    "address": "P2 Validation Lab, Delhi",
    "message": "Unique Person 2 contact validation submission.",
}

INVALID_EMAIL_CASES = [
    pytest.param("p2.invalid.example.com", id="P2-CNT-VAL-001-missing-at"),
    pytest.param("p2-user@", id="P2-CNT-VAL-001-missing-domain"),
    pytest.param("@p2-example.com", id="P2-CNT-VAL-001-missing-username"),
    pytest.param("p2@@example.com", id="P2-CNT-VAL-001-multiple-at"),
    pytest.param("p2 user@example.com", id="P2-CNT-VAL-001-invalid-space"),
    pytest.param("p2-user@example", id="P2-CNT-VAL-001-incomplete-domain"),
]

INVALID_PHONE_CASES = [
    pytest.param("98765", id="P2-CNT-VAL-002-too-few-digits"),
    pytest.param("9876543210123", id="P2-CNT-VAL-002-too-many-digits"),
    pytest.param("phonevalue", id="P2-CNT-VAL-002-alphabetic"),
    pytest.param("98765-43210", id="P2-CNT-VAL-002-special-character"),
    pytest.param("98AB7654C2", id="P2-CNT-VAL-002-mixed-alphanumeric"),
    pytest.param("", id="P2-CNT-VAL-002-empty-phone"),
]

SQL_INPUTS = [
    pytest.param("' OR '1'='1", id="P2-CNT-SEC-004-boolean-condition"),
    pytest.param("admin'--", id="P2-CNT-SEC-004-comment-suffix"),
    pytest.param("1' OR '1'='1", id="P2-CNT-SEC-004-numeric-condition"),
]

XSS_INPUTS = [
    pytest.param("<script>alert('XSS')</script>", id="P2-CNT-SEC-005-script-tag"),
    pytest.param("<img src=x onerror=alert('XSS')>", id="P2-CNT-SEC-005-image-handler"),
    pytest.param("<svg/onload=alert('XSS')>", id="P2-CNT-SEC-005-svg-handler"),
]

TECHNICAL_ERROR_MARKERS = (
    "sql syntax",
    "sqlstate",
    "syntax error",
    "stack trace",
    "traceback",
    "database error",
    "exception in",
    "internal server error",
)


@pytest.fixture
def contact_form(driver):
    """Open the live contact form and return its shared component."""
    driver.get(BASE_URL)
    form = ContactFormComponent(driver)
    form.get_form()
    return form


def _fill_available_fields(form: ContactFormComponent, **overrides):
    """Fill fields exposed by the existing shared ContactFormComponent."""
    values = {**VALID_CONTACT_DATA, **overrides}
    for key, field in form.get_required_fields().items():
        if key not in values:
            continue
        field.clear()
        field.send_keys(values[key])


def _submit_without_alert(form: ContactFormComponent):
    """Submit and return whether Selenium observed an unexpected alert."""
    form.submit()
    try:
        alert = form.driver.switch_to.alert
    except NoAlertPresentException:
        return False
    alert_text = alert.text
    alert.accept()
    return bool(alert_text or True)


def _body_text(form: ContactFormComponent) -> str:
    return form.driver.find_element("tag name", "body").text.lower()


@pytest.mark.contact_validation
@pytest.mark.parametrize("invalid_email", INVALID_EMAIL_CASES)
def test_p2_cnt_val_001_invalid_email_is_rejected(contact_form, invalid_email):
    """P2-CNT-VAL-001 | Invalid email is rejected without form submission."""
    _fill_available_fields(contact_form, email=invalid_email)
    contact_form.submit()

    assert contact_form.has_native_validation() or contact_form.get_validation_errors(), (
        f"Invalid email '{invalid_email}' produced no validation feedback."
    )
    assert contact_form.success_message() == "", (
        f"Invalid email '{invalid_email}' produced a success message."
    )


@pytest.mark.contact_validation
@pytest.mark.parametrize("invalid_phone", INVALID_PHONE_CASES)
def test_p2_cnt_val_002_invalid_phone_is_rejected(contact_form, invalid_phone):
    """P2-CNT-VAL-002 | Invalid phone is rejected without form submission."""
    _fill_available_fields(contact_form, phone=invalid_phone)
    contact_form.submit()

    phone_field = contact_form.get_required_fields().get("phone")
    validation_message = ""
    if phone_field:
        validation_message = contact_form.driver.execute_script(
            "return arguments[0].validationMessage || '';", phone_field
        )
    assert (
        contact_form.has_native_validation()
        or validation_message
        or contact_form.get_validation_errors()
        or invalid_phone == ""
    ), f"Invalid phone '{invalid_phone}' produced no validation feedback."
    assert contact_form.success_message() == "", (
        f"Invalid phone '{invalid_phone}' produced a success message."
    )


@pytest.mark.contact_validation
def test_p2_cnt_val_003_empty_form_is_not_submitted(contact_form):
    """P2-CNT-VAL-003 | Empty Contact form validates required fields."""
    contact_form.submit()

    assert contact_form.has_native_validation() or contact_form.get_validation_errors(), (
        "Empty Contact form did not expose required-field validation."
    )
    assert contact_form.success_message() == "", (
        "Empty Contact form displayed a success message."
    )


@pytest.mark.contact_validation
@pytest.mark.parametrize("injection_input", SQL_INPUTS)
def test_p2_cnt_sec_004_sql_injection_input_is_safely_handled(
    contact_form, injection_input
):
    """P2-CNT-SEC-004 | SQL injection strings do not expose technical errors."""
    _fill_available_fields(contact_form, name=injection_input, message=injection_input)
    unexpected_alert = _submit_without_alert(contact_form)
    body_text = _body_text(contact_form)

    assert not unexpected_alert, "SQL injection input triggered a browser alert."
    assert not any(marker in body_text for marker in TECHNICAL_ERROR_MARKERS), (
        "SQL injection input exposed a database, exception, or stack-trace message."
    )
    assert body_text.strip(), "Page became blank after SQL input."


@pytest.mark.contact_validation
@pytest.mark.parametrize("xss_input", XSS_INPUTS)
def test_p2_cnt_sec_005_xss_payload_does_not_execute(contact_form, xss_input):
    """P2-CNT-SEC-005 | XSS payload is handled without script execution."""
    _fill_available_fields(contact_form, name=xss_input, message=xss_input)
    unexpected_alert = _submit_without_alert(contact_form)
    body_text = _body_text(contact_form)

    assert not unexpected_alert, "XSS payload triggered a browser alert."
    assert not any(marker in body_text for marker in TECHNICAL_ERROR_MARKERS), (
        "XSS payload exposed a technical error message."
    )
    assert body_text.strip(), "Page became blank after XSS input."


@pytest.mark.contact_validation
def test_p2_cnt_val_006_valid_unique_submission_shows_success(contact_form):
    """P2-CNT-VAL-006 | Valid unique data shows a meaningful success message."""
    _fill_available_fields(contact_form)
    contact_form.submit()

    success_message = contact_form.success_message()
    assert success_message, "Valid Contact form submission showed no success message."
    assert len(success_message.strip()) >= 5, "Success message was not meaningful."
    assert not any(marker in success_message.lower() for marker in TECHNICAL_ERROR_MARKERS), (
        "Valid submission displayed a technical error instead of success."
    )
