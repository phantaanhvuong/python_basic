"""
test_tc06_file_download.py – TC06: File Download Verification

Kịch bản:
  1. Mở URL /download
  2. Click file đầu tiên
  3. Chờ file tải về (poll thư mục downloads/)
  4. Assert file tồn tại và size > 0

Điểm học:
  • Chrome download tự động → không có dialog "Lưu ở đâu?"
  • Cần cấu hình prefs trong driver_factory trỏ đến DOWNLOAD_DIR
  • Phải CHỜ file hoàn tất (check .crdownload biến mất)
"""

import pytest
from pages.download_page import DownloadPage
from utils.file_utils import file_exists
from core.logger import get_logger

log = get_logger("TC06")


class TestFileDownload:
    """Test suite cho TC06 – File Download."""

    def test_file_download_success(self, driver, download_dir):
        """
        TC06: Click download file → verify file tồn tại trong thư mục.

        Args:
            driver       : WebDriver fixture từ conftest.py
            download_dir : đường dẫn thư mục download từ conftest.py
        """
        log.info(">>> TC06 – File Download START")
        log.info(f"Download dir: {download_dir}")

        page = DownloadPage(driver)

        # ── Bước 1: Mở URL ───────────────────────────────────────────────────
        page.open_download()

        # Lấy tên file sẽ tải (để log)
        filename = page.get_first_file_name()
        log.info(f"Target file: '{filename}'")

        # ── Bước 2: Click download ───────────────────────────────────────────
        page.click_first_file()

        # ── Bước 3: Chờ file xuất hiện ──────────────────────────────────────
        # wait_and_verify_download() poll mỗi 0.5s, timeout 20s
        downloaded_path = page.wait_and_verify_download(timeout=20)

        # ── Bước 4: Assert file tồn tại và không rỗng ───────────────────────
        assert file_exists(downloaded_path), (
            f"File không tồn tại hoặc rỗng: {downloaded_path}"
        )
        log.info(f">>> TC06 PASSED – FILE DOWNLOADED: {downloaded_path}")
