"""
upload_page.py – Page Object cho TC02.

URL: https://the-internet.herokuapp.com/upload

Để upload file với Selenium:
  • KHÔNG cần click nút "Choose File" rồi dùng dialog
  • Chỉ cần send_keys(full_path) vào input[type=file]
  • Selenium tự xử lý việc chọn file
"""

import os
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from core.logger import get_logger

log = get_logger("upload_page")

# ─── Locators ─────────────────────────────────────────────────────────────────
# Input cho phép chọn file (type="file")
INPUT_FILE   = (By.CSS_SELECTOR, "#file-upload")
# Nút submit upload
BTN_SUBMIT   = (By.CSS_SELECTOR, "#file-submit")
# Text kết quả sau khi upload thành công
TEXT_RESULT  = (By.CSS_SELECTOR, "#uploaded-files")
# Heading xác nhận upload thành công
HEADING      = (By.CSS_SELECTOR, "h3")


class UploadPage(BasePage):
    """Thao tác với trang File Upload."""

    def open_upload(self) -> None:
        """Mở trang upload."""
        self.open("https://the-internet.herokuapp.com/upload")

    def upload_file(self, filepath: str) -> None:
        """
        Upload file bằng cách send absolute path vào input[type=file].

        Args:
            filepath: đường dẫn tuyệt đối đến file cần upload.
                      Dùng os.path.abspath() để chắc chắn.
        """
        abs_path = os.path.abspath(filepath)
        log.info(f"Uploading file: {abs_path}")

        # Gởi đường dẫn file vào input – Selenium sẽ tự điền
        file_input = self.find(INPUT_FILE)
        file_input.send_keys(abs_path)

        log.info("Clicking Upload button...")
        self.click(BTN_SUBMIT)

    def get_result_heading(self) -> str:
        """Lấy text của heading sau khi upload ('File Uploaded!')."""
        text = self.get_text(HEADING)
        log.info(f"UPLOAD SUCCESS – Heading: '{text}'")
        return text

    def get_uploaded_filename(self) -> str:
        """Lấy tên file vừa upload hiển thị trên trang."""
        return self.get_text(TEXT_RESULT)
