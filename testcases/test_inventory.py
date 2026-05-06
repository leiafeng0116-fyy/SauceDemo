from pages.inventory_page import InventoryPage
from common.test_data import ITEMS_DETAILS

class TestInventory:
    """CASE1: 登录后商品页标题显示Products"""
    def test_inventory_page(self, logged_driver):
        inventory_page = InventoryPage(logged_driver)
        product_title = inventory_page.wait_for_element_visible(inventory_page.Products_title)
        
        assert "inventory" in inventory_page.driver.current_url, f"断言失败，当前 URL 不包含 'inventory'，实际：{inventory_page.driver.current_url}"
        assert product_title.text == "Products", f"断言失败，标题文字不是 Products，实际：{product_title.text}"


    """CASE2: 登录后展示商品列表"""
    def test_product_list_visible(self, logged_driver):
        inventory_page = InventoryPage(logged_driver)
        items = inventory_page.get_inventory_items()

        # 断言商品列表可见且不为空
        assert inventory_page.is_product_list_visible(), "断言失败，商品列表未显示或为空"
        # 以第一个商品（Sauce Labs Backpack）为例断言详情正确显示
        first_item_name = ITEMS_DETAILS["Backpack"]["name"]
        assert inventory_page.is_product_detail_visible_by_name(first_item_name), f"断言失败，商品 '{first_item_name}' 的详情未正确显示"
        print(f"✅ test_product_list_visible passed：成功展示 {len(items)} 件商品，第一件商品详情正确显示")
    

    """CASE3: 添加多个商品到购物车"""
    def test_add_to_cart(self, logged_driver):
        inventory_page = InventoryPage(logged_driver)
        items_to_add = [
            ITEMS_DETAILS["Backpack"]["name"],
            ITEMS_DETAILS["Bolt T-Shirt"]["name"],
            ITEMS_DETAILS["Onesie"]["name"],
        ]
        inventory_page.add_items_to_cart_by_name(items_to_add)
        cart_count = inventory_page.cart_item_count()

        assert cart_count == len(items_to_add), f"断言失败，购物车中商品数量不正确，预期：{len(items_to_add)}，实际：{cart_count}"
        print(f"✅ 成功添加 {len(items_to_add)} 件商品到购物车")


    """CASE4: 从购物车移除已添加的商品"""
    def test_remove_from_cart(self, logged_driver):
        inventory_page = InventoryPage(logged_driver)
        item_to_add = ITEMS_DETAILS["Onesie"]["name"]
        # 先添加商品
        inventory_page.add_item_to_cart_by_name(item_to_add)
        assert inventory_page.remove_button_visible_by_name(item_to_add), "断言失败，Remove 按钮不可见"

        # 移除商品
        inventory_page.click_remove_button_by_name(item_to_add)
        cart_count = inventory_page.cart_item_count()

        assert cart_count == 0, f"断言失败，移除商品失败。购物车商品数量：{cart_count}"
        # print(f"✅ 成功移除 {item_to_add}，当前购物车数量：{cart_count}")

    """CASE5: 排序（价格从低到高）"""
    def test_sort_items(self, logged_driver):
        inventory_page = InventoryPage(logged_driver)
        inventory_page.sort_items("lohi")  # 使用简写参数，测试内部映射功能
        import time; time.sleep(3)
        # 断言排序后第一个商品是价格最低的（Sauce Labs Onesie，$7.99）
        first_item_price = inventory_page.get_first_item_price()
        assert first_item_price == "$7.99", f"断言失败，排序后第一个商品价格不正确，预期：$7.99，实际：{first_item_price}"
        print(f"✅ 成功按价格从低到高排序，第一件商品价格正确显示为 {first_item_price}")

    """CASE6: 点击商品链接进入详情页"""
    def test_click_item_link(self,logged_driver):
        inventory_page = InventoryPage(logged_driver)
        item = ITEMS_DETAILS["Onesie"]
        inventory_page.go_to_item_detail_by_name(item["name"])
        # 断言跳转到正确的商品详情页（URL 包含 item_id)
        expected_url_part = f"inventory-item.html?id={item['id']}"
        assert expected_url_part in inventory_page.driver.current_url, f"断言失败，点击商品链接后 URL 不正确，预期包含：{expected_url_part}，实际：{inventory_page.driver.current_url}"
        print(f"✅ 成功点击商品链接并跳转到详情页，当前 URL：{inventory_page.driver.current_url}")

