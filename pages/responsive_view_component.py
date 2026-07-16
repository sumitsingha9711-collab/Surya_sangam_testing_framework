from __future__ import annotations

from selenium.webdriver.common.by import By


class ResponsiveViewComponent:
    def __init__(self, driver):
        self.driver = driver

    def set_viewport(self, width: int, height: int):
        self.driver.set_window_size(width, height)

    def has_horizontal_overflow(self) -> bool:
        return bool(
            self.driver.execute_script(
                "return Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) > window.innerWidth + 1;"
            )
        )

    def get_visible_images(self):
        return [img for img in self.driver.find_elements(By.TAG_NAME, "img") if img.is_displayed()]

    def are_images_within_viewport(self) -> bool:
        viewport_width = self.driver.execute_script("return window.innerWidth;")
        viewport_height = self.driver.execute_script("return window.innerHeight;")
        for image in self.get_visible_images():
            rect = image.rect
            if rect["x"] < 0 or rect["y"] < 0:
                return False
            if rect["x"] + rect["width"] > viewport_width + 2:
                return False
            if rect["y"] + rect["height"] > viewport_height + 200:
                continue
        return True

    def get_header(self):
        headers = self.driver.find_elements(By.TAG_NAME, "header")
        return headers[0] if headers else None

    def header_is_usable(self) -> bool:
        header = self.get_header()
        if header is None:
            return True
        return header.is_displayed() and header.rect["height"] > 0

    def footer_is_usable(self) -> bool:
        footers = self.driver.find_elements(By.TAG_NAME, "footer")
        if not footers:
            return True
        footer = footers[0]
        return footer.is_displayed() and footer.rect["height"] > 0

    def homepage_content_visible(self) -> bool:
        headlines = self.driver.find_elements(By.XPATH, "//h1 | //h2 | //h3")
        return any(element.is_displayed() for element in headlines)

    def buttons_are_clickable(self) -> bool:
        buttons = self.driver.find_elements(By.XPATH, "//button | //a[contains(@class, 'btn') or contains(@role, 'button')]")
        visible_buttons = [button for button in buttons if button.is_displayed()]
        return all(button.is_enabled() for button in visible_buttons)

    def no_text_overlap_in_viewport(self) -> bool:
        key_elements = self.driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //p | //button | //a")
        visible = [element for element in key_elements if element.is_displayed()]
        for index, first in enumerate(visible):
            first_rect = first.rect
            for second in visible[index + 1 :]:
                second_rect = second.rect
                same_x = abs(first_rect["x"] - second_rect["x"]) < 1
                same_y = abs(first_rect["y"] - second_rect["y"]) < 1
                same_w = abs(first_rect["width"] - second_rect["width"]) < 1
                same_h = abs(first_rect["height"] - second_rect["height"]) < 1
                if same_x and same_y and same_w and same_h:
                    return False
        return True
