from selenium.webdriver.common.by import By
from base.base_page import BasePage
from pages.inventory_page import InventoryPage
from common.test_data import ITEMS_DETAILS


class ProductDetailPage(BasePage):

    product_name = (By.CSS_SELECTOR, ".inventory_details_name")
    product_price = (By.CSS_SELECTOR, ".inventory_details_price")
    product_desc = (By.CSS_SELECTOR, ".inventory_details_desc")
    product_image = (By.CSS_SELECTOR, ".inventory_details_img")
    add_to_cart_btn = (By.CSS_SELECTOR, "#add-to-cart")
    remove_btn = (By.CSS_SELECTOR, "#remove")
    back_to_products_btn = (By.CSS_SELECTOR, "#back-to-products")

    # https://chat.deepseek.com/share/4kaf9aekb8dfx944cd 
    # 类方法：可以通过类名直接调用，而不需要先创建实例。用类名.方法名调用，语义清晰，适合工厂方法等场景。
    # 这里如果用实例方法，需要先创建实例才能调用方法，但还没进入页面（需要实例才能进页面，但进了页面才能有实例）。
    # detail_page = ProductDetailPage(driver)  # 此时还没跳转到详情页
    # detail_page.open_by_name("...")          # 方法里再跳转？语义混乱。虽然能实现功能，但是不建议使用。如果类里构造函数有验证容易报错
    @classmethod
    def open_by_name(cls, driver, product_name):
        """从 inventory 页面点击进入指定商品的详情页"""
        InventoryPage(driver).go_to_item_detail_by_name(product_name)
        return cls(driver)
    
    def get_product_name(self):
        return self.driver.find_element(*self.product_name).text
    
    def get_product_price(self):
        return self.driver.find_element(*self.product_price).text
    
    def click_add_btn(self):
        add_btn = self.wait_for_element_visible(self.add_to_cart_btn)
        self.driver.execute_script("arguments[0].click();", add_btn)
    
    def click_remove_btn(self):
        remove_btn = self.wait_for_element_visible(self.remove_btn) 
        self.driver.execute_script("arguments[0].click();", remove_btn)

    def click_back_btn(self):
        back_btn = self.wait_for_element_clickable(self.back_to_products_btn)
        self.driver.execute_script("arguments[0].click();", back_btn)

    def click_cart_icon(self):
        cart_icon = self.wait_for_element_clickable(InventoryPage.cart_badge)
        self.driver.execute_script("arguments[0].click();", cart_icon)


