"""
retry.py – Retry decorator cho các thao tác Selenium có thể bị flaky.

Cách dùng:
    from utils.retry import retry

    @retry(times=3, delay=1)
    def click_button():
        page.click(BUTTON)

Khi nào cần dùng?
    • Element chưa kịp xuất hiện trong DOM
    • StaleElementReferenceException (element bị DOM re-render)
    • Timeout ngắn ngủi
"""

import time
import functools
from typing import Callable, Type, Tuple

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException,
)
from core.logger import get_logger

log = get_logger("retry")

# Các exception mặc định sẽ được retry
DEFAULT_EXCEPTIONS: Tuple[Type[Exception], ...] = (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException,
)


def retry(times: int = 3, delay: float = 1.0, exceptions: tuple = DEFAULT_EXCEPTIONS):
    """
    Decorator thực hiện retry khi gặp Selenium exception.

    Args:
        times   : số lần thử tối đa (bao gồm lần đầu)
        delay   : thời gian chờ (giây) giữa mỗi lần thử
        exceptions: tuple các exception class cần retry
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    log.warning(
                        f"[Retry {attempt}/{times}] {func.__name__} failed: {e.__class__.__name__}"
                    )
                    if attempt < times:
                        time.sleep(delay)
            # Hết số lần retry → ném exception cuối cùng
            log.error(f"[Retry] {func.__name__} FAILED after {times} attempts.")
            raise last_exc
        return wrapper
    return decorator
