"""Locators used only by the Phase 7 Person 2 Blog checks."""

from selenium.webdriver.common.by import By


class BlogsPerson2Locators:
    """Stable, content-oriented Blog locators."""

    BLOG_LINKS = (
        By.CSS_SELECTOR,
        "a[href*='/blogs/'], a[href*='/blogs?']",
    )
    BLOG_HEADING = (By.CSS_SELECTOR, "main h1, article h1, h1")
    CONTENT_IMAGES = (
        By.CSS_SELECTOR,
        "main img, article img, [role='main'] img",
    )
    CONTENT_LINKS = (
        By.CSS_SELECTOR,
        "main a[href], article a[href], [role='main'] a[href]",
    )
    SHARE_CONTROLS = (
        By.XPATH,
        "//main//*[self::a or self::button]["
        "contains(translate(@aria-label, 'SHARE', 'share'), 'share') or "
        "contains(translate(@title, 'SHARE', 'share'), 'share') or "
        "contains(translate(normalize-space(.), 'SHARE', 'share'), 'share') or "
        "contains(@href, 'facebook.com/sharer') or "
        "contains(@href, 'twitter.com/intent') or "
        "contains(@href, 'x.com/intent') or "
        "contains(@href, 'linkedin.com/share') or "
        "contains(@href, 'whatsapp.com/send') or "
        "contains(@href, 't.me/share')"
        "] | //article//*[self::a or self::button]["
        "contains(translate(@aria-label, 'SHARE', 'share'), 'share') or "
        "contains(translate(@title, 'SHARE', 'share'), 'share') or "
        "contains(translate(normalize-space(.), 'SHARE', 'share'), 'share') or "
        "contains(@href, 'facebook.com/sharer') or "
        "contains(@href, 'twitter.com/intent') or "
        "contains(@href, 'x.com/intent') or "
        "contains(@href, 'linkedin.com/share') or "
        "contains(@href, 'whatsapp.com/send') or "
        "contains(@href, 't.me/share')"
        "]",
    )
    RELATED_HEADING = (
        By.XPATH,
        "//*[self::h2 or self::h3 or self::h4][contains("
        "translate(normalize-space(.), 'RELATED', 'related'), 'related')]",
    )

