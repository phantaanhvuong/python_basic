"""
test_tc02_file_upload.py – TC02: File Upload

Kịch bản:
  1. Mở URL /upload
  2. Chọn file từ máy (send_keys path vào input[type=file])
  3. Click Upload
  4. Assert heading hiển thị "File Uploaded!"

Điểm học:
  • Không cần dialog "chọn file" – gởi path trực tiếp vào input
  • File phải tồn tại trên máy trước khi upload
"""

import os
import pytest
from pages.upload_page import UploadPage
from core.logger import get_logger

log = get_logger("TC02")

# Đường dẫn tới file test (tương đối từ thư mục gốc project)
UPLOAD_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "test_upload.txt")
)
EXPECTED_HEADING = "File Uploaded!"


class TestFileUpload:
    """Test suite cho TC02 – File Upload."""

    def test_file_upload_success(self, driver):
        """
        TC02: Verify 'File Uploaded!' xuất hiện sau khi chọn và upload file.

        Args:
            driver: WebDriver fixture từ conftest.py
        """
        log.info(">>> TC02 – File Upload START")

        # ── Kiểm tra file tồn tại trước khi upload ───────────────────────────
        assert os.path.isfile(UPLOAD_FILE), f"File không tồn tại: {UPLOAD_FILE}"

        # ── Khởi tạo Page Object ─────────────────────────────────────────────
        page = UploadPage(driver)

        # ── Bước 1: Mở URL ───────────────────────────────────────────────────
        page.open_upload()

        # ── Bước 2 + 3: Chọn file + Click Upload ────────────────────────────
        page.upload_file(UPLOAD_FILE)

        # ── Bước 4: Verify ───────────────────────────────────────────────────
        heading = page.get_result_heading()
        uploaded_name = page.get_uploaded_filename()

        assert heading == EXPECTED_HEADING, (
            f"Expected '{EXPECTED_HEADING}', got '{heading}'"
        )
        log.info(f">>> TC02 PASSED – Uploaded: '{uploaded_name}'")
