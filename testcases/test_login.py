import pytest
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

# 登录测试数据
Login_test_data = {
    "valid_login":      ("standard_user", "secret_sauce",    InventoryPage.app_logo),
    "locked_out_login": ("locked_out_user", "secret_sauce",  LoginPage.locked_user_error_text),
}

class TestLogin:

    @pytest.mark.parametrize(
        "username,password,expect",
        Login_test_data.values(),
        ids=Login_test_data.keys()
    )
    
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_login_scenarios(self, login_driver, username, password, expect):
        login_driver = LoginPage(login_driver)
        login_driver.login(username, password)
        expected_ele = login_driver.wait_for_element_visible(expect)
        assert expected_ele.is_displayed(), f"元素断言失败，{expect}不存在"