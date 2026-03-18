from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):
    HEADER = (By.TAG_NAME, "h2")

    def get_header_text(self):
        return self.get_text(self.HEADER)