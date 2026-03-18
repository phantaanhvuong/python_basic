# Advanced Selenium Automation Framework

Automation test suite cho **https://the-internet.herokuapp.com** sử dụng:
- **Python 3.x** + **Selenium 4** + **Pytest**
- **Page Object Model (POM)** – mỗi trang web là 1 class riêng
- **Explicit Wait** – không sleep cứng, chờ đến khi điều kiện đúng
- **Logging** – ghi ra console + file `logs/test_run.log`
- **Screenshot on Fail** – tự động chụp ảnh khi test fail
- **Retry Mechanism** – `@retry` decorator cho element flaky
- **Headless Mode** – chạy không mở cửa sổ Chrome
- **Parallel Execution** – dùng `pytest-xdist`

---

## Cấu trúc thư mục

```
selenium_framwork/
├── conftest.py              # Fixtures + screenshot hook
├── pytest.ini               # Cấu hình Pytest
├── repuirements.txt         # Dependencies
│
├── core/
│   ├── config.py            # Cấu hình chung (URL, timeout, paths)
│   ├── driver_factory.py    # Khởi tạo WebDriver
│   └── logger.py            # Logging ra console + file
│
├── pages/                   # Page Object Model
│   ├── base_page.py         # Lớp cơ sở (find, click, alert, iframe...)
│   ├── dynamic_loading_page.py
│   ├── upload_page.py
│   ├── js_alerts_page.py
│   ├── iframe_page.py
│   ├── windows_page.py
│   └── download_page.py
│
├── tests/                   # Test Cases
│   ├── test_tc01_dynamic_loading.py
│   ├── test_tc02_file_upload.py
│   ├── test_tc03_js_alerts.py
│   ├── test_tc04_iframe.py
│   ├── test_tc05_multiple_windows.py
│   └── test_tc06_file_download.py
│
├── utils/
│   ├── retry.py             # @retry decorator
│   └── file_utils.py        # Chờ file download
│
├── data/
│   └── test_upload.txt      # File dùng cho TC02
│
├── downloads/               # Thư mục lưu file tải về (TC06) [tự tạo]
├── logs/                    # Log file [tự tạo]
│   └── test_run.log
└── reports/                 # HTML report + screenshots [tự tạo]
    ├── report.html
    └── screenshots/
```

---

## Cài đặt

```bash
# Vào thư mục project
cd d:\python_basic\selenium_framwork

# Cài dependencies
pip install -r repuirements.txt
```

---

## Chạy Test

### Chạy tất cả test (bình thường)
```bash
pytest tests/ -v
```

### Chạy 1 test case cụ thể
```bash
pytest tests/test_tc01_dynamic_loading.py -v
pytest tests/test_tc02_file_upload.py -v
pytest tests/test_tc03_js_alerts.py -v
pytest tests/test_tc04_iframe.py -v
pytest tests/test_tc05_multiple_windows.py -v
pytest tests/test_tc06_file_download.py -v
```

### Chạy Headless (không mở Chrome UI)
Mở `core/config.py`, đổi:
```python
HEADLESS = True
```
Rồi chạy bình thường:
```bash
pytest tests/ -v
```

### Chạy song song (4 worker)
```bash
pytest tests/ -n 4 -v
```

> ⚠️ Lưu ý: TC06 (download) nên chạy riêng khi dùng parallel để tránh conflict thư mục download.

---

## Xem kết quả

| Output | Vị trí |
|---|---|
| HTML Report | `reports/report.html` |
| Log file | `logs/test_run.log` |
| Screenshot khi fail | `reports/screenshots/*.png` |
| File đã tải về | `downloads/` |

---

## Test Cases

| TC | Tên | URL | Kỹ thuật chính |
|---|---|---|---|
| TC01 | Dynamic Loading | /dynamic_loading/2 | Explicit Wait, visibility_of |
| TC02 | File Upload | /upload | send_keys(path) vào input[type=file] |
| TC03 | JS Alert | /javascript_alerts | switch_to.alert, accept/dismiss |
| TC04 | iFrame | /iframe | switch_to.frame, JS innerHTML |
| TC05 | Multiple Windows | /windows | window_handles, switch_to.window |
| TC06 | File Download | /download | Chrome prefs, poll file existence |

---

## Bonus Features

### 1. Retry Decorator
```python
from utils.retry import retry

@retry(times=3, delay=1)
def click_flaky_button():
    page.click(BUTTON)
```

### 2. Headless Mode
```python
# core/config.py
HEADLESS = True
```

### 3. Parallel Execution
```bash
pytest tests/ -n auto -v   # dùng số CPU tự động
pytest tests/ -n 4 -v      # 4 workers
```

### 4. Page Object Model
Mọi page đều kế thừa `BasePage`:
```python
class DynamicLoadingPage(BasePage):
    def click_start(self):
        self.click(BTN_START)  # dùng method của BasePage
```
