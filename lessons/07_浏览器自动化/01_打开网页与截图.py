"""打开网页与截图 —— selenium 入门第一课

演示 selenium：创建无头 Chrome、打开网页、取标题和 URL、截图保存、关闭浏览器。
selenium 4 的 selenium-manager 会自动下载匹配的驱动，不用手动管 chromedriver。

运行: uv run python lessons/07_浏览器自动化/01_打开网页与截图.py
"""
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


# 截图保存到 sample 目录
SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)


def create_driver():
    """创建无头 Chrome 浏览器实例。

    selenium 4 自带 selenium-manager，会自动下载匹配版本的 chromedriver。
    如果本机没装 Chrome 或驱动下载失败，返回 None 而不是崩溃。
    """
    options = webdriver.ChromeOptions()
    # 无头模式：不弹窗，在后台跑，适合服务器和自动化脚本
    options.add_argument("--headless")
    # 无头时建议禁用 GPU，避免某些环境报错
    options.add_argument("--disable-gpu")
    # 把窗口设大一点，截图更完整（无头模式默认窗口可能很小）
    options.add_argument("--window-size=1280,800")
    # 避免在 Linux 服务器上以 root 跑时报错
    options.add_argument("--no-sandbox")
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except WebDriverException as e:
        print(f"  [浏览器启动失败] {type(e).__name__}")
        msg = str(e)
        if "cannot find Chrome binary" in msg or "no chrome" in msg.lower():
            print("  原因: 未检测到 Chrome 浏览器，请先安装 Chrome")
            print("  下载: https://www.google.com/chrome/")
        elif "session not created" in msg.lower():
            print("  原因: 浏览器版本和驱动不匹配，selenium-manager 下载驱动失败")
            print("  建议: 检查网络后重试，或手动下载 chromedriver 放到 PATH")
        else:
            print(f"  详情: {msg[:200]}")
        return None
    except Exception as e:
        print(f"  [未知错误] {type(e).__name__}: {e}")
        return None


print("=" * 55)
print("1. 创建无头 Chrome 浏览器")
print("=" * 55)
print("  配置: --headless（无头）+ --window-size=1280,800")
print("  selenium 4 的 selenium-manager 会自动下载匹配的 chromedriver")
driver = create_driver()
if driver is None:
    print("\n  浏览器启动失败，后续演示无法进行，脚本退出。")
    print("  请安装 Chrome 浏览器后重试。")
    raise SystemExit(1)
print(f"  浏览器已启动，会话 ID: {driver.session_id}")
print("  -> webdriver.Chrome(options=...) 创建实例，无头模式不弹窗")

print("\n" + "=" * 55)
print("2. 打开网页：driver.get(url)")
print("=" * 55)
url = "https://example.com"
print(f"  打开: {url}")
driver.get(url)
print("  -> get() 会等到页面 onload 触发才返回（不是立刻返回）")

print("\n" + "=" * 55)
print("3. 获取页面信息：title 和 current_url")
print("=" * 55)
print(f"  driver.title       = {driver.title!r}")
print(f"  driver.current_url = {driver.current_url!r}")
print(f"  driver.page_source 的长度 = {len(driver.page_source)} 字符")
print("  -> title 是 <title> 标签内容，current_url 是最终 URL（可能有跳转）")
print("  -> page_source 是整个 HTML 源码，可以拿去给 BeautifulSoup 解析")

print("\n" + "=" * 55)
print("4. 截图保存：driver.save_screenshot(path)")
print("=" * 55)
shot_path = SAMPLE_DIR / "example.png"
driver.save_screenshot(str(shot_path))
print(f"  截图已保存到: {shot_path}")
print(f"  文件大小: {shot_path.stat().st_size} 字节")
print("  -> save_screenshot 保存整个浏览器窗口的 PNG")
print("  -> 无头模式下截图是设定的 window-size 大小，所以前面把窗口设大一点")

print("\n" + "=" * 55)
print("5. 再打开一个页面，演示多次导航")
print("=" * 55)
url2 = "https://www.python.org"
print(f"  打开: {url2}")
try:
    driver.get(url2)
    print(f"  标题: {driver.title!r}")
    print(f"  URL:  {driver.current_url!r}")
    shot2 = SAMPLE_DIR / "python_org.png"
    driver.save_screenshot(str(shot2))
    print(f"  截图: {shot2} ({shot2.stat().st_size} 字节)")
except WebDriverException as e:
    print(f"  [访问失败] {type(e).__name__}: {str(e)[:150]}")
print("  -> 同一个 driver 可以多次 get()，相当于在地址栏输入新网址")

print("\n" + "=" * 55)
print("6. 关闭浏览器：driver.quit()")
print("=" * 55)
driver.quit()
print("  已关闭浏览器，释放了进程和资源")
print("  -> quit() 关闭整个浏览器并结束驱动进程")
print("  -> 别用 close()，它只关当前标签页，进程还在，容易泄漏")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. webdriver.Chrome(options=...) 创建浏览器，selenium 4 自动管理驱动")
print("  2. 无头模式加 --headless，不弹窗适合自动化；调试时去掉看浏览器在干什么")
print("  3. driver.get(url) 打开页面，.title / .current_url / .page_source 取信息")
print("  4. save_screenshot(path) 截图；用完务必 quit() 释放资源（别用 close()）")
print("  5. 浏览器启动可能失败（没装 Chrome、版本不匹配），必须 try/except 处理")