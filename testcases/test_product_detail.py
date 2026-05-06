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
