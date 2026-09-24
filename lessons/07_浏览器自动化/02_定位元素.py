"""定位元素 —— selenium 找元素的六种方式

演示 selenium 的六种定位方式：By.ID / NAME / CLASS_NAME / TAG_NAME / CSS_SELECTOR / XPATH。
对比 find_element（找一个）和 find_elements（找所有），取元素文字和属性。
用本地 HTML 文件演示，不依赖网络。

运行: uv run python lessons/07_浏览器自动化/02_定位元素.py
"""
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
)


SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)

# 本地测试 HTML，包含各种可定位的元素
HTML_CONTENT = """<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>定位演示页</title></head>
<body>
  <h1 id="main-title">欢迎来到测试页面</h1>
  <p class="intro">这是一个用于演示 selenium 定位方式的页面。</p>

  <form id="login-form" name="login">
    <input type="text" id="username" name="username" placeholder="用户名">
    <input type="password" id="password" name="password" placeholder="密码">
    <button type="submit" id="submit-btn" class="btn btn-primary">登录</button>
  </form>

  <div class="menu">
    <a href="/home" class="nav-link">首页</a>
    <a href="/news" class="nav-link">新闻</a>
    <a href="/about" class="nav-link">关于</a>
  </div>

  <ul id="item-list">
    <li class="item">苹果</li>
    <li class="item">香蕉</li>
    <li class="item">樱桃</li>
  </ul>

  <p>页面底部的一段文字。</p>
</body>
</html>
"""


def create_driver():
    """创建无头 Chrome，失败时返回 None 并打印友好提示。"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--no-sandbox")
    try:
        return webdriver.Chrome(options=options)
    except WebDriverException as e:
        print(f"  [浏览器启动失败] {type(e).__name__}")
        msg = str(e)
        if "cannot find Chrome binary" in msg or "no chrome" in msg.lower():
            print("  原因: 未检测到 Chrome 浏览器，请先安装 Chrome")
        else:
            print(f"  详情: {msg[:200]}")
        return None
    except Exception as e:
        print(f"  [未知错误] {type(e).__name__}: {e}")
        return None


# 准备本地 HTML 文件
html_path = SAMPLE_DIR / "定位演示.html"
html_path.write_text(HTML_CONTENT, encoding="utf-8")

print("=" * 55)
print("1. 启动浏览器并打开本地测试页")
print("=" * 55)
driver = create_driver()
if driver is None:
    print("\n  浏览器启动失败，请安装 Chrome 后重试。")
    raise SystemExit(1)
# 用 file:// 协议打开本地 HTML，Windows 路径要转成绝对 URI
driver.get(html_path.resolve().as_uri())
print(f"  已打开: {driver.title!r}")
print(f"  URL: {driver.current_url}")
print("  -> 本地 HTML 文件用 file:// 协议打开，不依赖网络，演示更稳定")

print("\n" + "=" * 55)
print("2. 按 ID 定位：By.ID（最推荐，id 唯一）")
print("=" * 55)
h1 = driver.find_element(By.ID, "main-title")
print(f"  find_element(By.ID, 'main-title').text = {h1.text!r}")
btn = driver.find_element(By.ID, "submit-btn")
print(f"  登录按钮文字: {btn.text!r}")
print("  -> id 在页面里唯一，按 id 定位最快最稳，优先用")

print("\n" + "=" * 55)
print("3. 按 NAME 定位：By.NAME（表单字段常用）")
print("=" * 55)
user_input = driver.find_element(By.NAME, "username")
print(f"  用户名输入框的 placeholder: {user_input.get_attribute('placeholder')!r}")
pwd_input = driver.find_element(By.NAME, "password")
print(f"  密码框的 type: {pwd_input.get_attribute('type')!r}")
print("  -> 表单字段一般有 name 属性（提交表单要用），按 name 定位很方便")

print("\n" + "=" * 55)
print("4. 按 CLASS_NAME 定位：By.CLASS_NAME（只取一个 class）")
print("=" * 55)
intro = driver.find_element(By.CLASS_NAME, "intro")
print(f"  intro 段落文字: {intro.text!r}")
print("  -> CLASS_NAME 只能传单个 class 名，多个 class 用 CSS 选择器")

print("\n" + "=" * 55)
print("5. 按 TAG_NAME 定位：By.TAG_NAME（找某类标签）")
print("=" * 55)
# find_element 只返回第一个匹配的
first_p = driver.find_element(By.TAG_NAME, "p")
print(f"  第一个 <p> 的文字: {first_p.text!r}")
# find_elements 返回所有匹配的，是列表
all_p = driver.find_elements(By.TAG_NAME, "p")
print(f"  页面里所有 <p> 的数量: {len(all_p)}")
for i, p in enumerate(all_p):
    print(f"    <p> {i + 1}: {p.text!r}")
print("  -> find_element 找一个（找不到抛异常），find_elements 找所有（找不到返回空列表）")

print("\n" + "=" * 55)
print("6. 按 CSS_SELECTOR 定位：By.CSS_SELECTOR（最灵活）")
print("=" * 55)
# 多个 class 用 CSS 选择器
nav_links = driver.find_elements(By.CSS_SELECTOR, "a.nav-link")
print(f"  导航链接数量: {len(nav_links)}")
for a in nav_links:
    print(f"    {a.text!r} -> href={a.get_attribute('href')!r}")
# 组合选择器
form_btn = driver.find_element(By.CSS_SELECTOR, "form#login-form button.btn-primary")
print(f"  表单内主按钮: {form_btn.text!r}")
# 子元素选择器
first_item = driver.find_element(By.CSS_SELECTOR, "ul#item-list > li.item")
print(f"  列表第一项: {first_item.text!r}")
print("  -> CSS 选择器支持标签、class、id、后代、子元素、属性等，和前端写 CSS 一样")

print("\n" + "=" * 55)
print("7. 按 XPATH 定位：By.XPATH（最强大，但语法复杂）")
print("=" * 55)
# 绝对路径
title_by_xpath = driver.find_element(By.XPATH, "/html/body/h1")
print(f"  /html/body/h1: {title_by_xpath.text!r}")
# 相对路径 + 属性
user_by_xpath = driver.find_element(By.XPATH, "//input[@name='username']")
print(f"  //input[@name='username'] 的 placeholder: {user_by_xpath.get_attribute('placeholder')!r}")
# 取所有 li 的文字
items = driver.find_elements(By.XPATH, "//li[@class='item']")
print(f"  //li[@class='item'] 共 {len(items)} 个: {[li.text for li in items]}")
# 包含某文字的元素
contains = driver.find_element(By.XPATH, "//a[contains(text(), '新')]")
print(f"  //a[contains(text(),'新')]: {contains.text!r}")
print("  -> XPath 支持按文字内容、属性、层级定位，contains() 处理动态 class 很有用")
print("  -> 语法比 CSS 复杂，但能做 CSS 做不到的事（比如按文字内容找）")

print("\n" + "=" * 55)
print("8. find_element vs find_elements：找不到时的区别")
print("=" * 55)
# find_element 找不到会抛 NoSuchElementException
try:
    driver.find_element(By.ID, "not-exist")
except NoSuchElementException:
    print("  find_element 找不到元素 -> 抛 NoSuchElementException 异常")
# find_elements 找不到返回空列表，不抛异常
empty = driver.find_elements(By.CLASS_NAME, "not-exist")
print(f"  find_elements 找不到元素 -> 返回空列表: {empty}")
print("  -> 找单个元素要先 try/except；找多个直接判断列表是否为空更简洁")

print("\n" + "=" * 55)
print("9. 取元素的文字和属性：.text 和 .get_attribute()")
print("=" * 55)
link = driver.find_element(By.CSS_SELECTOR, "a.nav-link")
print(f"  元素 .text              = {link.text!r}")
print(f"  .get_attribute('href')  = {link.get_attribute('href')!r}")
print(f"  .get_attribute('class') = {link.get_attribute('class')!r}")
print(f"  .get_attribute('target') = {link.get_attribute('target')!r}  (没有该属性返回 None)")
print("  -> .text 取可见文字（display:none 的文字取不到）")
print("  -> .get_attribute() 取任意属性，属性不存在返回 None")

driver.quit()

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. 六种定位方式：ID > NAME > CSS > XPATH，按 id 最稳，CSS 最灵活，XPath 最强大")
print("  2. find_element 找一个（找不到抛异常），find_elements 找所有（找不到返回空列表）")
print("  3. .text 取可见文字，.get_attribute('xxx') 取属性值；不可见元素的 text 是空串")
print("  4. CSS 选择器写法和前端一样；XPath 能按文字内容定位，但语法更复杂")
print("  5. 本地 HTML 用 file:// 协议打开，不依赖网络，演示更稳定可靠")