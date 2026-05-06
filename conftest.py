# conftest：专门存放 pytest 全局 fixture、钩子函数、全局配置，所有测试用例自动共享，不用导入

import pytest
from selenium import webdriver
import os
from selenium.webdriver.safari.options import Options
from common.test_data import URLS, VALID_USER  
from common.keywords import CommonKeywords


# ===================== 截图工具函数 =====================
def _take_failure_screenshot(driver, request):
    """用例失败时自动截图（减少 fixture 间重复代码）"""
    if request.node.rep_call.failed:
        shot_dir = os.path.join("reports", "screenshots")
        os.makedirs(shot_dir, exist_ok=True)
        timestamp = str(int(__import__("time").time()))
        filename = f"{request.node.name}_{timestamp}.png"
        path = os.path.join(shot_dir, filename)
        driver.save_screenshot(path)
        print(f"失败已截图：{path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


# ===================== session 级：只打开一个 Safari 浏览器，所有测试共享 =====================
# 注意：Safari 限制同一时刻只能有一个 WebDriver 实例，所以所有测试只能用同一个浏览器。
@pytest.fixture(scope="session")
def global_driver():
    """整个测试会话只打开一个浏览器，登录一次"""
    options = Options()
    options.page_load_strategy = 'eager'
    driver = webdriver.Safari(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)

    # 先打开登录页，再登录一次，所有测试共享此 session
    driver.get(URLS["login_url"])
    kw = CommonKeywords(driver)
    kw.login(VALID_USER["username"], VALID_USER["password"])

    yield driver
    driver.quit()


# ===================== logged_driver - 使用已登录的 session =====================
@pytest.fixture(scope="function")
def logged_driver(request, global_driver):
    """使用 session 级 driver，跳转到 inventory 页面"""
    # 直接导航到 inventory 页面（Safari 的 session 共享，只要浏览器没关，登录态就在）
    global_driver.get(URLS["inventory_url"])

    # 兜底：如果因为某些原因 session 丢失，重新登录
    if "inventory.html" not in global_driver.current_url:
        kw = CommonKeywords(global_driver)
        kw.login(VALID_USER["username"], VALID_USER["password"])
        global_driver.get(URLS["inventory_url"])

    # Safari WebDriver 在页面跳转后需要 stabilization，否则会抛出 NoSuchFrameException
    __import__("time").sleep(1)

    # 重置购物车状态：移除所有已在购物车中的商品
    from pages.cart_page import CartPage
    cart_page = CartPage(global_driver)
    cart_page.reset_cart()

    yield global_driver

    # 用例失败时截图
    # _take_failure_screenshot(global_driver, request)


# ===================== login_driver - 测试登录使用 =====================
# 注意：Safari 同一时刻只能有一个 WebDriver 实例，依赖global_driver可以解决这个问题。大家就用一个浏览器
#       否则test_login和后续的测试用例一起运行时会报错。
@pytest.fixture(scope="function")
def login_driver(request, global_driver):
    """使用 session 级 driver，每次回到登录页，供测试不同登录场景"""
    global_driver.get(URLS["login_url"])
    global_driver.delete_all_cookies()
    global_driver.refresh()

    yield global_driver

    # 用例失败时截图
    # _take_failure_screenshot(global_driver, request)