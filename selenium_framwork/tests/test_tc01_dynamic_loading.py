"""
test_tc01_dynamic_loading.py – TC01: Dynamic Loading

Kịch bản:
  1. Mở URL /dynamic_loading/2
  2. Click nút Start
  3. Chờ (Explicit Wait) text xuất hiện
  4. Assert text == "Hello World!"

Điểm học:
  • Explicit Wait không sleep cứng, chỉ poll cho đến khi điều kiện đúng
  • dynamic loading example 2 load element hidden → hiển thị sau click
"""

import pytest
from pages.dynamic_loading_page import DynamicLoadingPage
from core.logger import get_logger

log = get_logger("TC01")

EXPECTED_TEXT = "Hello World!"


class TestDynamicLoading:
    """Test suite cho TC01 – Dynamic Loading."""

    def test_dynamic_load_text(self, driver):
        """
        TC01: Verify text 'Hello World!' xuất hiện sau khi click Start.

        Args:
            driver: WebDriver fixture từ conftest.py
        """
        log.info(">>> TC01 – Dynamic Loading START")

        # ── Khởi tạo Page Object ─────────────────────────────────────────────
        page = DynamicLoadingPage(driver)

        # ── Bước 1: Mở URL ───────────────────────────────────────────────────
        page.open_example()

        # ── Bước 2: Click Start ──────────────────────────────────────────────
        page.click_start()

        # ── Bước 3 + 4: Chờ text và lấy kết quả ─────────────────────────────
        # Đây là điểm quan trọng: get_loaded_text() dùng Explicit Wait
        # nó KHÔNG sleep 5 giây cứng, mà chờ đến khi element visible
        actual_text = page.get_loaded_text()

        # ── Bước 5: Assert ─────────────────────────────────────────────────── 
        assert actual_text == EXPECTED_TEXT, (
            f"Expected '{EXPECTED_TEXT}', got '{actual_text}'"
        )
        log.info(f">>> TC01 PASSED – Text: '{actual_text}'")
