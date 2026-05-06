from selenium.webdriver.common.by import By
from base.base_page import BasePage
from common.test_data import SORT_OPTIONS_MAP


class InventoryPage(BasePage):

    app_logo = (By.CSS_SELECTOR, ".app_logo")
    Products_title = (By.CSS_SELECTOR, "span.title")

    # 带占位符 {} 的定位模板，传入 id 后缀即可
    add_btn_by_id = (By.XPATH, "//button[@id='add-to-cart-{}']")
    remove_btn_by_id = (By.XPATH, "//button[@id='remove-{}']")
    item_link_by_name = (By.XPATH, "//div[contains(@class,'inventory_item_name') and text()='{}']")
    
    inventory_items_selector = (By.CSS_SELECTOR, ".inventory_item")
    item_name_selector = (By.CSS_SELECTOR, ".inventory_item_name")
    item_price_selector = (By.CSS_SELECTOR, ".inventory_item_price")
    item_desc_selector = (By.CSS_SELECTOR, ".inventory_item_desc")
    add_button_selector = (By.XPATH, "//button[contains(@class,'btn_inventory') and text()='Add to cart']")
    remove_btn_selector = (By.XPATH, "//button[contains(@class,'btn_inventory') and text()='Remove']")
    
    cart_badge = (By.CSS_SELECTOR, ".shopping_cart_badge")
    
    sort_dropdown = (By.CSS_SELECTOR, ".product_sort_container")
    sort_options = (By.XPATH, "//option[text()='{}']")
    
    @staticmethod
    def _name_to_id(name):
        """将商品显示名称转换为 button id 格式（全小写、空格变连字符）"""
        return name.lower().replace(" ", "-")


    def get_products_text(self):
        """获取标题文本"""
        return self.get_text(self.Products_title)
    
    def get_inventory_items(self):
        """获取页面上所有商品元素"""
        return self.driver.find_elements(*self.inventory_items_selector)
    
    def is_product_list_visible(self):
        """检查商品列表是否可见"""
        items = self.get_inventory_items()
        return len(items) > 0 
    
    def is_product_detail_visible_by_name(self, product_name):
        """检查指定商品的详情是否可见"""
        items = self.get_inventory_items()
        for item in items:
            name = item.find_element(*self.item_name_selector).text
            if name == product_name:
                price = item.find_element(*self.item_price_selector).text
                desc = item.find_element(*self.item_desc_selector).text
                return all([name, price, desc])
        return False
    
    
    def add_item_to_cart_by_index(self, index):
        """根据商品索引点击对应的 Add to cart 按钮"""
        add_buttons = self.driver.find_elements(*self.add_button_selector)
        if index < len(add_buttons):
            self.driver.execute_script("arguments[0].click();", add_buttons[index])
        else:
            raise IndexError(f"索引 {index} 超出商品数量范围")

    def add_item_to_cart_by_name(self, name):
        """根据商品名称点击对应的 Add to cart 按钮"""
        item_id = self._name_to_id(name)
        locator = (self.add_btn_by_id[0], self.add_btn_by_id[1].format(item_id))
        add_btn = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", add_btn)

    def add_items_to_cart_by_name(self, names: list):
        """批量添加多个商品到购物车，用于测试 setup 阶段准备数据"""
        for name in names:
            self.add_item_to_cart_by_name(name)
    
    def remove_button_visible_by_name(self, name):
        """检查指定商品的按钮文本是否为 'Remove'（说明已在购物车中）"""
        item_id = self._name_to_id(name)
        locator = (self.remove_btn_by_id[0], self.remove_btn_by_id[1].format(item_id))
        remove_btn = self.driver.find_element(*locator)
        if remove_btn.text == "Remove" and remove_btn.is_displayed():
            return True
        return False
    
    def click_remove_button_by_name(self, name):
        """根据商品名称点击对应的 Remove 按钮"""
        item_id = self._name_to_id(name)
        locator = (self.remove_btn_by_id[0], self.remove_btn_by_id[1].format(item_id))
        remove_btn = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", remove_btn)

    def cart_item_count(self):
        """获取购物车中商品数量"""
        cart_badge = self.driver.find_elements(*self.cart_badge)
        if cart_badge:
            return int(cart_badge[0].text)
        return 0
    
    def get_all_product_names(self):
        """获取页面上所有商品的名称列表"""
        items = self.get_inventory_items()
        names = []
        for item in items:
            name = item.find_element(*self.item_name_selector).text
            names.append(name)
        return names

    def sort_items(self, option):
        """
        对页面上的商品进行排序。

        Args: option: 排序选项，支持以下值：
                "az" 或 "Name (A to Z)",
                "za" 或 "Name (Z to A)",
                "lohi" 或 "Price (low to high)",
                "hilo" 或 "Price (high to low)"
        """
        """
        语法：dict.get(key, default=None),key 是要查找的键，default 是可选参数，如果指定键不存在时返回的默认值，默认为 None。
        这里通过 SORT_OPTIONS_MAP.get(option, option) 实现了输入参数的灵活性：
        如果用户传入的是简写（如 "lohi"），会映射到完整的选项文本（如 "Price (low to high)"）；
        如果用户直接传入完整文本（如 "Price (low to high)"），则直接使用，不受影响。
        """
        option = SORT_OPTIONS_MAP.get(option, option)
        self.wait_for_element_visible(self.sort_dropdown).click()
        option_locator = (self.sort_options[0], self.sort_options[1].format(option))
        self.wait_for_element_visible(option_locator).click()

    def get_first_item_price(self):
        """获取排序后第一个商品的价格（字符串格式，如 "$7.99"）"""
        return self.driver.find_elements(*self.item_price_selector)[0].text

    def get_first_item_name(self):
        """获取排序后第一个商品的名称"""
        return self.driver.find_elements(*self.item_name_selector)[0].text
    
    def go_to_item_detail_by_name(self, name):
        """点击指定名称的商品链接，进入详情页"""
        locator = (self.item_link_by_name[0], self.item_link_by_name[1].format(name))
        item_link = self.wait_for_element_visible(locator)
        self.driver.execute_script("arguments[0].click();", item_link)
