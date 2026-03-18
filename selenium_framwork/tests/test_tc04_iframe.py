"""
test_tc04_iframe.py – TC04: iFrame Interaction

Kịch bản:
  1. Mở URL /iframe
  2. Switch vào TinyMCE iframe
  3. Clear nội dung hiện tại
  4. Nhập text: "Selenium Automation Test"
  5. Verify text trong editor

Điểm học:
  • Không switch vào iframe → KHÔNG tìm thấy element bên trong
  • Sau khi xong phải switch_to.default_content() để dùng lại page bình thường
  • TinyMCE dùng iframe lồng nhau và contenteditable body
"""

import pytest
from pages.iframe_page import IframePage
from core.logger import get_logger

log = get_logger("TC04")

NEW_TEXT = "Selenium Automation Test"


class TestIframe:
    """Test suite cho TC04 – iFrame Interaction."""

    def test_iframe_edit_text(self, driver):
        """
        TC04: Switch vào TinyMCE iframe, xóa text cũ, nhập text mới, verify.

        Args:
            driver: WebDriver fixture từ conftest.py
        """
        log.info(">>> TC04 – iFrame Interaction START")

        page = IframePage(driver)

        # ── Bước 1: Mở URL ───────────────────────────────────────────────────
        page.open_iframe()

        # ── Bước 2: Switch vào iframe ────────────────────────────────────────
        # SAU khi gọi hàm này, driver đang "ở trong" iframe
        # Mọi find/click đều tác động vào DOM của iframe
        page.switch_to_editor_frame()

        # ── Bước 3 + 4: Xóa và nhập text mới ───────────────────────────────
        page.clear_and_type(NEW_TEXT)

        # ── Bước 5: Verify text trong editor ─────────────────────────────────
        actual_text = page.get_editor_text()
        assert NEW_TEXT in actual_text, (
            f"Expected '{NEW_TEXT}' in editor, got: '{actual_text}'"
        )

        # ── Switch lại default content ────────────────────────────────────────
        page.exit_iframe()

        log.info(f">>> TC04 PASSED – Editor text: '{actual_text}'")
