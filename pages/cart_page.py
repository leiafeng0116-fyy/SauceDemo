from base.base_page import BasePage
from pages.inventory_page import InventoryPage
from selenium.webdriver.common.by import By


class CartPage(BasePage):
    
    cart_item_selector = (By.CSS_SELECTOR, ".cart_item")
    remove_btn_selector = (By.XPATH, "//button[contains(text(),'Remove')]")

    _item_name_xpath = "//div[contains(text(),'{}') and contains(@class,'inventory_item_name')]"
    cart_item_by_name = (By.XPATH, _item_name_xpath)
    cart_item_price_by_name = (By.XPATH, _item_name_xpath + "/following-sibling::div[@class='inventory_item_price']")
    cart_item_desc_by_name = (By.XPATH, _item_name_xpath + "/following-sibling::div[@class='inventory_item_desc']")
    remove_btn_by_name = (By.XPATH, _item_name_xpath + "/following-sibling::button[contains(text(),'Remove')]")
    
    your_cart_text = (By.CSS_SELECTOR, "span.title")
    continue_shopping_btn = (By.ID, "continue-shopping")
    checkout_btn = (By.ID, "checkout")

    @classmethod
    def open_cart_page(cls, driver):
        InventoryPage(driver).click_cart_icon()
        return cls(driver)
    
    def get_all_cart_items(self):
        """获取购物车中所有商品元素"""
        return self.driver.find_elements(*self.cart_item_selector)
    
    def remove_product_from_cart_by_name(self, product_name):
        """根据商品名称点击对应的 Remove 按钮，从购物车移除该商品"""
        remove_btn_locator = (self.remove_btn_by_name[0], self.remove_btn_by_name[1].format(product_name))
        remove_btn = self.wait_for_element_clickable(remove_btn_locator)
        self.driver.execute_script("arguments[0].click();", remove_btn)

    def remove_products_from_cart_by_namelist(self, product_names:list):
        """根据商品名称列表批量移除购物车中的商品"""
        for name in product_names:
            self.remove_product_from_cart_by_name(name)
    
    def reset_cart(self):
        """重置购物车：移除所有已在购物车中的商品。"""
        # saucedemo.com 的购物车数据存储在服务端 session 中，cookie 注入恢复登录态时会连带恢复购物车数据。
        # 此方法通过 JS 遍历所有按钮，自动点击 "Remove" 清空购物车，确保每个测试用例开始时购物车状态一致。
        self.driver.execute_script("""
            document.querySelectorAll('button').forEach(btn => {
                if (btn.textContent === 'Remove') btn.click();
            });
        """)

        # 等待移除操作完成，确保购物车已清空。等价于断言
        self.wait_for_element_invisible(self.remove_btn_selector)
    


    def get_your_cart_text(self):
        """获取购物车页面标题文本"""
        return self.get_text(self.your_cart_text)
    
    def click_continue_shopping(self):
        """点击 Continue Shopping 按钮返回商品列表页"""
        continue_btn = self.wait_for_element_clickable(self.continue_shopping_btn)
        self.driver.execute_script("arguments[0].click();", continue_btn)