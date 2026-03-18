from pages.login_page import LoginPage
from data.test_data import VALID_USERNAME, VALID_PASSWORD


def test_login_success(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    message = login_page.get_flash_message()
    assert "You logged into a secure area!" in message