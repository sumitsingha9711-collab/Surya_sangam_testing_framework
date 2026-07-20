"""CTA button tests for the Surya Sangam homepage."""

import pytest

from pages.home_page import HomePage


@pytest.mark.buttons
def test_cta_buttons_visible_enabled_clickable(driver):
    """Verify CTA buttons visible and enabled"""
    home_page = HomePage(driver)
    home_page.open_homepage()

    buttons = home_page.get_visible_cta_buttons()
    assert buttons, "No visible CTA buttons were found on the homepage."

    for button in buttons:
        label = button.text.strip() or button.get_attribute("aria-label")
        assert button.is_displayed(), f"CTA button '{label}' was not displayed."
        assert button.is_enabled(), f"CTA button '{label}' was not enabled."


@pytest.mark.buttons
def test_visible_cta_buttons_clickable(driver):
    """Verify every visible CTA button clickable"""
    home_page = HomePage(driver)
    home_page.open_homepage()

    buttons = home_page.get_visible_cta_buttons()
    assert buttons, "No visible CTA buttons were found on the homepage."

    for index in range(len(buttons)):
        buttons = home_page.get_visible_cta_buttons()
        button = buttons[index]
        label = button.text.strip() or button.get_attribute("aria-label")
        assert home_page.click_cta_and_verify_response(button), (
            f"CTA button '{label}' was not clickable."
        )
        home_page.open_homepage()
