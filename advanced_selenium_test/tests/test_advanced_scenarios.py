import os
import sys
import pytest

# Cho phép import utils khi chạy từ root project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.driver_factory import create_chrome_driver
from utils.logger import setup_logger
from utils.helpers import (
    ensure_folder,
    take_screenshot,
    wait_for_element_visible,
    wait_for_element_clickable,
    wait_for_text_present,
    retry_find_element,
    wait_for_file_download
)

BASE_URL = "https://the-internet.herokuapp.com"
DOWNLOAD_DIR = os.path.abspath("downloads")
SCREENSHOT_DIR = os.path.abspath("screenshots")
RESOURCE_DIR = os.path.abspath("resources")

logger = setup_logger()


class TestAdvancedSeleniumAutomation:

    @classmethod
    def setup_class(cls):
        ensure_folder(DOWNLOAD_DIR)
        ensure_folder(SCREENSHOT_DIR)
        cls.driver = create_chrome_driver(download_dir=DOWNLOAD_DIR, headless=False)
        cls.wait = WebDriverWait(cls.driver, 10)
        logger.info("TEST START")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
        logger.info("TEST FINISHED")

    def safe_open(self, url):
        logger.info(f"OPEN URL: {url}")
        self.driver.get(url)

    def handle_failure(self, test_name, exception):
        screenshot_path = take_screenshot(self.driver, SCREENSHOT_DIR, test_name)
        logger.error(f"{test_name} FAILED: {exception}")
        logger.error(f"Screenshot saved: {screenshot_path}")
        pytest.fail(f"{test_name} FAILED: {exception}")

    def test_tc01_dynamic_loading(self):
        """
        TC01 – Dynamic Loading Test
        Expected: Hello World!
        """
        test_name = "TC01_dynamic_loading"

        try:
            self.safe_open(f"{BASE_URL}/dynamic_loading/2")

            start_btn = wait_for_element_clickable(
                self.driver,
                (By.CSS_SELECTOR, "#start button"),
                timeout=10
            )
            start_btn.click()

            hello_text = wait_for_element_visible(
                self.driver,
                (By.CSS_SELECTOR, "#finish h4"),
                timeout=15
            )

            assert hello_text.text.strip() == "Hello World!"
            logger.info("DYNAMIC LOAD SUCCESS")
            logger.info("TEST PASSED")

        except Exception as e:
            self.handle_failure(test_name, e)

    def test_tc02_file_upload(self):
        """
        TC02 – File Upload
        Expected: File Uploaded!
        """
        test_name = "TC02_file_upload"

        try:
            self.safe_open(f"{BASE_URL}/upload")

            file_input = wait_for_element_visible(
                self.driver,
                (By.CSS_SELECTOR, "input[type='file']"),
                timeout=10
            )

            upload_file_path = os.path.join(RESOURCE_DIR, "sample_upload.txt")
            file_input.send_keys(upload_file_path)

            upload_btn = wait_for_element_clickable(
                self.driver,
                (By.CSS_SELECTOR, "#file-submit"),
                timeout=10
            )
            upload_btn.click()

            uploaded_msg = wait_for_element_visible(
                self.driver,
                (By.CSS_SELECTOR, "div.example h3"),
                timeout=10
            )

            assert uploaded_msg.text.strip() == "File Uploaded!"
            logger.info("UPLOAD SUCCESS")
            logger.info("TEST PASSED")

        except Exception as e:
            self.handle_failure(test_name, e)

    def test_tc03_javascript_alert_handling(self):
        """
        TC03 – JavaScript Alert Handling
        - JS Alert -> Accept
        - JS Confirm -> Cancel
        """
        test_name = "TC03_javascript_alerts"

        try:
            self.safe_open(f"{BASE_URL}/javascript_alerts")

            # Part 1: JS Alert
            alert_btn = wait_for_element_clickable(
                self.driver,
                (By.XPATH, "//button[text()='Click for JS Alert']"),
                timeout=10
            )
            alert_btn.click()

            alert = self.wait.until(EC.alert_is_present())
            alert.accept()

            result = wait_for_element_visible(
                self.driver,
                (By.CSS_SELECTOR, "#result"),
                timeout=10
            )
            assert result.text.strip() == "You successfully clicked an alert"

            # Part 2: JS Confirm -> Cancel
            confirm_btn = wait_for_element_clickable(
                self.driver,
                (By.XPATH, "//button[text()='Click for JS Confirm']"),
                timeout=10
            )
            confirm_btn.click()

            confirm_alert = self.wait.until(EC.alert_is_present())
            confirm_alert.dismiss()

            result = wait_for_element_visible(
                self.driver,
                (By.CSS_SELECTOR, "#result"),
                timeout=10
            )
            assert result.text.strip() == "You clicked: Cancel"

            logger.info("ALERT HANDLED")
            logger.info("TEST PASSED")

        except Exception as e:
            self.handle_failure(test_name, e)

    def test_tc04_iframe_interaction(self):
        """
        TC04 – iFrame Interaction
        Expected text: Selenium Automation Test
        """
        test_name = "TC04_iframe_interaction"

        try:
            self.safe_open(f"{BASE_URL}/iframe")

            # Switch vào iframe bằng Expected Condition
            self.wait.until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe"))
            )

            editor = wait_for_element_visible(
                self.driver,
                (By.CSS_SELECTOR, "body#tinymce"),
                timeout=10
            )

            # TinyMCE thường chặn các phím hoặc gặp lỗi InvalidElementStateException với .clear()
            # Dùng JavaScript để ép nội dung văn bản vào trực tiếp thân iFrame.
            self.driver.execute_script("arguments[0].innerHTML = '<p>Selenium Automation Test</p>';", editor)

            assert "Selenium Automation Test" in editor.text

            self.driver.switch_to.default_content()

            logger.info("IFRAME EDIT SUCCESS")
            logger.info("TEST PASSED")

        except Exception as e:
            self.handle_failure(test_name, e)

    def test_tc05_multiple_windows(self):
        """
        TC05 – Multiple Windows
        Expected: New Window
        """
        test_name = "TC05_multiple_windows"

        try:
            self.safe_open(f"{BASE_URL}/windows")

            main_window = self.driver.current_window_handle

            click_here = wait_for_element_clickable(
                self.driver,
                (By.LINK_TEXT, "Click Here"),
                timeout=10
            )
            click_here.click()

            self.wait.until(lambda d: len(d.window_handles) == 2)

            for handle in self.driver.window_handles:
                if handle != main_window:
                    self.driver.switch_to.window(handle)
                    break

            new_window_text = wait_for_element_visible(
                self.driver,
                (By.CSS_SELECTOR, "div.example h3"),
                timeout=10
            )

            assert new_window_text.text.strip() == "New Window"

            self.driver.close()
            self.driver.switch_to.window(main_window)

            logger.info("WINDOW SWITCH SUCCESS")
            logger.info("TEST PASSED")

        except Exception as e:
            self.handle_failure(test_name, e)

    def test_tc06_file_download_verification(self):
        """
        TC06 – File Download
        Expected: file được tải về thư mục download
        """
        test_name = "TC06_file_download"

        try:
            # Dọn thư mục download trước khi test
            for f in os.listdir(DOWNLOAD_DIR):
                file_path = os.path.join(DOWNLOAD_DIR, f)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            self.safe_open(f"{BASE_URL}/download")

            # Click download file đầu tiên
            first_file_link = wait_for_element_clickable(
                self.driver,
                (By.CSS_SELECTOR, "div.example a"),
                timeout=10
            )
            expected_file_name = first_file_link.text.strip()
            first_file_link.click()

            downloaded_file = wait_for_file_download(DOWNLOAD_DIR, timeout=25)

            downloaded_path = os.path.join(DOWNLOAD_DIR, downloaded_file)
            assert os.path.exists(downloaded_path)
            assert downloaded_file == expected_file_name

            logger.info("FILE DOWNLOADED")
            logger.info("TEST PASSED")

        except Exception as e:
            self.handle_failure(test_name, e)