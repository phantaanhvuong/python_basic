"""
logger.py – Cấu hình logging cho toàn bộ framework.

Mỗi test step gọi logger.info("...") hoặc logger.error("...")
Log được ghi ra 2 nơi cùng lúc:
  1. Console (stdout) – thấy ngay khi chạy pytest
  2. File  logs/test_run.log – lưu lại lịch sử
"""

import logging
import sys
from core.config import LOG_FILE


def get_logger(name: str = "selenium_test") -> logging.Logger:
    """
    Trả về một Logger đã được cấu hình sẵn.
    Gọi hàm này ở đầu mỗi file test hoặc page object:
        log = get_logger(__name__)
    """
    logger = logging.getLogger(name)

    # Tránh thêm handler trùng nếu hàm được gọi nhiều lần
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # ── Format chung ─────────────────────────────────────────────────────────
    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Handler 1: ghi ra console ─────────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(fmt)

    # ── Handler 2: ghi ra file ────────────────────────────────────────────────
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger