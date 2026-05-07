from pages.cart_page import CartPage
from common.keywords import add_items_to_cart
from pages.inventory_page import InventoryPage

class TestCartPage:

    """CASE1: 进入购物车页面，展示正确的标题和按钮"""
    def test_cart_page(self, logged_driver):
        cart_page = CartPage.open_cart_page(logged_driver)
        cart_page.wait_for_element_visible(cart_page.your_cart_text)
        assert "cart.html" in logged_driver.current_url, f"断言失败，当前 URL 不包含 'cart.html'，实际：{logged_driver.current_url}"
        assert cart_page.get_your_cart_text() == "Your Cart", f"断言失败，页面标题不正确，预期：'Your Cart'，实际：{cart_page.get_your_cart_text()}"

    """CASE2: 购物车页面点击 Continue Shopping 按钮返回商品列表页"""
    def test_click_continue_shopping(self, logged_driver):
        cart_page = CartPage.open_cart_page(logged_driver)
        cart_page.click_continue_shopping()
        assert "inventory" in logged_driver.current_url, f"断言失败，当前 URL 不包含 'inventory'，实际：{logged_driver.current_url}"

    """CASE3: 清空购物车"""
    def test_reset_cart(self, logged_driver):
        add_items_to_cart(logged_driver, "Backpack", "Bolt T-Shirt", "Onesie")
        inventory_page = InventoryPage(logged_driver)
        assert inventory_page.cart_item_count() == 3, f"添加购物车失败"
        inventory_page.click_cart_icon()  # 进入购物车页
        cart_page = CartPage(logged_driver)
        cart_page.wait_for_element_clickable(cart_page.remove_btn_selector) 
        cart_page.reset_cart()
        cart_items = cart_page.get_all_cart_items()
        assert len(cart_items) == 0, f"断言失败，购物车中商品数量不为0"