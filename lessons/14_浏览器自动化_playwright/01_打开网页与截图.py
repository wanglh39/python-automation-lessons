"""打开网页与截图 —— Playwright 最基本用法

对比 Selenium：不需要 webdriver、不需要 driver manager、代码更简洁。
用 channel="chrome" 直接调用系统已装的 Chrome。

运行: uv run python lessons/14_浏览器自动化_playwright/01_打开网页与截图.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

sample = Path(__file__).parent / "sample"
sample.mkdir(exist_ok=True)

print("=" * 55)
print("1. 启动浏览器（用系统 Chrome，无头模式）")
print("=" * 55)
print("  代码: p.chromium.launch(channel='chrome', headless=True)")
print("  对比 Selenium: webdriver.Chrome(options) + 自动管理 driver")
print()

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)

        print("=" * 55)
        print("2. 打开网页并获取信息")
        print("=" * 55)
        page = browser.new_page()
        page.goto("https://example.com")
        print(f"  标题: {page.title()}")
        print(f"  URL:  {page.url}")

        print("\n" + "=" * 55)
        print("3. 截图保存")
        print("=" * 55)
        shot1 = sample / "playwright_全页.png"
        page.screenshot(path=str(shot1))
        print(f"  普通截图: {shot1.name} ({shot1.stat().st_size} 字节)")

        shot2 = sample / "playwright_完整网页.png"
        page.screenshot(path=str(shot2), full_page=True)
        print(f"  完整截图: {shot2.name} ({shot2.stat().st_size} 字节)")

        print("\n" + "=" * 55)
        print("4. 打开第二个页面（多页面操作）")
        print("=" * 55)
        page2 = browser.new_page()
        page2.goto("https://example.com")
        print(f"  页面2标题: {page2.title()}")
        print(f"  当前有 {len(browser.contexts[0].pages)} 个页面")

        print("\n" + "=" * 55)
        print("5. 获取页面内容")
        print("=" * 55)
        text = page.locator("body").inner_text()
        print(f"  页面文本前80字: {text[:80]}...")

        browser.close()

    print("\n" + "=" * 55)
    print("完成!")
    print("=" * 55)
    print("要点:")
    print("  1. with sync_playwright() as p: 管理整个生命周期，自动清理")
    print("  2. channel='chrome' 用系统 Chrome，不用下载额外浏览器")
    print("  3. headless=True 不显示窗口，教学/服务器用；False 能看到操作")
    print("  4. page.screenshot() 一行截图，full_page=True 截完整长网页")

except Exception as e:
    print(f"\n  启动失败: {e}")
    print("\n  替代方案:")
    print("    1. 确保系统已装 Chrome 浏览器")
    print("    2. 或运行 uv run playwright install chromium 下载自带浏览器")
    print("       然后把脚本里 channel='chrome' 改成不传 channel 参数")