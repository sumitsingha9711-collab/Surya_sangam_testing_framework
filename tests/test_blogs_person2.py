"""Phase 7 Person 2: scoped Blog validation with one-pass navigation."""

from urllib.parse import urlparse
from urllib.request import Request, urlopen

import pytest

from pages.blogs_person2_page import BlogsPerson2Page


@pytest.mark.blogs
def test_p2_blogs_001_validate_unique_blogs_and_related_assets(driver):
    """P2-BLG-001 | Open blogs, images, shares, related posts, and broken links."""
    page = BlogsPerson2Page(driver)
    page.open_listing()
    blog_urls = page.discover_blog_urls()
    assert blog_urls, "P2-BLG-001: Blog listing did not expose any unique article URLs."

    visited = set()
    broken_images = set()
    broken_links = set()
    related_targets = set()
    share_missing = False
    share_broken = set()
    invalid_pages = []

    for blog_url in blog_urls:
        page.open_blog(blog_url)
        visited.add(blog_url)
        if not page.page_is_valid_blog(blog_url):
            invalid_pages.append(blog_url)
            continue

        broken_images.update(page.image_findings())
        controls = page.share_controls()
        if not controls:
            share_missing = True
        for control in controls:
            if not page.share_destination_is_valid(control, blog_url):
                share_broken.add(blog_url)

        related_targets.update(page.related_links())
        for href in page.content_links():
            if _is_relevant_link(href):
                broken_links.add(href) if not _reachable(href) else None

    # Related posts are checked at depth one only; discovered articles are already visited.
    for related_url in sorted(related_targets - visited):
        page.open_blog(related_url)
        if not page.page_is_valid_blog(related_url):
            broken_links.add(related_url)

    findings = []
    if invalid_pages:
        findings.append(f"invalid blog pages: {sorted(set(invalid_pages))}")
    if broken_images:
        findings.append(f"unique broken blog images: {sorted(broken_images)}")
    if share_missing:
        findings.append("share controls were absent on one or more blog pages")
    if share_broken:
        findings.append(f"invalid share controls on: {sorted(share_broken)}")
    if broken_links:
        findings.append(f"unique broken blog-scope links: {sorted(broken_links)}")
    assert not findings, "P2-BLG-001 unique findings: " + "; ".join(findings)


def _is_relevant_link(href):
    parsed = urlparse(href)
    if parsed.scheme in {"mailto", "tel", "javascript"} or not parsed.netloc:
        return False
    return parsed.netloc.endswith("suryasangam.com") or parsed.path.startswith("/blogs/")


def _reachable(url):
    try:
        request = Request(url, method="HEAD", headers={"User-Agent": "pytest-selenium"})
        with urlopen(request, timeout=8) as response:
            return 200 <= response.status < 400
    except Exception:
        try:
            request = Request(url, headers={"User-Agent": "pytest-selenium"})
            with urlopen(request, timeout=8) as response:
                return 200 <= response.status < 400
        except Exception:
            return False
