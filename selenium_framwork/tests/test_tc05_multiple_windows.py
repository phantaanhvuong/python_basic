"""
test_tc05_multiple_windows.py – TC05: Multiple Windows

Kịch bản:
  1. Mở URL /windows
  2. Click "Click Here" → tab mới mở ra
  3. Switch sang tab mới
  4. Verify heading = "New Window"
  5. Switch lại tab cũ

Điểm học:
  • driver.window_handles = danh sách tất cả tab/window handles
  • switch_to.window(handle) để chuyển tab
  • Luôn lưu original_handle trước khi click mở tab mới
"""

import pytest
from pages.windows_page import WindowsPage
from core.logger import get_logger

log = get_logger("TC05")

EXPECTED_HEADING = "New Window"


class TestMultipleWindows:
    """Test suite cho TC05 – Multiple Windows."""

    def test_new_window_and_switch_back(self, driver):
        """
        TC05: Mở tab mới, verify heading, switch lại tab gốc.

        Args:
            driver: WebDriver fixture từ conftest.py
        """
        log.info(">>> TC05 – Multiple Windows START")

        page = WindowsPage(driver)

        # ── Bước 1: Mở URL ───────────────────────────────────────────────────
        page.open_windows()

        # Lưu số tab hiện tại (nên là 1)
        tabs_before = len(driver.window_handles)
        assert tabs_before == 1, f"Expected 1 tab, found {tabs_before}"

        # ── Bước 2: Click mở tab mới ─────────────────────────────────────────
        page.click_open_new_window()

        # ── Bước 3: Switch sang tab mới ──────────────────────────────────────
        page.switch_to_new_window()

        # ── Bước 4: Verify heading ───────────────────────────────────────────
        heading = page.get_page_heading()
        assert EXPECTED_HEADING in heading, (
            f"Expected '{EXPECTED_HEADING}', got: '{heading}'"
        )
        log.info(f"WINDOW SWITCH SUCCESS – Heading: '{heading}'")

        # ── Bước 5: Switch lại tab gốc ──────────────────────────────────────
        page.switch_back_to_original()

        # Verify driver đang ở tab gốc
        assert driver.current_window_handle == page.original_handle
        log.info(">>> TC05 PASSED – Switched back to original window")
