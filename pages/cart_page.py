from base.base_page import BasePage

class CartPage(BasePage):
    """
    购物车相关操作封装。
    职责：管理购物车中的商品（添加、移除、清空）。
    """

    def reset_cart(self):
        """
        重置购物车：移除所有已在购物车中的商品。
        
        saucedemo.com 的购物车数据存储在服务端 session 中，cookie 注入恢复登录态时会连带恢复购物车数据。
        此方法通过 JS 遍历所有商品按钮，自动点击 "Remove" 清空购物车，确保每个测试用例开始时购物车状态一致。
        """
        self.driver.execute_script("""
            for (const btn of document.querySelectorAll('.btn_inventory')) {
                if (btn.textContent === 'Remove') {
                    btn.click();
                }
            }
        """)
        # 等待移除操作完成（JS 点击后需要浏览器处理）
        import time
        time.sleep(0.5)