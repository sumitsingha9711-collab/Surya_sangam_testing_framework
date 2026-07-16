from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By


BASE_URL = "https://www.suryasangam.com/"


@pytest.fixture
def homepage(driver):
    driver.get(BASE_URL)
    return driver


def _all_homepage_images(driver):
    return driver.find_elements(By.TAG_NAME, "img")


def test_all_homepage_images_are_displayed(homepage):
    images = _all_homepage_images(homepage)

    assert images, "Expected homepage images to be present."
    for image in images:
        assert image.is_displayed(), f"Image is not displayed: {image.get_attribute('src')}"


def test_homepage_image_src_attributes_are_not_empty(homepage):
    images = _all_homepage_images(homepage)

    assert images, "Expected homepage images to be present."
    for image in images:
        src = (image.get_attribute("src") or "").strip()
        assert src, "Homepage images must have a non-empty src attribute."


def test_homepage_images_are_not_broken(homepage):
    images = _all_homepage_images(homepage)

    assert images, "Expected homepage images to be present."

    broken_images = []
    for image in images:
        src = (image.get_attribute("src") or "").strip()
        if not src:
            broken_images.append("<empty src>")
            continue
        is_loaded = homepage.execute_script(
            "return arguments[0].complete && arguments[0].naturalWidth > 0;",
            image,
        )
        if not is_loaded:
            broken_images.append(src)

    assert not broken_images, "Broken homepage image(s) detected: " + ", ".join(broken_images)
