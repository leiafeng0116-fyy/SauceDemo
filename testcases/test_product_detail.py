from pages.product_detail_page import ProductDetailPage
from common.test_data import ITEMS_DETAILS

class TestProductDetail:

    """CASE1: 点击商品名称进入详情页，展示正确的商品信息"""
    def test_product_detail(self, logged_driver):
        item = ITEMS_DETAILS["Bolt T-Shirt"]
        detail_page = ProductDetailPage.open_by_name(logged_driver, item["name"])
        # 断言详情页展示正确的商品信息
        assert detail_page.get_product_name() == item["name"], f"断言失败，商品名称不正确，预期：{item['name']}，实际：{detail_page.get_product_name()}"
        assert detail_page.get_product_price() == item["price"], f"断言失败，商品价格不正确，预期：{item['price']}，实际：{detail_page.get_product_price()}"
    
    """CASE2: 从详情页点击 Back to products 返回商品列表页"""
    def test_back_to_products(self, logged_driver):
        detail_page = ProductDetailPage.open_by_name(logged_driver, ITEMS_DETAILS["Bolt T-Shirt"]["name"])
        detail_page.click_back_btn()
        # 断言返回后 URL 包含 inventory，说明回到商品列表页了 
        assert "id=" not in logged_driver.current_url, f"断言失败，当前 URL 不应该包含 'id='，实际：{logged_driver.current_url}"

    """CASE3: 从详情页添加商品到购物车"""
    def test_add_to_cart_from_detail_page(self, logged_driver):
        detail_page = ProductDetailPage.open_by_name(logged_driver, ITEMS_DETAILS["Fleece Jacket"]["name"])
        detail_page.click_add_btn()
        # Remove按钮出现，说明已添加到购物车。等价于断言
        detail_page.wait_for_element_visible(detail_page.remove_btn)
        

    """CASE4: 从详情页移除已添加的商品"""
    def test_remove_from_cart_from_detail_page(self, logged_driver):
        detail_page = ProductDetailPage.open_by_name(logged_driver, ITEMS_DETAILS["Fleece Jacket"]["name"])
        detail_page.click_add_btn()  # 先添加到购物车
        detail_page.wait_for_element_clickable(detail_page.remove_btn)  # 等待 Remove 按钮可点击，说明已添加成功
        detail_page.click_remove_btn()  # 再从详情页移除
        # 等待 Add to cart 按钮可点击，说明已成功移除。等价于assert
        detail_page.wait_for_element_clickable(detail_page.add_to_cart_btn)  
    
    """CASE5: 从详情页点击购物车图标进入购物车页"""
    def test_go_to_cart_from_detail_page(self, logged_driver):
        detail_page = ProductDetailPage.open_by_name(logged_driver, ITEMS_DETAILS["Fleece Jacket"]["name"])
        detail_page.click_add_btn()  # 先添加到购物车
        detail_page.click_cart_icon()  # 点击页面上的购物车图标进入购物车页
        # 断言进入购物车页后 URL 包含 cart，说明成功跳转到购物车页了 
        assert "cart.html" in logged_driver.current_url, f"断言失败，当前 URL 不包含 'cart.html'，实际：{logged_driver.current_url}"
