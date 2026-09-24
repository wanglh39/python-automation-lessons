# 模块 14：浏览器自动化（Playwright）

> Playwright 是微软开发的现代浏览器自动化库，比 Selenium 更快、API 更简洁、自带自动等待。本模块与 [模块 7（Selenium）](../07_浏览器自动化/) 并行，让你对比两种方案。

## Playwright vs Selenium 对比

| 维度 | Playwright | Selenium |
|---|---|---|
| 自动等待 | 内置，元素出现自动等 | 需手动配显式/隐式等待 |
| API 风格 | `page.locator().click()` 链式 | `driver.find_element().click()` |
| 代码量 | 少约 30-50% | 较冗长 |
| 速度 | 快（直接走 CDP 协议） | 较慢（走 WebDriver HTTP 协议） |
| 多浏览器 | chromium / firefox / webkit 统一 API | 需不同 driver |
| 截图 | `page.screenshot()` 一行 | `driver.save_screenshot()` |
| 录制工具 | `playwright codegen` 生成代码 | Selenium IDE 浏览器插件 |
| 生态/资料 | 较新但增长快 | 老牌，资料多 |
| 适用场景 | 新项目、爬虫、测试 | 旧项目维护、兼容老浏览器 |

> **选型建议**：新项目首选 Playwright；维护旧项目或需要兼容老 IE 用 Selenium。

## 核心库一览

| 库 | 来源 | 用途 | 推荐度 |
|---|:---:|---|:---:|
| `playwright` | 第三方（微软） | 浏览器自动化 | ★★★★★ |
| `playwright.sync_api` | 同上 | 同步 API（教学用） | ★★★★★ |
| `playwright.async_api` | 同上 | 异步 API（高并发爬虫用） | ★★★★ |

## 核心 API 速查

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 启动浏览器（channel="chrome" 用系统已装的 Chrome）
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page()

    # 导航
    page.goto("https://example.com")
    page.title()                    # 页面标题
    page.url                        # 当前 URL
    page.go_back()                  # 后退
    page.reload()                   # 刷新

    # 定位元素（Locator 模式，推荐）
    page.locator("#id")             # 按 ID
    page.locator(".class")          # 按 class
    page.locator("css=div > p")     # CSS 选择器
    page.locator("text=登录")       # 按文本
    page.locator("xpath=//div")     # XPath

    # 操作（自动等待元素出现再操作）
    locator.click()                 # 点击
    locator.fill("内容")            # 填充（清空再输入）
    locator.type("内容")            # 逐字输入（模拟键盘）
    locator.press("Enter")          # 按键
    locator.check()                 # 勾选复选框
    locator.select_option("值")     # 下拉选择

    # 获取信息
    locator.text_content()          # 文本内容
    locator.inner_text()            # 内部文本
    locator.get_attribute("href")   # 属性值
    locator.count()                 # 匹配数量
    locator.is_visible()            # 是否可见

    # 截图
    page.screenshot(path="shot.png")           # 全页截图
    page.screenshot(path="shot.png", full_page=True)  # 完整网页
    locator.screenshot(path="elem.png")        # 元素截图

    # 等待（大多数情况不需要，Locator 自动等待）
    page.wait_for_load_state("networkidle")    # 等网络空闲
    page.wait_for_timeout(2000)                # 等固定毫秒

    browser.close()
```

## 本模块示例

| 脚本 | 演示 |
|---|---|
| [01_打开网页与截图.py](01_打开网页与截图.py) | 启动 Chrome、打开网页、截图、获取标题 |
| [02_定位元素.py](02_定位元素.py) | CSS/text/XPath 定位、获取属性、遍历多元素 |
| [03_填表与点击.py](03_填表与点击.py) | 自动填表单、点击、下拉选择、按键 |
| [04_自动等待优势.py](04_自动等待优势.py) | 演示 Playwright 自动等待 vs Selenium 手动等待 |

运行方式：
```bash
uv run python lessons/14_浏览器自动化_playwright/01_打开网页与截图.py
```

> 本模块用 `channel="chrome"` 直接调用你系统已装的 Chrome，无需额外下载浏览器。如果没有 Chrome，脚本会提示替代方案。

## 底层原理（简单了解）

1. **CDP 协议**：Playwright 直接通过 Chrome DevTools Protocol（CDP）与浏览器通信，是 WebSocket 双向连接，比 Selenium 的 HTTP WebDriver 协议更快。
2. **自动等待原理**：Locator 的每个操作（click/fill 等）在执行前会自动轮询检查元素是否满足条件（存在、可见、可交互），默认超时 30 秒。这省去了 Selenium 里写 `WebDriverWait` 的麻烦。
3. **channel="chrome"**：Playwright 默认用自带的 Chromium，设置 `channel="chrome"` 则用系统安装的 Chrome，省去下载 150MB 浏览器。
4. **sync vs async**：`sync_api` 是同步阻塞，教学和简单脚本用；`async_api` 是协程，高并发爬虫（同时开几十个页面）用。底层一样，只是 API 风格不同。