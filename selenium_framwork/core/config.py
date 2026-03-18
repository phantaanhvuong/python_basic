import os

# ─── URL gốc của website cần test ─────────────────────────────────────────────
BASE_URL = "https://the-internet.herokuapp.com"

# ─── Trình duyệt (chỉ hỗ trợ chrome hiện tại) ────────────────────────────────
BROWSER = "chrome"

# ─── Thời gian chờ tối đa (giây) cho Explicit Wait ───────────────────────────
TIMEOUT = 15

# ─── Bật / tắt chế độ headless (chạy không có cửa sổ trình duyệt) ─────────────
# True  → chạy nền (không mở Chrome UI)
# False → mở Chrome bình thường để quan sát
HEADLESS = False

# ─── Thư mục lưu file tải về (TC06) ──────────────────────────────────────────
# os.path.abspath đảm bảo đường dẫn tuyệt đối dù chạy từ thư mục nào
DOWNLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "downloads"))

# ─── Thư mục lưu screenshot khi test fail ─────────────────────────────────────
SCREENSHOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots"))

# ─── Đường dẫn file log ───────────────────────────────────────────────────────
LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "test_run.log"))

# ─── Tạo các thư mục nếu chưa tồn tại ────────────────────────────────────────
for _dir in [DOWNLOAD_DIR, SCREENSHOT_DIR, os.path.dirname(LOG_FILE)]:
    os.makedirs(_dir, exist_ok=True)