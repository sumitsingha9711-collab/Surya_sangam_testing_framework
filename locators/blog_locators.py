"""Centralized locators for the Surya Sangam blog module."""

from selenium.webdriver.common.by import By


class BlogLocators:
    """Locators for blog listing and blog article pages."""

    BLOG_HEADING = (
        By.XPATH,
        "//main//*[self::h1 or self::h2][contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'blog') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'smarthub')]",
    )
    BLOG_LISTING_SECTION = (
        By.XPATH,
        "//main//*[self::section or self::div][.//a[contains(@href, '/blogs/')]]",
    )
    BLOG_CARDS = (
        By.XPATH,
        "//main//*[self::article or self::section or self::div][.//a[contains(@href, '/blogs/')]]",
    )
    BLOG_TITLES = (
        By.XPATH,
        "//main//*[self::h2 or self::h3 or self::h4][normalize-space()]",
    )
    BLOG_IMAGES = (
        By.XPATH,
        "//main//img",
    )
    BLOG_AUTHOR = (
        By.XPATH,
        "//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'by ') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'author') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'author')]",
    )
    BLOG_PUBLISH_DATE = (
        By.XPATH,
        "//time | //*[(contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'date') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'time')) and normalize-space()]",
    )
    BLOG_CATEGORY = (
        By.XPATH,
        "//*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'category') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'category') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'solar basics') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'smart energy tips') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'latest news') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'magazine')]",
    )
    BLOG_SEARCH_BOX = (
        By.XPATH,
        "//input[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'search') or @type='search']",
    )
    BLOG_PAGINATION = (
        By.XPATH,
        "//nav[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'pagination')] | //button[normalize-space()='Previous' or normalize-space()='Next' or normalize-space()='1' or normalize-space()='2' or normalize-space()='Last'] | //a[normalize-space()='Previous' or normalize-space()='Next' or normalize-space()='1' or normalize-space()='2' or normalize-space()='Last']",
    )
    BLOG_PAGINATION_PREVIOUS = (
        By.XPATH,
        "//button[normalize-space()='Previous' or normalize-space()='Prev'] | //a[normalize-space()='Previous' or normalize-space()='Prev']",
    )
    BLOG_PAGINATION_NEXT = (
        By.XPATH,
        "//button[normalize-space()='Next'] | //a[normalize-space()='Next']",
    )
    BLOG_PAGINATION_FIRST = (
        By.XPATH,
        "//button[normalize-space()='1'] | //a[normalize-space()='1']",
    )
    BLOG_PAGINATION_LAST = (
        By.XPATH,
        "//button[normalize-space()='Last'] | //a[normalize-space()='Last']",
    )
    BLOG_FEATURED_IMAGE = (
        By.XPATH,
        "//main//img[contains(@alt, '')] | //main//img",
    )
    BLOG_CONTENT = (
        By.XPATH,
        "//main//p[normalize-space()] | //main//article | //main//div[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'content')]",
    )
    BLOG_SHARE_BUTTONS = (
        By.XPATH,
        "//a[contains(@href, 'linkedin.com') or contains(@href, 'facebook.com') or contains(@href, 'wa.me') or contains(@href, 'whatsapp.com') or contains(@href, 'x.com') or contains(@href, 'twitter.com')] | //button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'share')]",
    )
    BLOG_RELATED_POSTS = (
        By.XPATH,
        "//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'related posts') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'more from') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'you may also like')]",
    )
    BLOG_RELATED_LINKS = (
        By.XPATH,
        "//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'related posts') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'more from') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'you may also like')]/following::a[@href][1] | //main//a[contains(@href, '/blogs/') and not(contains(@href, '/blogs/1'))]",
    )
    INTERNAL_LINKS = (
        By.XPATH,
        "//a[@href and not(starts-with(@href, 'mailto:')) and not(starts-with(@href, 'tel:')) and not(ancestor::header)]",
    )
    EXTERNAL_LINKS = (
        By.XPATH,
        "//a[@href and (starts-with(@href, 'http://') or starts-with(@href, 'https://')) and not(contains(@href, 'suryasangam.com'))]",
    )
    BLOG_DETAIL_HEADING = (
        By.XPATH,
        "//main//*[self::h1 or self::h2 or self::h3][normalize-space()]",
    )
    BLOG_DETAIL_AUTHOR = BLOG_AUTHOR
    BLOG_DETAIL_DATE = BLOG_PUBLISH_DATE
    BLOG_DETAIL_FEATURED_IMAGE = BLOG_FEATURED_IMAGE
    BLOG_DETAIL_CONTENT = BLOG_CONTENT
    BLOG_DETAIL_RELATED_POSTS = BLOG_RELATED_POSTS
    BLOG_DETAIL_RELATED_LINKS = BLOG_RELATED_LINKS
    BLOG_DETAIL_SHARE_BUTTONS = BLOG_SHARE_BUTTONS
    BLOG_DETAIL_BREADCRUMB = (
        By.XPATH,
        "//nav[contains(@aria-label, 'breadcrumb') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'breadcrumb')] | //*[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'breadcrumb')]",
    )
