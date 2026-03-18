"""
iframe_page.py – Page Object cho TC04.

URL: https://the-internet.herokuapp.com/iframe

Trang này nhúng TinyMCE editor trong một iframe.
Để tương tác với nội dung bên trong iframe, driver phải "switch"
vào iframe trước, thao tác xong thì switch lại "default content".

TinyMCE dùng iframe với id="mce_0_ifr", bên trong có body[contenteditable].
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from core.logger import get_logger

log = get_logger("iframe_page")

# ─── Locators ─────────────────────────────────────────────────────────────────
# iframe của TinyMCE editor
IFRAME       = (By.CSS_SELECTOR, "#mce_0_ifr")
# Body editable bên trong iframe
EDITOR_BODY  = (By.CSS_SELECTOR, "body#tinymce")


class IframePage(BasePage):
    """Thao tác với trang iFrame (TinyMCE editor)."""

    def open_iframe(self) -> None:
        """Mở trang iframe."""
        self.open("https://the-internet.herokuapp.com/iframe")

    def switch_to_editor_frame(self) -> None:
        """
        Switch driver vào bên trong iframe của TinyMCE.
        Sau khi gọi hàm này, mọi find/click đều tác động bên trong iframe.
        """
        # Chờ iframe available và tự động switch vào
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(IFRAME))
        log.info("Switched INTO TinyMCE iframe")

    def clear_and_type(self, text: str) -> None:
        """
        Xóa nội dung hiện tại và nhập text mới vào body editor.

        Dùng JavaScript để clear vì TinyMCE không respond tốt với
        element.clear() thông thường.
        """
        body = self.find(EDITOR_BODY)

        # Xóa nội dung bằng JS
        self.driver.execute_script("arguments[0].innerHTML = '';", body)

        # Gõ text mới
        body.send_keys(text)
        log.info(f"IFRAME EDIT SUCCESS – Typed: '{text}'")

    def get_editor_text(self) -> str:
        """Lấy text hiện tại trong editor body."""
        body = self.find(EDITOR_BODY)
        return body.text

    def exit_iframe(self) -> None:
        """Switch trở lại page chính (thoát khỏi iframe)."""
        self.switch_to_default()
