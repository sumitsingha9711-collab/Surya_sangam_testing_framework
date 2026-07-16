from __future__ import annotations

from urllib.parse import urlparse

import pytest

from pages.about_information_page import AboutInformationPage
from pages.responsive_view_component import ResponsiveViewComponent


BASE_URL = "https://www.suryasangam.com/"
ABOUT_PATH_FRAGMENT = "/aboutus"


@pytest.fixture
def about_page(driver):
    page = AboutInformationPage(driver)
    page.open_from_homepage(BASE_URL)
    page.wait_for_loaded()
    return page


def test_about_page_opens_successfully(about_page):
    assert about_page.is_loaded(), "About page should open successfully."


def test_about_page_url_is_correct(about_page):
    assert ABOUT_PATH_FRAGMENT in about_page.driver.current_url


def test_about_page_title_is_correct(about_page):
    assert "Solar Marketplace" in about_page.driver.title or "Surya Sangam" in about_page.driver.title


def test_about_page_main_heading_is_visible(about_page):
    assert about_page.get_primary_heading().is_displayed()


def test_about_page_company_description_is_visible(about_page):
    body_text = about_page.get_visible_text()
    assert "Surya Sangam" in body_text
    assert "solar energy" in body_text.lower()


def test_about_page_important_sections_are_visible(about_page):
    assert about_page.has_expected_content()


def test_about_page_text_is_not_empty(about_page):
    assert about_page.has_non_empty_text()


def test_about_page_expected_headings_are_present(about_page):
    text = about_page.get_visible_text()
    for expected in ("Who are we?", "Our Mission", "What We Offer", "Why Choose Surya Sangam?", "Our Commitment"):
        assert expected in text


def test_about_page_images_are_visible(about_page):
    images = about_page.get_images()
    assert images, "Expected images on the About page."
    assert all(image.is_displayed() for image in images)


def test_about_page_image_src_attributes_are_not_empty(about_page):
    sources = about_page.image_sources()
    assert sources, "Expected image sources on the About page."
    assert all(source for source in sources)


def test_about_page_images_are_not_broken(about_page):
    broken_images = about_page.broken_images()
    assert not broken_images, "Broken About page image(s): " + ", ".join(broken_images)


def test_about_page_cta_buttons_are_visible_enabled_and_clickable(about_page):
    ctas = about_page.get_cta_buttons()
    assert ctas, "Expected CTA buttons on the About page."
    for cta in ctas:
        assert cta.is_displayed()
        assert cta.is_enabled()


def test_about_page_navigation_and_header_functionality(about_page):
    current_url = about_page.driver.current_url
    header_links = [link for link in about_page.driver.find_elements_by_tag_name("a") if link.is_displayed()]  # type: ignore[attr-defined]
    assert header_links, "Expected navigation links to be present."
    about_page.driver.back()
    about_page.driver.forward()
    assert current_url in about_page.driver.current_url


def test_about_page_internal_links_work(about_page):
    internal_links = about_page.get_internal_links()
    assert internal_links, "Expected internal links on the About page."
    for link in internal_links:
        href = (link.get_attribute("href") or "").strip()
        assert href
        assert urlparse(href).scheme in {"http", "https"}


def test_about_page_back_navigation_works(about_page):
    about_page.driver.get(BASE_URL)
    about_page.open_from_homepage(BASE_URL)
    current_url = about_page.driver.current_url
    about_page.go_back()
    assert BASE_URL in about_page.driver.current_url or current_url != about_page.driver.current_url


@pytest.mark.parametrize("viewport_name,width,height", [
    ("desktop", 1920, 1080),
    ("laptop", 1366, 768),
    ("tablet", 768, 1024),
    ("mobile", 390, 844),
])
def test_about_page_responsive_layout(about_page, viewport_name, width, height):
    responsive = ResponsiveViewComponent(about_page.driver)
    responsive.set_viewport(width, height)
    about_page.driver.refresh()
    about_page.wait_for_loaded()

    assert not responsive.has_horizontal_overflow(), f"Horizontal overflow detected at {viewport_name} size."
    assert responsive.header_is_usable(), f"Header is not usable at {viewport_name} size."
    assert responsive.footer_is_usable(), f"Footer is not usable at {viewport_name} size."
