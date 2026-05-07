from selenium.webdriver.common.by import By
from base.base_page import BasePage
from common.test_data import URLS

class LoginPage(BasePage):  # 继承 -- 子类拥有父类的所有功能

    # 定位
    login_logo = (By.CSS_SELECTOR, ".login_logo")
    username_input = (By.ID, "user-name")
    password_input = (By.ID, "password")
    login_btn = (By.ID, "login-button")
    locked_user_error_text = (By.XPATH, "//h3[@data-test='error']")


    def login(self, username, password):
        self.input_text(self.username_input, username)
        self.input_text(self.password_input, password)
        ele_login = self.driver.find_element(*self.login_btn) # *为拆包
        self.driver.execute_script("arguments[0].click();", ele_login)


 
