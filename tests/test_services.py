"""Services module tests for Surya Sangam."""

import pytest

from pages.services_page import ServicesPage


@pytest.fixture
def services_page(driver):
    """Open the services hub and return the page object."""
    page = ServicesPage(driver)
    page.open_services_page()
    return page


def _service_count(services_page):
    cards = services_page.get_all_service_cards()
    assert cards, "Expected at least one service card on the services hub."
    return len(cards)


def _reopen_service(services_page, index):
    """Open a service card again after returning to the hub."""
    services_page.return_to_services_page()
    return services_page.open_service(index)


@pytest.mark.services
def test_services_page_loads_successfully(services_page):
    """Verify the services hub loads successfully."""
    assert services_page.verify_page_loaded(), "Services page did not load successfully."
    assert services_page.verify_page_title(), "Services page title did not contain Surya Sangam."
    assert services_page.verify_current_url(), "Services page URL did not match the services hub route."
    assert services_page.verify_hero_section(), "Services hero section was not visible."
    assert services_page.verify_services_heading(), "Services heading was not visible."


@pytest.mark.services
def test_service_cards_are_displayed_and_clickable(services_page):
    """Verify every service card is visible and clickable."""
    card_count = _service_count(services_page)

    for index in range(card_count):
        cards = services_page.get_all_service_cards()
        card = cards[index]
        title = services_page.get_service_card_title(card)
        description = services_page.get_service_card_description(card)
        image = services_page.get_service_card_image(card)
        ctas = services_page.get_service_card_cta_buttons(card)
        original_url = services_page.driver.current_url

        assert card.is_displayed(), f"Service card '{title}' was not displayed."
        assert title, f"Service card {index + 1} did not expose a title."
        assert description, f"Service card '{title}' did not expose a description."
        assert image is not None, f"Service card '{title}' did not expose an image."
        assert image.is_displayed(), f"Service card '{title}' image was not displayed."
        assert ctas, f"Service card '{title}' did not expose a CTA button."
        assert all(cta.is_displayed() for cta in ctas), f"Service card '{title}' had a hidden CTA."
        assert all(cta.is_enabled() for cta in ctas), f"Service card '{title}' had a disabled CTA."

        opened_url = services_page.open_service(index)
        assert opened_url != original_url, f"Service card '{title}' did not navigate away from the hub."
        assert services_page.verify_service_heading(), f"Service card '{title}' did not open a valid detail page."
        assert services_page.verify_service_description(), f"Service page for '{title}' did not expose a description."
        assert services_page.return_to_services_page(), f"Could not return to the services hub after opening '{title}'."
        assert services_page.verify_page_loaded(), "Services page did not reload after returning from a service detail page."


@pytest.mark.services
def test_service_navigation_opens_each_available_service(services_page):
    """Verify every service card can be opened and revisited."""
    card_count = _service_count(services_page)
    original_url = services_page.driver.current_url

    for index in range(card_count):
        cards = services_page.get_all_service_cards()
        title = services_page.get_service_card_title(cards[index])

        opened_url = services_page.open_service(index)
        assert opened_url != original_url, f"Service '{title}' did not open a different URL."
        assert services_page.verify_service_heading(), f"Service '{title}' did not display a heading."
        assert services_page.verify_service_description(), f"Service '{title}' did not display a description."
        assert services_page.verify_service_sections(), f"Service '{title}' did not expose the expected sections."
        assert services_page.verify_page_title(), f"Service '{title}' did not keep the Surya Sangam title."
        assert services_page.return_to_services_page(), f"Could not return to the services hub after visiting '{title}'."
        assert services_page.verify_page_loaded(), f"Services hub did not reload after visiting '{title}'."


@pytest.mark.services
def test_service_content_is_complete(services_page):
    """Verify service page content blocks are populated."""
    card_count = _service_count(services_page)

    for index in range(card_count):
        cards = services_page.get_all_service_cards()
        title = services_page.get_service_card_title(cards[index])
        services_page.open_service(index)

        assert services_page.verify_service_heading(), f"Service '{title}' heading was not visible."
        assert services_page.verify_service_description(), f"Service '{title}' description was empty."
        assert services_page.verify_service_images(), f"Service '{title}' images were missing or broken."
        assert services_page.verify_service_icons(), f"Service '{title}' icons were missing or not visible."
        assert services_page.verify_service_statistics(), f"Service '{title}' statistics block failed validation."
        assert services_page.verify_no_empty_sections(), f"Service '{title}' contained an empty content block."
        assert services_page.verify_service_sections(), f"Service '{title}' did not expose the expected sections."
        assert services_page.return_to_services_page(), f"Could not return to the services hub after checking '{title}'."


@pytest.mark.services
def test_service_cta_buttons_are_visible_enabled_and_clickable(services_page):
    """Verify every visible CTA on each service page is usable."""
    card_count = _service_count(services_page)

    for service_index in range(card_count):
        cards = services_page.get_all_service_cards()
        title = services_page.get_service_card_title(cards[service_index])
        services_page.open_service(service_index)

        buttons = services_page.get_cta_buttons()
        assert buttons, f"No CTA buttons were found on the service page for '{title}'."

        for button_index in range(len(buttons)):
            buttons = services_page.get_cta_buttons()
            button = buttons[button_index]
            label = button.text.strip() or button.get_attribute("aria-label") or button.get_attribute("title") or f"CTA {button_index + 1}"

            assert button.is_displayed(), f"CTA '{label}' was not displayed on '{title}'."
            assert button.is_enabled(), f"CTA '{label}' was disabled on '{title}'."
            assert services_page.click_cta_button(button), f"CTA '{label}' was not clickable on '{title}'."
            assert services_page.return_to_services_page(), f"Could not return to the services hub after clicking CTA '{label}' on '{title}'."
            services_page.open_service(service_index)


@pytest.mark.services
def test_service_images_are_displayed_and_loaded(services_page):
    """Verify service images are visible and fully loaded."""
    card_count = _service_count(services_page)

    for index in range(card_count):
        cards = services_page.get_all_service_cards()
        title = services_page.get_service_card_title(cards[index])
        services_page.open_service(index)

        images = services_page.get_visible_service_images()
        assert images, f"No visible images were found on the service page for '{title}'."
        assert all(image.is_displayed() for image in images), f"One or more images were hidden on '{title}'."
        assert services_page.verify_all_images_loaded(), f"One or more images were broken on '{title}'."
        assert services_page.return_to_services_page(), f"Could not return to the services hub after checking images for '{title}'."


@pytest.mark.services
def test_service_navigation_and_header_behaviour(services_page):
    """Verify breadcrumb, header, back, and internal navigation behavior."""
    card_count = _service_count(services_page)
    assert services_page.verify_header_navigation(), "Header navigation was not visible on the services hub."

    for index in range(card_count):
        cards = services_page.get_all_service_cards()
        title = services_page.get_service_card_title(cards[index])
        services_page.open_service(index)

        assert services_page.verify_breadcrumb_navigation(), f"Breadcrumb navigation failed on '{title}'."
        assert services_page.verify_header_navigation(), f"Header navigation was hidden on '{title}'."
        assert services_page.return_to_services_page(), f"Back navigation failed after opening '{title}'."
        assert services_page.verify_page_loaded(), f"Services hub did not reload after leaving '{title}'."

        links = services_page.get_service_links()
        for link_index in range(len(links)):
            links = services_page.get_service_links()
            link = links[link_index]
            label = link.text.strip() or link.get_attribute("href") or f"Link {link_index + 1}"
            assert services_page.verify_internal_link(link), f"Internal link '{label}' did not navigate correctly on '{title}'."
            assert services_page.return_to_services_page(), f"Could not return to the services hub after opening internal link '{label}' on '{title}'."
            services_page.open_service(index)


@pytest.mark.services
def test_service_links_remain_stable_across_multiple_transitions(services_page):
    """Verify internal links remain functional after repeated page transitions."""
    card_count = _service_count(services_page)

    for index in range(card_count):
        cards = services_page.get_all_service_cards()
        title = services_page.get_service_card_title(cards[index])
        services_page.open_service(index)

        links = services_page.get_service_links()
        if not links:
            assert services_page.return_to_services_page(), f"Could not return to the services hub after visiting '{title}'."
            continue

        for link_index in range(len(links)):
            links = services_page.get_service_links()
            link = links[link_index]
            label = link.text.strip() or link.get_attribute("href") or f"Link {link_index + 1}"
            assert services_page.verify_internal_link(link), f"Internal link '{label}' failed on '{title}'."
            assert services_page.return_to_services_page(), f"Could not return to the services hub after visiting internal link '{label}' on '{title}'."
            services_page.open_service(index)

        assert services_page.return_to_services_page(), f"Could not return to the services hub after validating links for '{title}'."
