"""
driver_factory.py – Tạo và cấu hình WebDriver.

Tính năng:
  • Hỗ trợ headless mode (HEADLESS = True trong config)
  • Cấu hình thư mục tải file tự động (không hỏi "lưu ở đâu?")
  • Dùng webdriver-manager để tự tải chromedriver đúng phiên bản
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from core.config import BROWSER, HEADLESS, DOWNLOAD_DIR


def get_driver() -> webdriver.Chrome:
    """
    Khởi tạo và trả về WebDriver theo cấu hình trong config.py.

    Returns:
        webdriver.Chrome: instance WebDriver đã cấu hình sẵn
    """
    if BROWSER.lower() == "chrome":
        options = Options()

        # ── Giao diện ───────────────────────────────────────────────────────
        options.add_argument("--start-maximized")

        if HEADLESS:
            # Chạy không có UI – phù hợp CI/CD hoặc chạy nền
            options.add_argument("--headless=new")   # Chrome ≥ 112
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")

        # ── Bỏ các thông báo "Chrome is being controlled by automation" ──────
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # ── Cấu hình thư mục tải file (TC06) ────────────────────────────────
        # Chrome sẽ tự động lưu file vào DOWNLOAD_DIR mà không hỏi
        prefs = {
            "download.default_directory": DOWNLOAD_DIR,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        options.add_experimental_option("prefs", prefs)

        # ── Khởi tạo driver – webdriver-manager tự tải chromedriver ─────────
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    raise ValueError(f"Browser '{BROWSER}' chưa được hỗ trợ.")