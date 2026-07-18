"""Screenshot utility for failed tests."""

import hashlib
import re
from pathlib import Path


SCREENSHOT_DIR = Path(__file__).resolve().parents[1] / "screenshots"


def capture_screenshot(driver, test_name):
    """Capture one validated screenshot per test and return its path.

    The filename is deterministic, so reruns update the same evidence instead
    of creating timestamped duplicates. A screenshot is rejected when the
    browser is closed, has no usable page URL, or returns empty image bytes.
    """
    if driver is None:
        raise ValueError("A live WebDriver instance is required.")

    try:
        current_url = driver.current_url
    except Exception as error:
        raise RuntimeError("The browser session is no longer available.") from error

    if not current_url or current_url in {"about:blank", "data:,"}:
        raise RuntimeError(f"No usable page is loaded for screenshot: {current_url!r}")

    try:
        image_bytes = driver.get_screenshot_as_png()
    except Exception as error:
        raise RuntimeError("The browser could not capture a screenshot.") from error

    if not image_bytes or not image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("The browser returned invalid or empty screenshot data.")

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    test_id = str(test_name)
    readable_name = re.sub(r"[^0-9A-Za-z._-]+", "_", test_id).strip("_")
    readable_name = readable_name[:100] or "failed_test"
    digest = hashlib.sha1(test_id.encode("utf-8")).hexdigest()[:10]
    screenshot_path = SCREENSHOT_DIR / f"{readable_name}_{digest}.png"

    # Deterministic path: a rerun replaces the old evidence instead of adding
    # another timestamped screenshot for the same test.
    screenshot_path.write_bytes(image_bytes)
    return screenshot_path
