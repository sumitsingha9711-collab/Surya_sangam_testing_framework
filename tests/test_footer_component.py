from __future__ import annotations

from urllib.parse import urlparse

import pytest
from selenium.webdriver.common.by import By

from pages.footer_component import FooterComponent


BASE_URL = "https://www.suryasangam.com/"


@pytest.fixture
def homepage(driver):
    driver.get(BASE_URL)
    return driver


def test_footer_is_displayed(homepage):
    footer = FooterComponent(homepage)
    assert footer.is_visible(), "Footer should be displayed on the homepage."


def test_footer_contains_expected_sections(homepage):
    footer = FooterComponent(homepage)
    sections = footer.get_section_headings()

    for expected in ("Follow Us", "Our Offerings", "Resources", "About Us", "Help", "Contact Us", "Registered Office"):
        assert expected in sections or expected in footer.get_text(), f"Expected footer section missing: {expected}"


def test_footer_links_are_visible(homepage):
    footer = FooterComponent(homepage)
    visible_links = footer.get_visible_footer_links()

    assert visible_links, "Expected at least one visible footer link."
    for link in visible_links:
        assert link.is_displayed()
        assert link.text.strip() or (link.get_attribute("aria-label") or "").strip()


def test_footer_links_have_valid_href_attributes(homepage):
    footer = FooterComponent(homepage)
    links = footer.get_visible_footer_links()

    hrefs = []
    for link in links:
        href = (link.get_attribute("href") or "").strip()
        assert href, "Footer links must have a non-empty href attribute."
        assert not href.lower().startswith("javascript:"), f"Invalid footer link href: {href}"
        hrefs.append(href)

    assert hrefs, "Expected footer href values to be collected."


def test_footer_contact_information_is_visible(homepage):
    footer = FooterComponent(homepage)
    contact_text = footer.get_contact_information()

    assert contact_text, "Footer contact information should be visible."
    assert "@suryasangam.com" in footer.get_text() or "customer.support" in footer.get_text()
    assert "+91" in footer.get_text()


def test_footer_copyright_information_is_visible(homepage):
    footer = FooterComponent(homepage)
    copyright_text = footer.get_copyright_text()

    assert copyright_text, "Footer copyright text should be visible."
    assert "All Rights Reserved" in copyright_text


def test_footer_social_media_links_are_present(homepage):
    footer = FooterComponent(homepage)
    social_links = footer.get_visible_social_media_links()

    assert social_links, "Expected social media links in the footer."


def test_footer_social_media_links_contain_valid_urls(homepage):
    footer = FooterComponent(homepage)
    social_links = footer.get_visible_social_media_links()

    assert social_links, "Expected social media links in the footer."

    allowed_domains = ("linkedin.com", "instagram.com", "x.com", "twitter.com")
    for link in social_links:
        href = (link.get_attribute("href") or "").strip()
        parsed = urlparse(href)
        assert href, "Social media links must not be empty."
        assert parsed.scheme in {"http", "https"}, f"Invalid social media link scheme: {href}"
        assert any(domain in parsed.netloc.lower() for domain in allowed_domains), (
            f"Unexpected social media destination: {href}"
        )
