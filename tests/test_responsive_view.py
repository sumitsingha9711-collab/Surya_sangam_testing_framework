from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By

from pages.responsive_view_component import ResponsiveViewComponent


BASE_URL = "https://www.suryasangam.com/"
VIEWPORTS = [
    ("desktop", 1920, 1080),
    ("laptop", 1366, 768),
    ("tablet", 768, 1024),
    ("mobile", 390, 844),
]


@pytest.fixture
def homepage(driver):
    driver.get(BASE_URL)
    return driver


@pytest.mark.parametrize("viewport_name,width,height", VIEWPORTS)
def test_homepage_responsive_layout(homepage, viewport_name, width, height):
    responsive = ResponsiveViewComponent(homepage)
    responsive.set_viewport(width, height)

    homepage.refresh()

    assert not responsive.has_horizontal_overflow(), f"Horizontal overflow detected at {viewport_name} size."
    assert responsive.header_is_usable(), f"Header is not usable at {viewport_name} size."
    assert responsive.homepage_content_visible(), f"Homepage content is not visible at {viewport_name} size."
    assert responsive.buttons_are_clickable(), f"Buttons are not clickable at {viewport_name} size."
    assert responsive.are_images_within_viewport(), f"Images are outside the viewport at {viewport_name} size."
    assert responsive.no_text_overlap_in_viewport(), f"Overlapping text detected at {viewport_name} size."

    homepage.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    assert responsive.footer_is_usable(), f"Footer is not usable at {viewport_name} size."
