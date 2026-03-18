"""
conftest.py – Cấu hình Pytest cho toàn bộ test suite.

Pytest tự động đọc file này ở thư mục gốc project.
Các fixture và hook định nghĩa ở đây có thể dùng trong mọi test file.

Fixture:
  driver  – khởi tạo WebDriver trước mỗi test, quit sau khi xong
  download_dir – trả về path thư mục download để test TC06 verify

Hook:
  pytest_runtest_makereport – chụp screenshot nếu test FAIL
"""

import pytest
from core.driver_factory import get_driver
from core.config import DOWNLOAD_DIR, SCREENSHOT_DIR
from core.logger import get_logger

log = get_logger("conftest")


# ─── Fixture: WebDriver ───────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def driver():
    """
    Khởi tạo Chrome WebDriver trước mỗi test function.
    Sau khi test xong (dù pass hay fail), driver.quit() luôn được gọi.

    scope="function" → mỗi test case có driver riêng (isolation)
    """
    log.info("=" * 60)
    log.info("TEST START")
    _driver = get_driver()
    yield _driver           # trả driver cho test dùng
    _driver.quit()          # cleanup sau yield
    log.info("TEST END")
    log.info("=" * 60)


# ─── Fixture: Download Directory ─────────────────────────────────────────────
@pytest.fixture(scope="session")
def download_dir():
    """Trả về đường dẫn thư mục download để TC06 kiểm tra file."""
    return DOWNLOAD_DIR


# ─── Hook: Screenshot khi Fail ───────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook này được Pytest gọi sau mỗi phase của test (setup / call / teardown).
    Nếu phase 'call' (phần test thực tế) bị FAIL, chụp screenshot.

    Cách hoạt động:
      tryfirst=True  → hook này chạy trước các hook khác
      hookwrapper=True → yield để lấy kết quả sau khi test chạy xong
    """
    outcome = yield  # chờ test chạy xong
    report = outcome.get_result()

    # Chỉ xử lý phase "call" (bản thân test logic), bỏ qua setup/teardown
    if report.when == "call" and report.failed:
        # Lấy driver từ fixture (nếu test có dùng fixture "driver")
        driver = item.funcargs.get("driver")
        if driver is not None:
            test_name = item.name.replace("[", "_").replace("]", "_")
            screenshot_path = f"{SCREENSHOT_DIR}/{test_name}_FAIL.png"
            driver.save_screenshot(screenshot_path)
            log.error(f"TEST FAILED – Screenshot: {screenshot_path}")