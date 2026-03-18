"""
windows_page.py – Page Object cho TC05.

URL: https://the-internet.herokuapp.com/windows

Khi click "Click Here", trình duyệt mở thêm một tab mới.
Selenium không tự động follow tab mới – phải chủ động switch.

Cơ chế:
  1. Ghi lại handle của tab gốc (original_handle)
  2. Click link → tab mới xuất hiện
  3. Lấy danh sách handles → tìm handle mới
  4. switch_to.window(new_handle)
  5. Thao tác xong → switch lại original_handle
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from core.logger import get_logger

log = get_logger("windows_page")

# ─── Locators ─────────────────────────────────────────────────────────────────
LINK_CLICK_HERE = (By.CSS_SELECTOR, ".example a")
HEADING_NEW_WIN = (By.CSS_SELECTOR, "h3")


class WindowsPage(BasePage):
    """Thao tác với trang Multiple Windows."""

    def __init__(self, driver):
        super().__init__(driver)
        # Lưu handle của tab đầu tiên ngay khi khởi tạo
        self.original_handle = driver.current_window_handle

    def open_windows(self) -> None:
        """Mở trang gốc."""
        self.open("https://the-internet.herokuapp.com/windows")
        # Cập nhật lại original handle (phòng trường hợp navigate)
        self.original_handle = self.driver.current_window_handle

    def click_open_new_window(self) -> None:
        """Click link để mở tab mới."""
        log.info("Clicking to open new window...")
        self.click(LINK_CLICK_HERE)

    def switch_to_new_window(self) -> None:
        """
        Switch sang tab/window mới nhất (tab không phải original).

        Lưu ý: phải gọi sau click_open_new_window().
        """
        all_handles = self.driver.window_handles
        # Tìm handle nào không phải tab gốc
        new_handle = [h for h in all_handles if h != self.original_handle][0]
        self.driver.switch_to.window(new_handle)
        log.info(f"WINDOW SWITCH SUCCESS – Switched to new tab: {new_handle}")

    def get_page_heading(self) -> str:
        """Lấy heading của tab mới ('New Window')."""
        text = self.get_text(HEADING_NEW_WIN)
        log.info(f"New window heading: '{text}'")
        return text

    def switch_back_to_original(self) -> None:
        """Switch trở về tab gốc."""
        self.driver.switch_to.window(self.original_handle)
        log.info("Switched back to original window")
