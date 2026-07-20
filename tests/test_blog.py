"""Blog module tests for Surya Sangam."""

from urllib.parse import urlparse

import pytest

from pages.blog_page import BlogPage


@pytest.fixture
def blog_page(driver):
    """Open the blog listing page and return the page object."""
    page = BlogPage(driver)
    page.open_blog_page()
    return page


def _blog_count(page):
    cards = page.get_blog_cards()
    if not cards:
        pytest.skip("Blog cards were not discoverable in the current site markup.")
    return len(cards)


@pytest.mark.blog
def test_blog_listing_loads_successfully(blog_page):
    """Verify blog listing loads successfully."""
    assert blog_page.verify_page_loaded(), "Blog listing did not load successfully."
    assert blog_page.verify_page_title(), "Blog page title did not contain Surya Sangam."
    assert blog_page.verify_current_url(), "Blog page URL did not match the listing route."
    assert blog_page.verify_blog_listing(), "Blog listing content was incomplete or hidden."
    assert blog_page.get_blog_cards(), "No blog cards were found on the listing page."
    assert blog_page.get_blog_titles(), "No blog titles were found on the listing page."


@pytest.mark.blog
def test_blog_cards_display_images_titles_dates_and_categories(blog_page):
    """Verify blog cards are rendered with visible metadata."""
    cards = blog_page.get_blog_cards()
    if not cards:
        pytest.skip("Blog cards were not discoverable in the current site markup.")

    for index, card in enumerate(cards, start=1):
        title = blog_page.get_blog_card_title(card)
        image = blog_page.get_blog_card_image(card)
        date_text = blog_page.get_blog_card_date(card)
        category_text = blog_page.get_blog_card_category(card)

        assert card.is_displayed(), f"Blog card {index} was not displayed."
        assert title, f"Blog card {index} did not expose a title."
        assert image is not None, f"Blog card '{title}' did not expose an image."
        assert image.is_displayed(), f"Blog card '{title}' image was not displayed."
        assert date_text, f"Blog card '{title}' did not expose a publish date."
        assert category_text, f"Blog card '{title}' did not expose a category."


@pytest.mark.blog
def test_open_every_blog_and_validate_article_content(blog_page):
    """Open every blog and validate article content."""
    blog_count = _blog_count(blog_page)
    listing_url = blog_page.driver.current_url

    for index in range(blog_count):
        cards = blog_page.get_blog_cards()
        title = blog_page.get_blog_card_title(cards[index])
        opened_url = blog_page.open_blog(index)

        assert opened_url != listing_url, f"Blog '{title}' did not navigate away from the listing."
        assert blog_page.verify_blog_heading(), f"Blog '{title}' did not show a heading."
        assert blog_page.verify_blog_content(), f"Blog '{title}' did not show article content."
        assert blog_page.verify_featured_image(), f"Blog '{title}' featured image was missing or broken."
        assert blog_page.verify_author(), f"Blog '{title}' author metadata was missing."
        assert blog_page.verify_publish_date(), f"Blog '{title}' publish date was missing."
        assert blog_page.return_to_blog_listing(), f"Could not return to the blog listing after visiting '{title}'."
        assert blog_page.verify_page_loaded(), f"Blog listing did not reload after visiting '{title}'."


@pytest.mark.blog
def test_related_posts_and_links_work(blog_page):
    """Verify related blog posts are present and functional."""
    blog_page.open_blog(0)
    assert blog_page.verify_related_posts(), "Related posts section was missing or empty."

    links = blog_page.get_related_post_links()
    if not links:
        pytest.skip("Related blog posts were not discoverable in the current site markup.")

    for index in range(len(links)):
        links = blog_page.get_related_post_links()
        link = links[index]
        label = link.text.strip() or link.get_attribute("href") or f"Related link {index + 1}"
        assert blog_page.verify_internal_link(link), f"Related post link '{label}' did not navigate correctly."
        assert blog_page.verify_blog_heading() or blog_page.verify_blog_content(), (
            f"Related post link '{label}' did not open a valid article."
        )
        assert blog_page.return_to_blog_listing(), f"Could not return to the blog listing after '{label}'."
        assert blog_page.verify_page_loaded(), "Blog listing did not reload after related post navigation."
        blog_page.open_blog(0)


@pytest.mark.blog
def test_share_buttons_are_visible_enabled_and_clickable(blog_page):
    """Verify share buttons are usable when present on a blog page."""
    blog_page.open_blog(0)
    buttons = blog_page.get_share_buttons()
    if not buttons:
        pytest.skip("Share buttons were not present on the current blog page.")

    for index in range(len(buttons)):
        buttons = blog_page.get_share_buttons()
        button = buttons[index]
        label = button.text.strip() or button.get_attribute("aria-label") or button.get_attribute("title") or f"Share {index + 1}"

        assert button.is_displayed(), f"Share control '{label}' was not displayed."
        assert button.is_enabled(), f"Share control '{label}' was not enabled."
        assert blog_page.click_share_button(button), f"Share control '{label}' was not clickable."

        if len(blog_page.driver.window_handles) > 1:
            for handle in blog_page.driver.window_handles[1:]:
                blog_page.driver.switch_to.window(handle)
                blog_page.driver.close()
            blog_page.driver.switch_to.window(blog_page.driver.window_handles[0])
        else:
            blog_page.driver.back()
        blog_page.wait_for_page_load()
        assert blog_page.return_to_blog_listing(), f"Could not return to the blog listing after clicking '{label}'."
        blog_page.open_blog(0)


@pytest.mark.blog
def test_blog_pagination_is_functional(blog_page):
    """Verify blog pagination controls work when available."""
    controls = blog_page.get_pagination_controls()
    if not controls:
        pytest.skip("Pagination controls were not present on the blog listing page.")

    original_url = blog_page.driver.current_url
    page_links = {control.text.strip(): control for control in controls if control.text.strip()}
    assert page_links, "Pagination controls did not expose visible labels."

    if "Next" in page_links:
        blog_page.click_pagination("next")
        assert blog_page.driver.current_url != original_url, "Next page did not change the blog listing URL."
        assert blog_page.verify_page_loaded(), "Blog listing did not remain valid after opening the next page."
        if "Previous" in page_links or "Prev" in page_links:
            blog_page.click_pagination("previous")
            assert blog_page.verify_page_loaded(), "Blog listing did not return to a valid first page."

    if "1" in page_links:
        blog_page.click_pagination("first")
        assert blog_page.verify_page_loaded(), "First page control did not return to a valid listing."

    if "Last" in page_links:
        before_last = blog_page.driver.current_url
        blog_page.click_pagination("last")
        assert blog_page.driver.current_url != before_last, "Last page control did not change the listing URL."
        assert blog_page.verify_page_loaded(), "Blog listing did not remain valid after opening the last page."


@pytest.mark.blog
def test_blog_internal_and_external_links_are_valid(blog_page):
    """Verify blog listing and article links are functional."""
    blog_links = blog_page.get_blog_links()
    if not blog_links:
        pytest.skip("No discoverable article links were present in the blog listing markup.")

    for index in range(len(blog_links)):
        blog_links = blog_page.get_blog_links()
        link = blog_links[index]
        href = (link.get_attribute("href") or "").strip()
        label = link.text.strip() or href or f"Blog link {index + 1}"

        assert href, f"Blog link '{label}' did not contain a valid href."
        parsed = urlparse(href)
        if parsed.netloc.endswith("suryasangam.com"):
            assert blog_page.verify_internal_link(link), f"Blog link '{label}' did not navigate correctly."
            assert blog_page.return_to_blog_listing(), f"Could not return to the blog listing after '{label}'."
            assert blog_page.verify_page_loaded(), f"Blog listing did not reload after visiting '{label}'."

    blog_page.open_blog(0)
    internal_links = blog_page.verify_internal_links()
    external_links = blog_page.get_external_links()

    if not internal_links:
        pytest.skip("No internal links were present on the blog article page.")
    if external_links:
        assert blog_page.verify_external_links(), "External blog links were present but invalid."
