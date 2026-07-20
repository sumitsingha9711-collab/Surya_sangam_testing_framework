from __future__ import annotations

from urllib.parse import urlparse

import pytest
from selenium.webdriver.common.by import By


BASE_URL = "https://www.suryasangam.com/"
SOCIAL_DOMAINS = ("linkedin.com", "instagram.com", "x.com", "twitter.com")


@pytest.fixture
def homepage(driver):
    driver.get(BASE_URL)
    return driver


def _collect_social_links(driver):
    anchors = driver.find_elements(By.TAG_NAME, "a")
    social_links = []
    for anchor in anchors:
        href = (anchor.get_attribute("href") or "").strip().lower()
        if any(domain in href for domain in SOCIAL_DOMAINS):
            social_links.append(anchor)
    return social_links


def test_social_media_links_are_visible(homepage):
    social_links = _collect_social_links(homepage)

    assert social_links, "Expected social media links on the homepage."
    assert all(link.is_displayed() for link in social_links)


def test_social_media_links_contain_valid_href_values(homepage):
    social_links = _collect_social_links(homepage)

    assert social_links, "Expected social media links on the homepage."
    for link in social_links:
        href = (link.get_attribute("href") or "").strip()
        assert href, "Social media links must contain a valid href."


def test_social_media_links_do_not_contain_empty_urls(homepage):
    social_links = _collect_social_links(homepage)

    assert social_links, "Expected social media links on the homepage."
    assert all((link.get_attribute("href") or "").strip() for link in social_links)


def test_social_media_links_open_expected_destination(homepage):
    social_links = _collect_social_links(homepage)

    assert social_links, "Expected social media links on the homepage."
    for link in social_links:
        href = (link.get_attribute("href") or "").strip()
        parsed = urlparse(href)
        assert parsed.scheme in {"http", "https"}
        assert any(domain in parsed.netloc.lower() for domain in SOCIAL_DOMAINS)
