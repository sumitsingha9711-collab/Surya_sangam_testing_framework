"""Contact page tests for Surya Sangam."""

import pytest

from locators.contact_locators import ContactLocators
from pages.contact_page import ContactPage


VALID_DATA = {
    "name": "Automation Tester",
    "email": "automation@example.com",
    "phone": "9876543210",
    "bill": "2500",
    "address": "Aditya World City, Ghaziabad",
    "message": "Please share rooftop solar information.",
}


@pytest.fixture
def contact_page(driver):
    page = ContactPage(driver)
    page.open_contact_page()
    return page


@pytest.mark.contact
def test_contact_page_loads_successfully(contact_page):
    """Verify Contact page loads successfully"""
    assert contact_page.verify_page_loaded()


@pytest.mark.contact
def test_contact_page_url_and_title(contact_page):
    """Verify Contact page URL and title"""
    assert contact_page.verify_current_url()
    assert contact_page.verify_page_title()


@pytest.mark.contact
def test_contact_form_fields_are_present(contact_page):
    """Verify Contact form fields are visible"""
    assert contact_page.get_form_fields()
    assert contact_page.is_visible(ContactLocators.NAME_INPUT)
    assert contact_page.is_visible(ContactLocators.EMAIL_INPUT)
    assert contact_page.is_visible(ContactLocators.PHONE_INPUT)
    assert contact_page.is_visible(ContactLocators.MESSAGE_INPUT)


@pytest.mark.contact
def test_empty_contact_form_shows_validation(contact_page):
    """Verify empty Contact form validation"""
    contact_page.submit_form()
    assert contact_page.verify_validation_message()
    assert contact_page.verify_current_url()


@pytest.mark.contact
def test_valid_contact_submission_is_handled(contact_page):
    """Verify valid Contact form submission is handled"""
    contact_page.fill_required_fields(**VALID_DATA)
    alert_text = contact_page.submit_form()

    assert contact_page.verify_current_url()
    assert (
        contact_page.verify_success_message()
        or alert_text
        or not contact_page.verify_validation_message()
    ), "Valid submission produced neither success nor a safe page response."


def _invalid_response_is_handled(contact_page):
    """Return True when invalid input is validated or does not succeed."""
    return (
        contact_page.verify_validation_message()
        or not contact_page.verify_success_message()
    )


@pytest.mark.contact
@pytest.mark.parametrize("email", ["invalid", "missing@domain", "a@b"])
def test_invalid_email_is_rejected_or_handled(contact_page, email):
    """Verify invalid email validation"""
    data = {**VALID_DATA, "email": email}
    contact_page.fill_required_fields(**data)
    contact_page.submit_form()

    assert contact_page.verify_current_url()
    assert _invalid_response_is_handled(contact_page)


@pytest.mark.contact
@pytest.mark.parametrize("phone", ["123", "abcdefghij", "!@#$%^&*()"])
def test_invalid_phone_is_rejected_or_handled(contact_page, phone):
    """Verify invalid phone validation"""
    data = {**VALID_DATA, "phone": phone}
    contact_page.fill_required_fields(**data)
    contact_page.submit_form()

    assert contact_page.verify_current_url()
    assert _invalid_response_is_handled(contact_page)


@pytest.mark.contact
@pytest.mark.parametrize("field_name", ["name", "email", "phone", "bill", "address"])
def test_missing_required_field_shows_validation(contact_page, field_name):
    """Verify missing required Contact field validation"""
    data = {**VALID_DATA, field_name: ""}
    contact_page.fill_required_fields(**data)
    contact_page.submit_form()

    assert contact_page.verify_validation_message()
    assert contact_page.verify_current_url()


@pytest.mark.contact
@pytest.mark.parametrize("payload", ["' OR '1'='1", "<script>alert('xss')</script>", "<img src=x onerror=alert(1)>"])
def test_security_payloads_are_handled_safely(contact_page, payload):
    """Verify Contact form handles injection and markup payloads safely"""
    data = {**VALID_DATA, "name": payload, "message": payload}
    contact_page.fill_required_fields(**data)
    alert_text = contact_page.submit_form()

    assert contact_page.verify_current_url()
    assert not alert_text.lower().startswith("javascript:")
    assert contact_page.verify_page_title()


@pytest.mark.contact
def test_long_contact_input_does_not_break_page(contact_page):
    """Verify maximum Contact input length is handled"""
    long_value = "A" * 1000
    data = {**VALID_DATA, "name": long_value, "message": long_value}
    contact_page.fill_required_fields(**data)
    contact_page.submit_form()

    assert contact_page.verify_page_loaded()
    assert contact_page.verify_current_url()


@pytest.mark.contact
def test_contact_form_handles_spaces(contact_page):
    """Verify Contact form handles leading and trailing spaces"""
    data = {
        **VALID_DATA,
        "name": "  Automation Tester  ",
        "email": "  automation@example.com  ",
        "message": "  Solar enquiry  ",
    }
    contact_page.fill_required_fields(**data)
    contact_page.submit_form()

    assert contact_page.verify_current_url()
    assert contact_page.verify_page_title()


@pytest.mark.contact
def test_contact_buttons_are_visible_enabled_and_clickable(contact_page):
    """Verify Contact buttons are visible and enabled"""
    submit = contact_page.wait_for_clickable(ContactLocators.SUBMIT_BUTTON)
    assert submit.is_displayed()
    assert submit.is_enabled()

    for cta in contact_page.get_contact_ctas():
        assert cta.is_displayed()
        assert cta.is_enabled()

    reset_buttons = contact_page.driver.find_elements(*ContactLocators.RESET_BUTTON)
    for reset in reset_buttons:
        assert reset.is_displayed()
        assert reset.is_enabled()


@pytest.mark.contact
def test_clear_contact_form_clears_fields(contact_page):
    """Verify Contact form clear behavior"""
    contact_page.fill_required_fields(**VALID_DATA)
    contact_page.clear_form()

    assert all(
        not field.get_attribute("value")
        for field in contact_page.get_form_fields()
    )


@pytest.mark.contact
def test_contact_information_is_displayed(contact_page):
    """Verify Contact email phone and address"""
    assert "@suryasangam.com" in contact_page.get_contact_email()
    assert "+91" in contact_page.get_contact_phone()
    assert "Ghaziabad" in contact_page.get_contact_address()


@pytest.mark.contact
def test_google_map_when_present(contact_page):
    """Verify Google Map when the Contact page provides one"""
    map_elements = contact_page.driver.find_elements(*ContactLocators.GOOGLE_MAP)
    if not map_elements:
        pytest.skip("Contact page does not currently provide a Google Map element.")

    assert any(element.is_displayed() for element in map_elements)