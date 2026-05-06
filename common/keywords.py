# 公共业务关键字封装层：跨多个页面、多步骤业务流的封装
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from selenium.webdriver.support import expected_conditions as EC

class CommonKeywords:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.inventory_page = InventoryPage(driver)

    def login(self, username, password):
        self.login_page.login(username, password)


