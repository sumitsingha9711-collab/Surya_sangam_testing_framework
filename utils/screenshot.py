"""Screenshot utility for failed tests."""

from datetime import datetime
from pathlib import Path


SCREENSHOT_DIR = Path(__file__).resolve().parents[1] / "screenshots"


def capture_screenshot(driver, test_name):
    """Capture a timestamped screenshot and return its path."""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_test_name = test_name.replace("/", "_").replace("\\", "_")
    screenshot_path = SCREENSHOT_DIR / f"{safe_test_name}_{timestamp}.png"
    driver.save_screenshot(str(screenshot_path))
    return screenshot_path
