"""
dynamic_loading_page.py – Page Object cho TC01.

URL: https://the-internet.herokuapp.com/dynamic_loading/2

Trang này có một nút "Start". Khi click, nội dung sẽ load
động sau một khoảng thời gian. Script phải CHỜ (Explicit Wait)
cho đến khi text "Hello World!" hiển thị.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from core.logger import get_logger

log = get_logger("dynamic_loading_page")

# ─── Locators – dùng CSS Selector ────────────────────────────────────────────
# Nút Start trên trang
BTN_START = (By.CSS_SELECTOR, "#start button")

# Đoạn text xuất hiện sau khi load xong (nằm trong div#finish)
TEXT_FINISH = (By.CSS_SELECTOR, "#finish h4")


class DynamicLoadingPage(BasePage):
    """Thao tác với trang Dynamic Loading."""

    def open_example(self) -> None:
        """Mở trang dynamic loading example 2."""
        self.open("https://the-internet.herokuapp.com/dynamic_loading/2")

    def click_start(self) -> None:
        """Click nút Start để bắt đầu quá trình load động."""
        log.info("Clicking START button...")
        self.click(BTN_START)

    def get_loaded_text(self) -> str:
        """
        CHỜ cho đến khi #finish h4 visible rồi lấy text.

        Đây là Explicit Wait: script không sleep cứng,
        mà chờ đến khi điều kiện visibility_of_element_located thỏa mãn.
        Timeout lấy từ config.py (mặc định 15 giây).
        """
        log.info("Waiting for dynamic content to appear...")
        element = self.wait.until(EC.visibility_of_element_located(TEXT_FINISH))
        text = element.text
        log.info(f"DYNAMIC LOAD SUCCESS – Text: '{text}'")
        return text
