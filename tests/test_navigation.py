"""Header navigation tests for the Surya Sangam homepage."""

import pytest

from pages.header import Header
from pages.home_page import HomePage


@pytest.mark.navigation
def test_navigation_menu_visible(driver):
    """Verify navigation menu visible"""
    home_page = HomePage(driver)
    header = Header(driver)
    home_page.open_homepage()

    assert header.verify_navigation_menu(), "Navigation menu or expected links were hidden."


@pytest.mark.navigation
def test_logo_clickable(driver):
    """Verify logo clickable"""
    home_page = HomePage(driver)
    header = Header(driver)
    home_page.open_homepage()

    header.click_logo()
    assert home_page.verify_current_url(), "Logo did not navigate to the homepage."


@pytest.mark.navigation
@pytest.mark.parametrize(
    "menu_item",
    ["Home", "Store", "Surya SmartHub", "About Us", "Contact Us"],
)
def test_navigation_links_clickable(driver, menu_item):
    """Verify navigation links clickable"""
    home_page = HomePage(driver)
    header = Header(driver)
    home_page.open_homepage()

    assert header.verify_menu_item_visible(menu_item), f"{menu_item} link was not visible."
    header.click_navigation_item(menu_item)
    assert driver.current_url, f"{menu_item} click did not leave a valid browser URL."
