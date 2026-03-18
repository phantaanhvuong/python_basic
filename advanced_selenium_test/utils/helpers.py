import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

def ensure_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def take_screenshot(driver, screenshot_dir, test_name):
    ensure_folder(screenshot_dir)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_name = f"{test_name}_{timestamp}.png"
    screenshot_path = os.path.join(screenshot_dir, screenshot_name)
    driver.save_screenshot(screenshot_path)
    return screenshot_path

def wait_for_element_visible(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )

def wait_for_element_clickable(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )

def wait_for_text_present(driver, locator, text, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element(locator, text)
    )

def retry_find_element(driver, locator, retries=3, timeout=5):
    attempt = 0
    while attempt < retries:
        try:
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except (TimeoutException, StaleElementReferenceException):
            attempt += 1
            time.sleep(1)
    raise TimeoutException(f"Could not find element {locator} after {retries} retries.")

def wait_for_file_download(download_dir, timeout=30):
    start_time = time.time()
    
    # ensure dir exists before tracking files
    ensure_folder(download_dir)
    initial_files = set(os.listdir(download_dir))
    
    while time.time() - start_time < timeout:
        current_files = set(os.listdir(download_dir))
        new_files = current_files - initial_files
        
        # Check if the new file is fully downloaded (not a temporary .crdownload file)
        for f in new_files:
            if not f.endswith('.crdownload') and not f.endswith('.tmp'):
                return f
        time.sleep(1)
        
    raise Exception("File download timed out.")
