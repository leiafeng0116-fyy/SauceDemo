# 公共业务关键字封装层：跨多个页面、多步骤业务流的封装
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from common.test_data import ITEMS_DETAILS


def login(driver, username, password):
    LoginPage(driver).login(username, password)

def add_items_to_cart(driver, *short_names):
    """ 业务关键字：添加多个商品到购物车
        short_names: ITEMS_DETAILS 中的 key，例如 "Backpack", "Onesie"
    """
    names = [ITEMS_DETAILS[k]["name"] for k in short_names]
    InventoryPage(driver).add_items_to_cart_by_name(names)



