from selenium.webdriver.common.by import By
from base.base_page import BasePage
from common.test_data import URLS

class LoginPage(BasePage):  # 继承 -- 子类拥有父类的所有功能

    # 定位
    username_input = (By.ID, "user-name")
    password_input = (By.ID, "password")
    login_btn = (By.ID, "login-button")
    locked_user_error_text = (By.XPATH, "//h3[@data-test='error']")



    def login(self, username, password):
        self.input_text(self.username_input, username)
        self.input_text(self.password_input, password)
        ele_login = self.driver.find_element(*self.login_btn) # *为拆包
        self.driver.execute_script("arguments[0].click();", ele_login)


    '''
    语法：
    ❓为什么这几个类变量不加self??
    这几个变量是类属性，不是实例属性，所以不用加self。
    实例属性是写在构造函数里面的，针对每个实例单独保存的，必须要加self。
    类函数调用类属性，可以写self.属性名，也可以写类名.属性名。
    总结：实例属性是写在构造函数里面的，针对每个实例都要单独初始化和保存，申明时需要加self。
    类属性是写在类里面的，不会根据实例的不同而变化，申明时不用加self，但是类函数调用的时候可以写成self.属性名
    '''
