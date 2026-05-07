# 自动化测试面试问答集

所有问题均来自该项目真实遇到的坑和修复过程。

---

## 问题一：Safari `<select>` 下拉框操作挂死

### 问题描述

排序测试 `test_sort_items` 执行时卡死 5 分 28 秒后报 `ReadTimeoutError`。

### 根因

`Select(dropdown).select_by_visible_text()` 内部会调用 `option.click()`，Safari WebDriver 对原生 `<option>` 元素的 `.click()` 操作存在兼容性问题，会无限挂起直到超时。

### 修复

用 JavaScript 代替 Select 类：
1. 先用 JS 查找目标 `option` 的 `value`
2. 再用 JS 设置 `d.value = value` + `dispatchEvent(new Event('change', {bubbles: true}))`

**关键细节**：`bubbles: true` 必须加，否则页面 JS 监听不到 change 事件，排序不会真正生效。

### 面试回答

> "印象比较深的是一个 Safari 兼容性问题。排序下拉框选择在 Safari 上会卡死到超时，排查发现是 Selenium 的 Select 类内部调了 `option.click()`，Safari WebDriver 对这个操作支持有问题。解决方案是用 JavaScript 直接设置 select 的 value 并触发 change 事件。这个经历让我对跨浏览器兼容性测试有了更实际的理解——有些问题在 Chrome 上完全正常，但在 Safari 上就会暴露。"

### 追问

- **Q: 为什么不用 `Select` 的 `select_by_value()`？**
  - A: 同样会调 `option.click()`，一样会挂死。
- **Q: 为什么不用 `Select` 的 `select_by_index()`？**
  - A: 一样调 `option.click()`，逃不掉。

---

## 问题二：session 隔离 + XPath `//` vs `.//`

### 问题描述

购物车相关测试用例单独跑都通过，但连续执行时必失败。加购之后执行移除，找不到 "Add to cart" 按钮，因为这个按钮已经是Remove了。

### 排查过程

1. **第一层（猜错）**：以为是前端 sessionStorage 缓存 → fixture 加 `sessionStorage.clear()` → 无效
2. **第二层（看日志）**：加 log 发现 用例 开始时购物车已有 2 个商品（之前case 遗留的）
3. **第三层（定位根因）**：购物车数据存在**服务端 session** 中。cookie 注入恢复登录态时，服务端连带恢复了该 session 的购物车数据
4. **第四层（附带发现）**：修复数据隔离后仍然失败，发现 `item.find_element()` 中 XPath 用 `//` 而非 `.//`，导致点击的是全局第一个 "Add to cart"，而非目标商品的按钮

### 修复

1. **新建 CartPage 封装清空逻辑**，职责分离
2. **在 fixture 中自动调用 `cart_page.reset_cart()`**：通过 JS 遍历页面，自动点击所有 "Remove" 按钮，清空上一个用例遗留的购物车数据
3. **修复 XPath `//` 为 `.//`**：确保元素查找从当前节点上下文开始

### 面试回答

> 有一个印象深刻的问题是 session 隔离相关的。我们项目用 `scope="session"` 的 driver 和 cookie 注入来实现免密登录，问题是不同测试用例之间购物车数据会互相干扰。

> 排查时我先怀疑是前端缓存问题，就在 fixture 里加了清除 sessionStorage 的逻辑，但没用。接着我在case中增加log输出，结合错误日志，发现用例执行时购物车已有 2 个商品（正是前一个case添加的）。这说明购物车数据没被隔离，进一步分析才发现购物车状态存在服务端 session 中，cookie 注入恢复登录态时，服务端会连带恢复该 session 下的购物车数据，这才是核心原因。解决方案是在 CartPage 封装清空购物车的逻辑（用一个 JS 脚本遍历页面自动点掉所有 'Remove' 按钮），再在fixture 中自动调用 CartPage 的 reset_cart 方法。

> 这个问题让我意识到，自动化测试中不仅要关注表面的用例失败，还要深入分析数据存储的底层逻辑，而且解决方案要兼顾可维护性，比如用 fixture 自动清理而非零散加在每个用例里。

> "In my automation testing project, I encountered a really memorable issue related to session isolation. We were testing an e-commerce website, and we used a WebDriver instance with scope="session" plus cookie injection to enable password-free login—but the shopping cart data was interfering between different test cases.

> At first, I suspected it was a frontend caching issue, so I added logic to clear the sessionStorage in the fixture, but that didn’t work. Then I added log outputs to the test cases, and from the error logs, I saw that the shopping cart already had 2 items (exactly the ones added by the previous test case). This proved the shopping cart data wasn’t isolated. After deeper analysis, I found the core cause: the shopping cart state was stored in the server-side session. When we restored the login state via cookie injection, the server also restored the shopping cart data tied to that session.

> To fix this, I encapsulated the logic to clear the shopping cart in a CartPage class—using a JavaScript script to iterate through the page and automatically click all 'Remove' buttons. Then I configured the fixture to call the reset_cart() method from CartPage automatically.

> This issue taught me that in automation testing, we can’t just focus on the surface-level test failures; we need to dig into the underlying logic of how data is stored. Also, solutions should prioritize maintainability—for example, using fixtures to handle automatic cleanup instead of adding ad-hoc cleanup code to every single test case."

### 追问

- **Q: 为什么用 `scope="session"`？**
  - A: Safari 限制同一时刻只能有一个 WebDriver 实例，无法为每个用例启动独立浏览器，所以必须复用。
- **Q: 有没有其他方案？**
  - A: 也可以每个用例执行完调 `reset_cart()`，但容易遗忘。放在 fixture 里自动执行更可靠，不依赖开发者的记忆力。
- **Q: 为什么不用 Chrome？**
  - A: 项目需求指定在 Safari 上执行。

---

## 问题三：Safari NoSuchFrameException 错误

### 问题描述

页面跳转后执行元素查找，Safari WebDriver 会间歇性抛出 `NoSuchFrameException`，导致测试不稳定。

### 根因

macOS Ventura 上 Safari WebDriver 的已知 bug，页面导航后 frame 上下文丢失。

### 修复

所有公共操作方法（`click_element`, `input_text`, `get_text` 等）加 try-except 兜底：

```python
def click_element(self, locator):
    try:
        self.wait.until(EC.element_to_be_clickable(locator))
    except Exception:
        self.driver.switch_to.default_content()  # 重置 frame 上下文
        self.wait.until(EC.element_to_be_clickable(locator))
    element.click()
```

### 面试回答

> "项目运行在 Safari 上，遇到一个 macOS Ventura 的 Safari WebDriver 已知 bug：页面跳转后 frame 上下文会丢失，导致 `NoSuchFrameException`。解决方案是在 BasePage 的每个公共操作方法里加 try-except 兜底——第一次失败时调用 `switch_to.default_content()` 重置 frame 上下文后重试。这不是一个优雅的方案，但这是一个对 Safari 兼容性问题的实处理方式，保证了测试的稳定性。"

### 追问

- **Q: 为什么不修更根本的原因？**
  - A: 这是 Safari WebDriver 的已知 bug，不是代码逻辑问题，由 Apple 的 WebDriver 实现导致，只能 workaround。
- **Q: try-except 是否会影响性能？**
  - A: 正常执行时一次通过，没有额外开销。只有在触发 Safari bug 时才会走 catch 分支。

---

## 项目选型：为什么用 Selenium + Pytest 这套方案

### 面试回答

> "项目主要跑在 Safari 上，PyTest + Selenium 是最成熟稳定的选择。架构上采用分层设计：BasePage（Selenium 公共操作）→ Pages（页面元素定位）→ Keywords（业务场景封装）→ TestCases（纯测试逻辑）。这种分层的优势是：页面变更时只需要改 Page 层的定位符，业务逻辑变了只改 Keywords 层，测试用例本身不受影响。另外用 fixture 管理浏览器生命周期和 cookie 注入、自动截图等，减少了测试代码的重复。"

---

## 问题四：session过期后，case没有重新登录，导致后面的用例全挂了
之前fixture兜底是检查url有没有inventory，未考虑到缓存中也会有这个字段，导致判断失效fixture没有重新登录，后续的case就全挂了。更新了判断条件，等待3s看看login按钮是否存在，存在则重新登录。解决问题。


## 核心收获总结

如果你在面试中被问到"自动化测试中遇到过什么问题"，建议选 **问题一（Safari 兼容性）** + **问题二（session 隔离）** 两个组合回答：

1. 一个偏技术细节（Safari WebDriver 兼容性处理）
2. 一个偏排查思路（数据分析 → 定位深层原因 → 方案设计 → 附带发现）

两个问题展示了不同的能力维度，比只讲一个更全面。