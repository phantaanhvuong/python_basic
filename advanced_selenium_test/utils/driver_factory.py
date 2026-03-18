import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def create_chrome_driver(download_dir=None, headless=False):
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

    prefs = {}
    if download_dir:
        # Đảm bảo đường dẫn tải xuống là tuyệt đối
        download_dir = os.path.abspath(download_dir)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            
        prefs.update({
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        })
    
    if prefs:
        chrome_options.add_experimental_option("prefs", prefs)

    # Sử dụng webdriver-manager để tự động cài đặt ChromeDriver phù hợp
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    
    return driver
