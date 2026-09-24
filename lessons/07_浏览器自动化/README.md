# 模块 7：浏览器自动化

> 网页爬虫拿不到的内容（要点击、要登录、要等 JS 渲染），交给浏览器自动化。selenium 让 Python 真的开一个浏览器、像人一样点击输入截图，适合做自动化测试、表单填写、抓动态网页。本模块演示"打开网页、定位元素、填表点击、等待加载"四步走。

## 核心库一览

| 库 | 来源 | 用途 | 推荐度 |
|---|:---:|---|:---:|
| `selenium` | 第三方 | 驱动真实浏览器：打开网页、点击、输入、截图、等待 | ★★★★★ |
| `webdriver` | selenium 内置 | 浏览器驱动入口（Chrome、Firefox、Edge） | ★★★★★ |
| `By` | selenium 内置 | 定位方式常量（ID、NAME、CSS、XPATH 等） | ★★★★★ |
| `WebDriverWait` | selenium 内置 | 显式等待：等到某条件成立再继续 | ★★★★ |
| `expected_conditions` | selenium 内置 | 等待条件（可见、可点击、出现等） | ★★★★ |

## selenium vs playwright

| 对比项 | selenium | playwright |
|---|---|---|
| 出现时间 | 2004，老牌 | 2020，微软出品 |
| 驱动管理 | selenium 4 自带 selenium-manager 自动下载 | 自带驱动，无需额外管理 |
| 浏览器支持 | Chrome / Firefox / Edge / Safari | Chrome / Firefox / WebKit / Edge |
| API 风格 | 同步为主，需手动等待 | 默认自动等待，API 更现代 |
| 速度 | 中等 | 更快（直接走 CDP 协议） |
| 录制工具 | 有 Selenium IDE 浏览器插件 | 有 codegen 命令行录制 |
| 学习资料 | 极多，几乎所有教程都讲它 | 较新但增长快 |
| 适用场景 | 教学入门、老项目、跨浏览器测试 | 新项目、追求速度、并行测试 |

> **本模块选 selenium**：生态成熟、教程多、selenium 4 的 selenium-manager 已经自动管理驱动，入门门槛低。学完 selenium 再看 playwright 会发现很多概念相通。

## 核心 API 速查

```python
# --- 打开浏览器、访问网页、关闭 ---
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--headless")           # 无头模式（不弹窗，服务器常用）
options.add_argument("--disable-gpu")        # 禁用 GPU（无头时建议加）
driver = webdriver.Chrome(options=options)   # selenium 4 自动管理驱动

driver.get("https://example.com")            # 打开网页
print(driver.title)                          # 页面标题
print(driver.current_url)                    # 当前 URL
driver.save_screenshot("截图.png")           # 截图保存
driver.quit()                                # 关闭浏览器（释放资源）
```

```python
# --- 定位元素 ---
from selenium.webdriver.common.by import By

driver.find_element(By.ID, "username")               # 按 id
driver.find_element(By.NAME, "email")                # 按 name 属性
driver.find_element(By.CLASS_NAME, "btn-primary")    # 按 class
driver.find_element(By.TAG_NAME, "input")            # 按标签名
driver.find_element(By.CSS_SELECTOR, "div.menu > a") # 按 CSS 选择器
driver.find_element(By.XPATH, "//input[@type='text']")  # 按 XPath

driver.find_elements(By.TAG_NAME, "p")               # 找多个，返回列表

elem.text                                           # 元素的可见文字
elem.get_attribute("href")                          # 取属性值
```

```python
# --- 输入、点击、清空、下拉框 ---
elem.send_keys("张三")                               # 输入文字
elem.clear()                                        # 清空输入框
elem.click()                                        # 点击

from selenium.webdriver.support.ui import Select
select = Select(driver.find_element(By.TAG_NAME, "select"))
select.select_by_visible_text("选项 A")             # 按可见文字选
select.select_by_value("opt_a")                     # 按 value 选
```

```python
# --- 等待加载 ---
# 隐式等待：全局设置，找元素时最多等 N 秒
driver.implicitly_wait(10)                          # 单位秒

# 显式等待：针对某条件最多等 N 秒，更精确
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "result"))   # 元素出现在 DOM 里
)
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "result")) # 元素可见
)
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "btn"))          # 元素可点击
)
```

## 本模块示例

| 脚本 | 演示 |
|---|---|
| [01_打开网页与截图.py](01_打开网页与截图.py) | 创建无头 Chrome、打开 example.com、取标题/URL、截图保存、关闭 |
| [02_定位元素.py](02_定位元素.py) | 六种定位方式（ID/NAME/CLASS/TAG/CSS/XPATH）、find_element vs find_elements、取文字和属性 |
| [03_填表与点击.py](03_填表与点击.py) | send_keys 输入、click 点击、clear 清空、Select 下拉框、自动填表单流程 |
| [04_等待加载.py](04_等待加载.py) | 隐式等待 vs 显式等待、三种等待条件、对比适用场景 |

运行方式：
```bash
uv run python lessons/07_浏览器自动化/01_打开网页与截图.py
uv run python lessons/07_浏览器自动化/02_定位元素.py
uv run python lessons/07_浏览器自动化/03_填表与点击.py
uv run python lessons/07_浏览器自动化/04_等待加载.py
```

> 没装 Chrome 浏览器也能跑：脚本会优雅提示"未找到浏览器"而不崩溃。建议先装 Chrome，selenium 4 的 selenium-manager 会自动下载匹配的驱动，不用手动管。

## 底层原理（简单了解）

1. **WebDriver 协议是 W3C 标准**：selenium 通过 HTTP 跟浏览器驱动（chromedriver）通信，驱动再控制浏览器。流程是 `Python 代码 -> HTTP 请求 -> chromedriver -> Chrome 浏览器`。所以 selenium 能跨语言（Python/Java/JS 都有客户端）也跨浏览器（换个驱动就行）。
2. **selenium-manager 自动管理驱动**：selenium 4 内置 selenium-manager，第一次运行时自动检测本机 Chrome 版本、下载匹配的 chromedriver、缓存起来。以前要手动下载驱动、对版本、放 PATH，现在全不用了。
3. **无头模式（headless）**：浏览器不开窗口、不显示界面，在后台跑，速度更快、能在没有显示器的服务器上跑。适合截图、抓数据；调试时建议去掉 `--headless` 看到浏览器实际在干什么。
4. **隐式等待 vs 显式等待**：隐式等待是全局的"找元素时最多等 N 秒"，简单但粗；显式等待是"等到某个条件成立"，可以等元素可见、可点击、消失等，精确控制。复杂页面（有动画、AJAX 加载）推荐显式等待。