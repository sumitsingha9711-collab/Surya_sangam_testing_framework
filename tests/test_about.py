"""About page tests for Surya Sangam."""

import pytest

from pages.about_page import AboutPage


@pytest.mark.about
def test_about_page_loads_successfully(driver):
    """Verify About page opens successfully"""
    about_page = AboutPage(driver)
    about_page.open_about_page()

    assert about_page.verify_page_loaded(), "About page did not load successfully."


@pytest.mark.about
def test_about_page_url(driver):
    """Verify About page URL"""
    about_page = AboutPage(driver)
    about_page.open_about_page()

    assert about_page.verify_current_url(), (
        f"About page URL did not match expected URL. Actual: {driver.current_url}"
    )


@pytest.mark.about
def test_about_page_title(driver):
    """Verify About page title"""
    about_page = AboutPage(driver)
    about_page.open_about_page()

    assert about_page.get_page_title(), "About page title was empty."
    assert about_page.verify_page_title(), (
        f"Unexpected About page title: {about_page.get_page_title()}"
    )


@pytest.mark.about
def test_about_main_heading_visible(driver):
    """Verify About page main heading"""
    about_page = AboutPage(driver)
    about_page.open_about_page()

    heading_text = about_page.get_main_heading_text()
    assert about_page.verify_main_heading(), "About page main heading was not visible."
    assert heading_text, "About page main heading text was empty."


@pytest.mark.about
def test_about_company_description_visible(driver):
    """Verify About page company description"""
    about_page = AboutPage(driver)
    about_page.open_about_page()

    description_text = about_page.get_company_description_text()
    assert about_page.verify_company_description(), (
        "About page company description was not visible."
    )
    assert description_text, "About page company description text was empty."


@pytest.mark.about
def test_about_images_loaded(driver):
    """Verify About page images load successfully"""
    about_page = AboutPage(driver)
    about_page.open_about_page()

    images = about_page.get_visible_about_images()
    assert images, "No visible About page images were found."
    for index, image in enumerate(images, start=1):
        assert image.is_displayed(), f"About page image {index} was not displayed."
    assert about_page.verify_images_loaded(), (
        "One or more visible About page images are broken."
    )


@pytest.mark.about
def test_about_cta_buttons_visible_enabled_clickable(driver):
    """Verify About page CTA buttons"""
    about_page = AboutPage(driver)
    about_page.open_about_page()

    buttons = about_page.get_visible_cta_buttons()
    assert buttons, "No visible CTA buttons were found on the About page."

    for index in range(len(buttons)):
        buttons = about_page.get_visible_cta_buttons()
        button = buttons[index]
        label = button.text.strip() or button.get_attribute("aria-label")

        assert button.is_displayed(), f"CTA button '{label}' was not displayed."
        assert button.is_enabled(), f"CTA button '{label}' was not enabled."
        assert about_page.click_cta_button(button), (
            f"CTA button '{label}' was not clickable."
        )
        about_page.open_about_page()


@pytest.mark.about
def test_about_internal_navigation_links(driver):
    """Verify About page internal navigation links"""
    about_page = AboutPage(driver)
    about_page.open_about_page()

    links = about_page.get_internal_navigation_links()
    assert links, "No internal navigation links were found on the About page."

    for index in range(len(links)):
        links = about_page.get_internal_navigation_links()
        link = links[index]
        label = link.text.strip() or link.get_attribute("href")

        assert link.is_displayed(), f"Internal link '{label}' was not displayed."
        assert link.is_enabled(), f"Internal link '{label}' was not enabled."
        assert about_page.verify_internal_navigation(link), (
            f"Internal link '{label}' did not navigate correctly."
        )
        about_page.open_about_page()
