"""自动等待优势 —— Playwright 最大的卖点

对比 Selenium: 必须写 WebDriverWait + expected_conditions
Playwright: Locator 操作自动等待，代码大幅简化

运行: uv run python lessons/14_浏览器自动化_playwright/04_自动等待优势.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

sample = Path(__file__).parent / "sample"
sample.mkdir(exist_ok=True)

# 生成一个延迟加载元素的 HTML（2秒后才出现按钮）
html_content = """<!DOCTYPE html>
<html>
<head><title>自动等待测试</title></head>
<body>
  <h1>自动等待演示</h1>
  <p>页面加载2秒后会出现一个按钮，Playwright 自动等待它出现</p>
  <div id="container"></div>
  <script>
    setTimeout(function() {
      document.getElementById('container').innerHTML =
        '<button id="late-btn">延迟出现的按钮</button>';
    }, 2000);
  </script>
</body>
</html>"""
html_file = sample / "test_autowait.html"
html_file.write_text(html_content, encoding="utf-8")

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        page.goto(f"file:///{html_file.resolve()}")

        print("=" * 55)
        print("1. 自动等待：直接点击延迟出现的按钮")
        print("=" * 55)
        print("  页面加载后 2 秒才出现按钮 #late-btn")
        print("  Playwright: 直接 click()，自动等待元素出现")
        print()

        import time
        start = time.time()
        # 这一行就体现了 Playwright 的优势：
        # 不需要 WebDriverWait，直接 click，它会自动等
        page.locator("#late-btn").click()
        elapsed = time.time() - start
        print(f"  点击成功！等待了 {elapsed:.2f} 秒（按钮2秒后才出现）")

        print("\n" + "=" * 55)
        print("2. 对比：同样的逻辑 Selenium 要怎么写")
        print("=" * 55)
        print("""
  # Selenium 写法（需要 5-6 行）:
  from selenium.webdriver.support.ui import WebDriverWait
  from selenium.webdriver.support import expected_conditions as EC

  try:
      btn = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.ID, "late-btn"))
      )
      btn.click()
  except TimeoutException:
      print("超时")

  # Playwright 写法（只需 1 行）:
  page.locator("#late-btn").click()  # 自动等待+点击
""")

        print("=" * 55)
        print("3. 等待页面状态（networkidle）")
        print("=" * 55)
        page2 = browser.new_page()
        page2.goto("https://example.com", wait_until="networkidle")
        print(f"  等待网络空闲后，标题: {page2.title()}")
        print("  wait_until='networkidle' 等所有网络请求完成")

        print("\n" + "=" * 55)
        print("4. 超时设置")
        print("=" * 55)
        print("  默认超时 30 秒，可以全局或单次设置:")
        print("    page.set_default_timeout(5000)  # 全局5秒")
        print("    locator.click(timeout=3000)     # 这次3秒")

        # 演示超时
        page3 = browser.new_page()
        page3.set_content("<div>没有按钮的页面</div>")
        try:
            page3.locator("#nonexistent").click(timeout=1000)
        except Exception as e:
            print(f"  1秒超时后抛异常: {type(e).__name__}")

        browser.close()

    print("\n" + "=" * 55)
    print("完成!")
    print("=" * 55)
    print("要点:")
    print("  1. Locator 的 click/fill/check 等操作自动等待元素就绪")
    print("  2. 对比 Selenium 省了 WebDriverWait + expected_conditions 的模板代码")
    print("  3. wait_until='networkidle' 等网络请求全部完成")
    print("  4. set_default_timeout() 全局超时，click(timeout=) 单次超时")

except Exception as e:
    print(f"\n  失败: {e}")
    print("  请确保系统已装 Chrome，或运行 uv run playwright install chromium")