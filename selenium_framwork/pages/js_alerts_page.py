"""
js_alerts_page.py – Page Object cho TC03.

URL: https://the-internet.herokuapp.com/javascript_alerts

JavaScript Alert có 3 loại:
  1. Alert  – chỉ có nút OK
  2. Confirm – có OK + Cancel
  3. Prompt  – có input text + OK + Cancel

Selenium xử lý alert thông qua driver.switch_to.alert
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from core.logger import get_logger

log = get_logger("js_alerts_page")

# ─── Locators ─────────────────────────────────────────────────────────────────
BTN_ALERT   = (By.XPATH, "//button[text()='Click for JS Alert']")
BTN_CONFIRM = (By.XPATH, "//button[text()='Click for JS Confirm']")
BTN_PROMPT  = (By.XPATH, "//button[text()='Click for JS Prompt']")
TEXT_RESULT = (By.CSS_SELECTOR, "#result")


class JsAlertsPage(BasePage):
    """Thao tác với trang JavaScript Alerts."""

    def open_alerts(self) -> None:
        """Mở trang JS Alerts."""
        self.open("https://the-internet.herokuapp.com/javascript_alerts")

    # ── Alert (chỉ có OK) ─────────────────────────────────────────────────────

    def trigger_and_accept_alert(self) -> str:
        """
        Click nút JS Alert → alert xuất hiện → accept (OK).

        Returns:
            str: text trong alert ('I am a JS Alert')
        """
        log.info("Triggering JS Alert...")
        self.click(BTN_ALERT)
        alert_text = self.accept_alert()   # method từ BasePage
        return alert_text

    # ── Confirm (OK + Cancel) ─────────────────────────────────────────────────

    def trigger_and_dismiss_confirm(self) -> str:
        """
        Click nút JS Confirm → alert xuất hiện → dismiss (Cancel).

        Returns:
            str: text trong alert trước khi dismiss
        """
        log.info("Triggering JS Confirm...")
        self.click(BTN_CONFIRM)
        alert_text = self.dismiss_alert()  # method từ BasePage
        return alert_text

    def trigger_and_accept_confirm(self) -> str:
        """Click nút JS Confirm → accept (OK)."""
        log.info("Triggering JS Confirm (accept)...")
        self.click(BTN_CONFIRM)
        return self.accept_alert()

    # ── Kết quả ───────────────────────────────────────────────────────────────

    def get_result_text(self) -> str:
        """Lấy text hiển thị trong div#result sau khi tương tác alert."""
        text = self.get_text(TEXT_RESULT)
        log.info(f"ALERT HANDLED – Result: '{text}'")
        return text
