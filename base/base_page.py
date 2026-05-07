# BasePage = 公共底层工具（点击、输入、等待），只放公共操作，不要写业务函数！
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver): # 构造函数
        self.driver = driver # 初始化driver
        self.wait = WebDriverWait(driver,30) # 初始化显示等待

    # 公用函数
    def open_url(self, url):
        self.driver.get(url)

    def input_text(self, locator, text):
        # Safari WebDriver 在 macOS Ventura 上存在已知 bug：
        # 页面跳转后执行元素查找会错误地抛出 NoSuchFrameException
        # 解决方法：先调用 switch_to.default_content() 重置 frame 上下文
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
        except Exception:
            self.driver.switch_to.default_content()
            element = self.wait.until(EC.presence_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def click_element(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            element = self.wait.until(EC.element_to_be_clickable(locator))
        except Exception:
            self.driver.switch_to.default_content()
            self.wait.until(EC.presence_of_element_located(locator))
            element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def get_title(self):
        return self.driver.title
    
    def get_text(self, locator):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
        except Exception:
            self.driver.switch_to.default_content()
            element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text
    
    # 等待元素可见
    def wait_for_element_visible(self, locator, timeout=10):
        # Safari WebDriver 在 macOS Ventura 上存在已知 bug：
        # 页面跳转后执行元素查找会错误地抛出 NoSuchFrameException
        # 解决方法：先调用 switch_to.default_content() 重置 frame 上下文
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except Exception:
            self.driver.switch_to.default_content()
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        
        # 等待元素不可见
    def wait_for_element_invisible(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except Exception:
            self.driver.switch_to.default_content()
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )

    # 等待元素可点击
    def wait_for_element_clickable(self, locator, timeout=10):
        # Safari WebDriver 在 macOS Ventura 上存在已知 bug：
        # 页面跳转后执行元素查找会错误地抛出 NoSuchFrameException
        # 解决方法：先调用 switch_to.default_content() 重置 frame 上下文
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except Exception:
            self.driver.switch_to.default_content()
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )


'''
self知识点：
    self就是对象自己，后面有谁调用BasePage这个类，生成了实例化对象，这个self就是谁
    两个作用：1. 在类内部保存自己的变量 2.在类内部，调用自己的方法
    🌟 self代表当前实例对象本身，用来在类内部访问自己的属性和方法，类里面所有方法第一个参数必须是self
'''