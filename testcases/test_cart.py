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

    """CASE4: 进入结算页面结算"""
    def test_checkout(self, logged_driver):
        add_items_to_cart(logged_driver, "Backpack","Onesie")
        cart_page = CartPage.open_cart_page(logged_driver)
        cart_page.click_checkout()
        cart_page.wait_for_element_visible(cart_page.checkout_information)  # 等待结算信息表单可见，说明已进入结算页面
        cart_page.input_checkout_info("John", "Doe", "12345")  # 输入结算信息并继续
        cart_page.wait_for_element_visible(cart_page.checkout_overview)  # 等待结算概览可见，说明已进入结算概览页面
        # 断言结算概览页面显示正确的商品总价、税费
        checkout_price = cart_page.get_checkout_price()
        assert checkout_price[0] == "Item total: $37.98", f"断言失败，结算概览页面商品总价不正确，预期：'Item total: $37.98'，实际：{cart_page.item_price_total}" 
        assert checkout_price[1]  == "Tax: $3.04", f"断言失败，结算概览页面税费不正确，预期：'Tax: $3.04'，实际：{cart_page.item_tax_total}"
        assert checkout_price[2]  == "Total: $41.02", f"断言失败，结算概览页面总价不正确，预期：'Total: $41.02'，实际：{cart_page.item_total}"
        # 点击finish
        cart_page.click_finish_btn()
        cart_page.wait_for_element_visible(cart_page.back_btn)
        cpmplete_text = cart_page.get_all_complete_text()
        assert cpmplete_text[0] == "Thank you for your order!", f"断言失败"
        assert cpmplete_text[1] == "Your order has been dispatched, and will arrive just as fast as the pony can get there!", f"断言失败"
        
