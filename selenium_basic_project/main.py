from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://the-internet.herokuapp.com/login")

        wait = WebDriverWait(driver, 10)

        username_input = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        username_input.send_keys("tomsmith")
        password_input.send_keys("SuperSecretPassword!")
        login_button.click()

        success_message = wait.until(
            EC.presence_of_element_located((By.ID, "flash"))
        )

        print("Đăng nhập thành công!")
        print(success_message.text)

        input("Nhấn Enter để đóng trình duyệt...")

    except Exception as e:
        print("Có lỗi xảy ra:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()