"""
test_tc03_js_alerts.py – TC03: JavaScript Alert Handling

Kịch bản:
  TC03a – JS Alert:
    1. Click "Click for JS Alert"
    2. Accept alert (OK)
    3. Verify result text = "You successfuly clicked an alert"

  TC03b – JS Confirm:
    4. Click "Click for JS Confirm"
    5. Dismiss (Cancel)
    6. Verify result text = "You clicked: Cancel"

Điểm học:
  • driver.switch_to.alert là cách duy nhất để tương tác JS Alert
  • Alert.text → lấy nội dung
  • Alert.accept() → nhấn OK
  • Alert.dismiss() → nhấn Cancel
"""

import pytest
from pages.js_alerts_page import JsAlertsPage
from core.logger import get_logger

log = get_logger("TC03")


class TestJsAlerts:
    """Test suite cho TC03 – JavaScript Alert Handling."""

    def test_js_alert_accept(self, driver):
        """
        TC03a: Click JS Alert → Accept → verify result.
        """
        log.info(">>> TC03a – JS Alert (accept) START")

        page = JsAlertsPage(driver)
        page.open_alerts()

        # Click nút → alert xuất hiện → accept
        alert_text = page.trigger_and_accept_alert()
        result = page.get_result_text()

        # Sau khi accept, result phải chứa "You successfuly clicked an alert"
        assert "You successfuly clicked an alert" in result, (
            f"Unexpected result: '{result}'"
        )
        log.info(f">>> TC03a PASSED – Alert text: '{alert_text}', Result: '{result}'")

    def test_js_confirm_dismiss(self, driver):
        """
        TC03b: Click JS Confirm → Dismiss (Cancel) → verify result.

        2 test method trong 1 class = chạy tuần tự với driver riêng
        vì scope="function" trong fixture driver
        """
        log.info(">>> TC03b – JS Confirm (dismiss) START")

        page = JsAlertsPage(driver)
        page.open_alerts()

        # Click Confirm → dismiss (Cancel)
        alert_text = page.trigger_and_dismiss_confirm()
        result = page.get_result_text()

        # Khi Cancel → result = "You clicked: Cancel"
        assert "Cancel" in result, f"Expected 'Cancel' in result, got: '{result}'"
        log.info(f">>> TC03b PASSED – Result: '{result}'")
