import time
import requests
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


SAUCEDEMO_URL = "https://www.saucedemo.com/"
GOOGLE_TRANSLATE_URL = "https://translate.google.com/?sl=auto&tl=vi&op=translate"

USERNAME = "standard_user"
PASSWORD = "secret_sauce"

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

TXT_FILE = OUTPUT_DIR / "translated_content.txt"
IMG_FILE = OUTPUT_DIR / "product_image.jpg"


def log(message):
    print(f"[LOG] {message}")


def save_text_file(file_path, content):
    file_path.write_text(content, encoding="utf-8")
    log(f"Đã lưu file txt: {file_path.resolve()}")


def download_image(image_url, file_path):
    response = requests.get(image_url, timeout=30)
    response.raise_for_status()
    file_path.write_bytes(response.content)
    log(f"Đã tải ảnh về: {file_path.resolve()}")


def get_inventory_text(driver, wait):
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

    title = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    ).text.strip()

    item_names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    item_descs = driver.find_elements(By.CLASS_NAME, "inventory_item_desc")

    names = [item.text.strip() for item in item_names if item.text.strip()]
    descs = [item.text.strip() for item in item_descs if item.text.strip()]

    content = []
    content.append(f"Page title: {title}")
    content.append("")
    content.append("Product names:")
    for i, name in enumerate(names, start=1):
        content.append(f"{i}. {name}")

    content.append("")
    content.append("Product descriptions:")
    for i, desc in enumerate(descs, start=1):
        content.append(f"{i}. {desc}")

    full_text = "\n".join(content)
    assert len(full_text) > 0, "Không lấy được nội dung trang sau khi login"
    return full_text


def translate_text_with_google(driver, wait, text_to_translate):
    log("Mở Google Dịch...")
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(GOOGLE_TRANSLATE_URL)

    wait.until(lambda d: "translate.google" in d.current_url)

    input_box = None
    input_locators = [
        (By.XPATH, "//textarea[@aria-label='Source text']"),
        (By.XPATH, "//textarea"),
        (By.XPATH, "//div[@contenteditable='true']"),
    ]

    for by, locator in input_locators:
        try:
            input_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((by, locator))
            )
            if input_box:
                break
        except TimeoutException:
            continue

    assert input_box is not None, "Không tìm thấy ô nhập của Google Dịch"

    input_box.click()
    try:
        input_box.clear()
    except Exception:
        pass

    input_box.send_keys(Keys.CONTROL, "a")
    input_box.send_keys(Keys.DELETE)
    input_box.send_keys(text_to_translate)

    log("Đang chờ kết quả dịch...")

    translated_text = ""
    end_time = time.time() + 30

    while time.time() < end_time:
        candidates = driver.find_elements(By.XPATH, "//span[@lang='vi']")
        texts = [x.text.strip() for x in candidates if x.text.strip()]
        if texts:
            translated_text = " ".join(dict.fromkeys(texts)).strip()
            if translated_text and translated_text != text_to_translate.strip():
                break
        time.sleep(1)

    assert translated_text, "Không lấy được nội dung dịch từ Google Dịch"
    return translated_text


def get_first_product_image_url(driver, wait):
    driver.switch_to.window(driver.window_handles[0])
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))

    img = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".inventory_item img"))
    )
    img_src = img.get_attribute("src")

    assert img_src and img_src.startswith("http"), "Không lấy được link ảnh"
    return img_src


def logout_saucedemo(driver, wait):
    log("Đăng xuất...")

    menu_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    )
    menu_btn.click()

    logout_link = wait.until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    )
    logout_link.click()

    wait.until(EC.visibility_of_element_located((By.ID, "login-button")))
    assert "saucedemo" in driver.current_url.lower(), "Không quay về trang login"
    log("Logout thành công")


def main():
    log("Khởi tạo trình duyệt...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    wait = WebDriverWait(driver, 20)

    try:
        # Bước 1: Mở SauceDemo
        log("Mở SauceDemo...")
        driver.get(SAUCEDEMO_URL)

        wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
        assert "saucedemo" in driver.current_url.lower(), "Không mở được trang login"

        # Bước 2: Login
        log("Đăng nhập...")
        driver.find_element(By.ID, "user-name").send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login-button").click()

        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title")))
        assert "inventory" in driver.current_url.lower(), "Đăng nhập thất bại"
        log("Đăng nhập thành công")

        # Bước 3: Lấy nội dung trang chủ
        log("Lấy nội dung trang sản phẩm...")
        inventory_text = get_inventory_text(driver, wait)
        print("\n===== NỘI DUNG LẤY ĐƯỢC =====")
        print(inventory_text[:1000])
        print("=============================\n")

        # Bước 4: Đưa vào Google Dịch
        translated_text = translate_text_with_google(driver, wait, inventory_text)

        # Bước 5: Lưu file txt
        save_text_file(TXT_FILE, translated_text)
        assert TXT_FILE.exists() and TXT_FILE.stat().st_size > 0, "Không tạo được file txt"

        # Bước 6: Tải ảnh
        image_url = get_first_product_image_url(driver, wait)
        download_image(image_url, IMG_FILE)
        assert IMG_FILE.exists() and IMG_FILE.stat().st_size > 0, "Không tải được ảnh"

        # Bước 7: Logout
        logout_saucedemo(driver, wait)

        log("Hoàn thành toàn bộ test")
        print("\n===== FILE KẾT QUẢ =====")
        print(f"TXT : {TXT_FILE.resolve()}")
        print(f"ẢNH : {IMG_FILE.resolve()}")
        print("========================")

    except Exception as e:
        log(f"LỖI: {e}")
        raise
    finally:
        log("Đóng trình duyệt...")
        driver.quit()


if __name__ == "__main__":
    main()