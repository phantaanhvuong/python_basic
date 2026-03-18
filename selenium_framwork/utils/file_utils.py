"""
file_utils.py – Tiện ích kiểm tra file tải về (TC06).

Hàm wait_for_file() poll liên tục cho đến khi:
  • File xuất hiện trong thư mục downloads/
  • Hoặc hết timeout → raise TimeoutError
"""

import os
import time


def wait_for_file(directory: str, timeout: int = 20) -> str:
    """
    Chờ cho đến khi xuất hiện file mới trong `directory`.

    Lưu ý: hàm này snapshot danh sách file TRƯỚC khi tải,
    sau đó chờ file mới xuất hiện.

    Args:
        directory : đường dẫn thư mục (thường là DOWNLOAD_DIR)
        timeout   : thời gian chờ tối đa (giây)

    Returns:
        str: đường dẫn tuyệt đối đến file vừa tải

    Raises:
        TimeoutError: nếu không thấy file trong khoảng timeout
    """
    # Snapshot danh sách file hiện có trước khi click download
    before = set(os.listdir(directory)) if os.path.exists(directory) else set()

    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(0.5)
        if not os.path.exists(directory):
            continue
        current = set(os.listdir(directory))
        new_files = current - before
        # Bỏ qua file .crdownload (Chrome đang tải dở)
        completed = [f for f in new_files if not f.endswith(".crdownload")]
        if completed:
            return os.path.join(directory, completed[0])

    raise TimeoutError(
        f"Không tìm thấy file mới trong '{directory}' sau {timeout}s"
    )


def file_exists(path: str) -> bool:
    """Kiểm tra file có tồn tại và có kích thước > 0."""
    return os.path.isfile(path) and os.path.getsize(path) > 0
