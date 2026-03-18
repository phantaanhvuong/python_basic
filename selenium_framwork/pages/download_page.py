"""
download_page.py – Page Object cho TC06.

URL: https://the-internet.herokuapp.com/download

Trang hiển thị danh sách file để tải về.
Script sẽ:
  1. Lấy tên file đầu tiên trong list
  2. Click để tải
  3. Gọi wait_for_file() để chờ file xuất hiện trong DOWNLOAD_DIR
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from core.config import DOWNLOAD_DIR
from utils.file_utils import wait_for_file
from core.logger import get_logger

log = get_logger("download_page")

# ─── Locators ─────────────────────────────────────────────────────────────────
# Tất cả link trong khu vực download
ALL_LINKS    = (By.CSS_SELECTOR, "#content .example a")
# Link đầu tiên (dùng nth-child)
FIRST_LINK   = (By.CSS_SELECTOR, "#content .example a:first-child")


class DownloadPage(BasePage):
    """Thao tác với trang File Download."""

    def open_download(self) -> None:
        """Mở trang download."""
        self.open("https://the-internet.herokuapp.com/download")

    def get_first_file_name(self) -> str:
        """Lấy tên file đầu tiên hiển thị trong danh sách."""
        return self.find(FIRST_LINK).text

    def click_first_file(self) -> None:
        """Click link file đầu tiên để bắt đầu download."""
        filename = self.get_first_file_name()
        log.info(f"Clicking to download: '{filename}'")
        self.click(FIRST_LINK)

    def wait_and_verify_download(self, timeout: int = 20) -> str:
        """
        Chờ file xuất hiện trong DOWNLOAD_DIR.

        Args:
            timeout: thời gian chờ tối đa (giây)

        Returns:
            str: đường dẫn tuyệt đối đến file đã tải

        Raises:
            TimeoutError: nếu file không xuất hiện
        """
        log.info(f"Waiting for file in: {DOWNLOAD_DIR}")
        filepath = wait_for_file(DOWNLOAD_DIR, timeout=timeout)
        log.info(f"FILE DOWNLOADED: {filepath}")
        return filepath
