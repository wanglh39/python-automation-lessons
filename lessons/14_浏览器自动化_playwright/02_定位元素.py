"""定位元素 —— Playwright 的 Locator 模式

对比 Selenium: find_element(By.ID, ...) 返回 WebElement
Playwright: page.locator("#id") 返回 Locator，操作时自动等待

运行: uv run python lessons/14_浏览器自动化_playwright/02_定位元素.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

sample = Path(__file__).parent / "sample"
sample.mkdir(exist_ok=True)

# 生成一个本地测试 HTML
html_content = """<!DOCTYPE html>
<html>
<head><title>定位元素测试</title></head>
<body>
  <h1 id="title">欢迎</h1>
  <div class="card">卡片1</div>
  <div class="card">卡片2</div>
  <div class="card">卡片3</div>
  <a href="https://example.com" id="link1">链接文字</a>
  <input type="text" name="username" placeholder="输入用户名">
  <button data-action="submit">提交按钮</button>
  <ul>
    <li>项目一</li>
    <li>项目二</li>
    <li>项目三</li>
  </ul>
</body>
</html>"""
html_file = sample / "test_locate.html"
html_file.write_text(html_content, encoding="utf-8")

print("=" * 55)
print("1. Playwright 定位方式一览")
print("=" * 55)
print("  page.locator('#id')         按 ID")
print("  page.locator('.class')      按 class")
print("  page.locator('css=...')     CSS 选择器")
print("  page.locator('text=文本')   按文本内容")
print("  page.locator('xpath=...')   XPath")
print("  对比 Selenium: find_element(By.ID, 'id') 较冗长")

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        page.goto(f"file:///{html_file.resolve()}")

        print("\n" + "=" * 55)
        print("2. 按 ID / class 定位")
        print("=" * 55)
        title = page.locator("#title")
        print(f"  #title 文本: {title.text_content()}")

        cards = page.locator(".card")
        print(f"  .card 数量: {cards.count()}")
        for i in range(cards.count()):
            print(f"    第{i+1}个: {cards.nth(i).text_content()}")

        print("\n" + "=" * 55)
        print("3. 按文本 / 属性定位")
        print("=" * 55)
        link = page.locator("text=链接文字")
        print(f"  text=链接文字 -> href: {link.get_attribute('href')}")

        btn = page.locator("[data-action='submit']")
        print(f"  [data-action='submit'] -> 文本: {btn.text_content()}")

        print("\n" + "=" * 55)
        print("4. CSS 选择器组合")
        print("=" * 55)
        items = page.locator("ul > li")
        print(f"  ul > li 共 {items.count()} 项:")
        for i in range(items.count()):
            print(f"    {items.nth(i).text_content()}")

        print("\n" + "=" * 55)
        print("5. XPath 定位")
        print("=" * 55)
        first_li = page.locator("xpath=//ul/li[1]")
        print(f"  //ul/li[1]: {first_li.text_content()}")

        print("\n" + "=" * 55)
        print("6. 获取元素属性与状态")
        print("=" * 55)
        inp = page.locator("[name='username']")
        print(f"  placeholder: {inp.get_attribute('placeholder')}")
        print(f"  是否可见: {inp.is_visible()}")
        print(f"  是否启用: {inp.is_enabled()}")

        browser.close()

    print("\n" + "=" * 55)
    print("完成!")
    print("=" * 55)
    print("要点:")
    print("  1. page.locator() 返回 Locator，不立即查找（延迟执行）")
    print("  2. 调用 .click()/.fill() 等操作时才查找，且自动等待元素就绪")
    print("  3. .count() 获取匹配数量，.nth(i) 取第 i 个")
    print("  4. text= 和 xpath= 前缀是 Playwright 特有，比 Selenium 简洁")

except Exception as e:
    print(f"\n  失败: {e}")
    print("  请确保系统已装 Chrome，或运行 uv run playwright install chromium")