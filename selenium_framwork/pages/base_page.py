"""
base_page.py – Lớp cơ sở cho tất cả Page Objects.

Mọi page class đều kế thừa BasePage và dùng lại các method:
  • find / click / type / get_text / is_visible   → Explicit Wait
  • take_screenshot                                → chụp màn hình
  • switch_to_frame / switch_to_default           → iframe
  • accept_alert / dismiss_alert / get_alert_text → JS Alert
"""

import os
import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from core.config import TIMEOUT, SCREENSHOT_DIR
from core.logger import get_logger

log = get_logger("base_page")


class BasePage:
    """Lớp base cho Page Object Model."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        # WebDriverWait dùng chung cho toàn page, timeout lấy từ config
        self.wait = WebDriverWait(driver, TIMEOUT)

    # ─── Navigation ─────────────────────────────────────────────────────────

    def open(self, url: str) -> None:
        """Mở URL trong trình duyệt."""
        log.info(f"OPEN URL: {url}")
        self.driver.get(url)

    # ─── Element Interactions ────────────────────────────────────────────────

    def find(self, locator: tuple) -> WebElement:
        """Chờ element xuất hiện trong DOM và trả về element đó."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator: tuple) -> None:
        """Chờ element có thể click và click vào."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator: tuple, text: str) -> None:
        """Tìm input element, xóa nội dung cũ và nhập text mới."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """Lấy text hiển thị của element."""
        return self.find(locator).text

    def is_visible(self, locator: tuple) -> WebElement:
        """Chờ element visible trên màn hình."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    # ─── Screenshot ──────────────────────────────────────────────────────────

    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Chụp màn hình và lưu vào SCREENSHOT_DIR.

        Args:
            name: tên file (không cần đuôi .png)

        Returns:
            str: đường dẫn tới file ảnh đã lưu
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(path)
        log.info(f"Screenshot saved: {path}")
        return path

    # ─── iFrame ──────────────────────────────────────────────────────────────

    def switch_to_frame(self, locator: tuple) -> None:
        """
        Switch driver vào bên trong iframe.
        Dùng khi cần tương tác với nội dung trong iframe (TC04).
        """
        frame = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.switch_to.frame(frame)
        log.debug("Switched INTO iframe")

    def switch_to_frame_by_id(self, frame_id: str) -> None:
        """Switch vào iframe theo id hoặc name."""
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(frame_id))
        log.debug(f"Switched into frame: {frame_id}")

    def switch_to_default(self) -> None:
        """Switch trở lại nội dung chính (thoát khỏi iframe)."""
        self.driver.switch_to.default_content()
        log.debug("Switched back to default content")

    # ─── JavaScript Alert ────────────────────────────────────────────────────

    def get_alert_text(self) -> str:
        """Chờ alert xuất hiện và lấy text của alert."""
        alert: Alert = self.wait.until(EC.alert_is_present())
        return alert.text

    def accept_alert(self) -> str:
        """
        Chờ alert → lấy text → nhấn OK.

        Returns:
            str: text của alert trước khi accept
        """
        alert: Alert = self.wait.until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        log.info(f"ALERT ACCEPTED: '{text}'")
        return text

    def dismiss_alert(self) -> str:
        """
        Chờ alert → lấy text → nhấn Cancel.

        Returns:
            str: text của alert trước khi dismiss
        """
        alert: Alert = self.wait.until(EC.alert_is_present())
        text = alert.text
        alert.dismiss()
        log.info(f"ALERT DISMISSED: '{text}'")
        return text

    # ─── Windows / Tabs ──────────────────────────────────────────────────────

    def get_window_handles(self) -> list:
        """Trả về danh sách handle của tất cả tab/window đang mở."""
        return self.driver.window_handles

    def switch_to_window(self, handle: str) -> None:
        """Switch sang tab/window theo handle."""
        self.driver.switch_to.window(handle)
        log.debug(f"Switched to window: {handle}")