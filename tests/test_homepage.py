"""Homepage content tests for Surya Sangam."""

import pytest

from pages.home_page import HomePage


@pytest.mark.homepage
def test_homepage_loads_successfully(driver):
    """Homepage loads successfully"""
    home_page = HomePage(driver)
    home_page.open_homepage()

    assert home_page.verify_current_url(), "Homepage URL did not match expected URL."
    assert home_page.verify_title(), "Homepage title did not contain Surya Sangam."


@pytest.mark.homepage
def test_homepage_title(driver):
    """Verify page title"""
    home_page = HomePage(driver)
    home_page.open_homepage()

    assert home_page.verify_title(), f"Unexpected page title: {driver.title}"


@pytest.mark.homepage
def test_homepage_logo_visible(driver):
    """Verify logo"""
    home_page = HomePage(driver)
    home_page.open_homepage()

    assert home_page.verify_logo_visible(), "Header logo was not visible."


@pytest.mark.homepage
def test_hero_banner_content(driver):
    """Verify Hero Banner"""
    home_page = HomePage(driver)
    home_page.open_homepage()

    assert home_page.verify_hero_section(), "Hero content was incomplete or hidden."
    assert home_page.verify_banner(), "Hero banner image did not load successfully."


@pytest.mark.homepage
def test_all_visible_images_loaded(driver):
    """Verify homepage images load successfully"""
    home_page = HomePage(driver)
    home_page.open_homepage()

    assert home_page.verify_images_loaded(), "One or more visible homepage images are broken."


@pytest.mark.homepage
def test_footer_visible_when_present(driver):
    """Verify footer content"""
    home_page = HomePage(driver)
    home_page.open_homepage()

    assert home_page.verify_footer_visible(), "Footer was not visible on the homepage."
    assert home_page.verify_footer_links_visible(), "Footer links were not visible."
