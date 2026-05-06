# 公共业务关键字封装层：基于BasePage与LoginPage封装常用业务操作
from pages.login_page import LoginPage
from pages.products_page import HomePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CommonKeywords:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver) #创建LoginPage实例对象
        self.home_page = HomePage(driver)

    # 关键字login,封装login
    def login(self, username, password):
        self.login_page.open_login_page()
        # 点击切换成帐号密码登录
        # safari运行会报错，可能是因为这个元素被遮挡，显示等待只能判断元素存在，元素可点击，但是像遮挡这种问题最好就用js去点击
        # 点击切换成帐号密码登录
        # ele = self.login_page.driver.find_element(*self.login_page.password_login_tab)  
        # self.login_page.driver.execute_script("arguments[0].click();", ele)
        
        # ❓**self.login_page.password_login_tab为什么要加*
        # 这个叫拆包！因为password_login_tab = (By.XPATH, '//*[@id="...')申明之后，password_login_tab是一个元祖
        # find_element要求传两个参数，如果直接传password_login_tab，就只有一个参数（一个元祖是一个参数）
        # 所以*就是把元祖拆包，拆成两个参数，依次传给find_element
        # 👉总结：元祖传定位，必须带*，做拆包
        # 衍生： **kwargs关键字拆包，拆字典，常用场景：
        # 1. Pytest配置测试数据 (看test_logon.py 我已经改成这个形式了)
        # 2. ActionChains 传参经常用 **，比如移动到元素并点击。
        #     # 定义动作参数
        #     action_kwargs = {
        #         "by": By.ID,
        #         "value": "submit_btn"
        #     }
        #     # 使用 ** 拆包传参
        #     ActionChains(driver).move_to_element(**action_kwargs).click().perform()
        # 3. 装饰器/通用函数（传参数可以不确定）
        #     def log_action(**kwargs):
        #         print("执行操作：", kwargs)
        #     # 调用时传任意参数
        #     log_action(action="click", element="button", timeout=10) #传多组参数
        

        # 输入
        self.login_page.input_text(self.login_page.username_input, username)
        self.login_page.input_text(self.login_page.password_input, password)
        # 点击登录
        ele_login = self.login_page.driver.find_element(*self.login_page.login_btn)
        self.login_page.driver.execute_script("arguments[0].click();", ele_login)

    def open_home_page(self):
        self.home_page.open_home_page()

    # 等待元素可见
    def wait_for_element_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    # 等待元素可点击
    def wait_for_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

