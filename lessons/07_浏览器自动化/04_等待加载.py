"""等待加载 —— selenium 处理异步加载

演示 selenium 两种等待方式：
  - 隐式等待 driver.implicitly_wait(N)：全局设置，找元素时最多等 N 秒
  - 显式等待 WebDriverWait + expected_conditions：针对某条件最多等 N 秒
对比两种等待的区别和适用场景。

运行: uv run python lessons/07_浏览器自动化/04_等待加载.py
"""
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
)


SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)

# 本地页面：点击按钮后用 setTimeout 延迟 2 秒才出现元素，用来演示等待
HTML_CONTENT = """<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>等待演示页</title></head>
<body>
  <h2>异步加载演示</h2>
  <button id="load-btn" onclick="loadLater()">点击加载</button>
  <div id="status">未加载</div>
  <script>
    function loadLater() {
      document.getElementById('status').innerText = '加载中...';
      // 第 1 秒：动态插入元素到 DOM，但 display:none（不可见）
      setTimeout(function() {
        var c = document.createElement('div');
        c.id = 'content';
        c.style.display = 'none';
        c.innerText = '内容加载完成！';
        document.body.appendChild(c);
      }, 1000);
      // 第 2 秒：设为可见
      setTimeout(function() {
        document.getElementById('content').style.display = 'block';
        document.getElementById('status').innerText = '已完成';
      }, 2000);
    }
  </script>
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


# 准备本地 HTML
html_path = SAMPLE_DIR / "等待演示.html"
html_path.write_text(HTML_CONTENT, encoding="utf-8")

print("=" * 55)
print("1. 为什么需要等待：网页是异步加载的")
print("=" * 55)
print("  很多网页用 AJAX / JS 动态加载内容，元素不是立刻出现")
print("  如果在元素出现前就 find_element，会抛 NoSuchElementException")
print("  selenium 提供两种等待：隐式等待（简单粗）和显式等待（精确）")

print("\n" + "=" * 55)
print("2. 不等待会怎样：演示找不到元素的报错")
print("=" * 55)
driver = create_driver()
if driver is None:
    print("\n  浏览器启动失败，请安装 Chrome 后重试。")
    raise SystemExit(1)
driver.get(html_path.resolve().as_uri())
# 先点击按钮触发延迟加载
driver.find_element(By.ID, "load-btn").click()
print("  已点击加载按钮，content 元素 1 秒后才插入 DOM，2 秒后才可见")
print("  立刻去找内容元素（不等待）:")
try:
    driver.find_element(By.ID, "content")
    print("  找到了（不应该发生，元素还没插入）")
except NoSuchElementException:
    print("  -> NoSuchElementException: 元素还没插入 DOM，find_element 直接失败了")
print("  -> 这就是为什么要等待：代码跑得比网页加载快")

print("\n" + "=" * 55)
print("3. 隐式等待：driver.implicitly_wait(N)")
print("=" * 55)
print("  隐式等待是全局设置：找元素时如果没找到，最多轮询等 N 秒")
print("  设置一次，后续所有 find_element 都生效")
driver.implicitly_wait(3)   # 设置全局隐式等待 3 秒
# 重新加载并触发
driver.get(html_path.resolve().as_uri())
driver.find_element(By.ID, "load-btn").click()
print("  已设置 implicitly_wait(3)，点击加载按钮后立刻找内容:")
start = time.time()
content = driver.find_element(By.ID, "content")
elapsed = time.time() - start
print(f"  找到了！实际等了 {elapsed:.2f} 秒（元素 1 秒后插入 DOM，在 3 秒超时内）")
print(f"  内容文字: {content.text!r}  (注意: 此时 display:none，text 是空串)")
print("  -> 隐式等待会在超时内反复找，找到就立刻返回，不用等到超时")
print("  -> 缺点: 只能等'出现在 DOM 里'，不能等'可见'/'可点击'，条件单一")

print("\n" + "=" * 55)
print("4. 显式等待：WebDriverWait + expected_conditions")
print("=" * 55)
print("  显式等待针对某个条件最多等 N 秒，条件丰富、精确控制")
print("  语法: WebDriverWait(driver, 超时秒).until(条件)")
# 关掉隐式等待，避免干扰显式等待的计时
driver.implicitly_wait(0)
driver.get(html_path.resolve().as_uri())
driver.find_element(By.ID, "load-btn").click()
print("  点击加载按钮后，用显式等待等内容可见:")
start = time.time()
content = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.ID, "content"))
)
elapsed = time.time() - start
print(f"  等到了！实际等了 {elapsed:.2f} 秒")
print(f"  内容文字: {content.text!r}  (visibility_of 能等到 display:block，text 有值)")
print("  -> WebDriverWait(driver, 5).until(条件) 最多等 5 秒，条件成立就返回")
print("  -> 条件不成立会一直轮询，直到成立或超时（超时抛 TimeoutException）")

print("\n" + "=" * 55)
print("5. 三种常用等待条件对比")
print("=" * 55)
print("  重新加载，分别演示三种条件:")
driver.get(html_path.resolve().as_uri())
driver.find_element(By.ID, "load-btn").click()

# 条件 1: presence_of_element_located —— 元素出现在 DOM 里（可能不可见）
start = time.time()
elem = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "content"))
)
t1 = time.time() - start
print(f"  presence_of_element_located: 等 {t1:.2f}s，元素在 DOM 里了")
print(f"    此时 elem.text = {elem.text!r}  (可能还是空，因为 display:none 刚改)")

# 条件 2: visibility_of_element_located —— 元素可见（display 不是 none）
driver.get(html_path.resolve().as_uri())
driver.find_element(By.ID, "load-btn").click()
start = time.time()
elem = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.ID, "content"))
)
t2 = time.time() - start
print(f"  visibility_of_element_located: 等 {t2:.2f}s，元素可见了")
print(f"    此时 elem.text = {elem.text!r}  (有值，因为 display:block 且文字已填)")

# 条件 3: element_to_be_clickable —— 元素可点击（可见且没被禁用）
# 用加载按钮演示（它一开始就可点击）
clickable = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID, "load-btn"))
)
print(f"  element_to_be_clickable: 按钮可点击，is_displayed={clickable.is_displayed()}, is_enabled={clickable.is_enabled()}")
print("  -> presence: 在 DOM 里就行（可能不可见）；visibility: 必须可见；clickable: 可见且可用")
print("  -> 按需选: 抽数据用 presence，等显示用 visibility，等点击用 clickable")

print("\n" + "=" * 55)
print("6. 等待超时：条件一直不成立会抛 TimeoutException")
print("=" * 55)
print("  演示等一个永远不会出现的元素:")
# 重新加载一个干净页面，避免前面页面的 JS 定时器干扰
driver.get("data:text/html,<html><body><p>空白页</p></body></html>")
try:
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "never-exist"))
    )
except TimeoutException:
    print("  -> TimeoutException: 等了 2 秒还没出现，抛异常")
print("  -> 显式等待超时会抛 TimeoutException，用 try/except 处理")
print("  -> 这比隐式等待好：能针对单个操作设不同超时，异常类型也更明确")

print("\n" + "=" * 55)
print("7. 隐式等待 vs 显式等待：怎么选")
print("=" * 55)
print("  +----------------+-------------------+-------------------+")
print("  |     对比项     |    隐式等待       |    显式等待       |")
print("  +----------------+-------------------+-------------------+")
print("  |    设置方式    |  全局设一次       |  每次单独写       |")
print("  |    等待条件    |  只等'出现'       |  可见/可点击/消失等|")
print("  |    超时时间    |  全局统一         |  每次可不同       |")
print("  |    代码量      |  少               |  多               |")
print("  |    精确度      |  低               |  高               |")
print("  +----------------+-------------------+-------------------+")
print("  建议:")
print("    - 简单页面、元素基本都立刻出现: 隐式等待够用，设 3-5 秒")
print("    - 复杂页面、有 AJAX/动画/跳转: 用显式等待，精确控制每个条件")
print("    - 不要混用: 同一脚本里隐式和显式一起用会互相干扰，计时变乱")

driver.quit()

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. 网页异步加载，不等待就找元素会抛 NoSuchElementException")
print("  2. 隐式等待 implicitly_wait(N) 全局设一次，简单但只能等'出现'，条件单一")
print("  3. 显式等待 WebDriverWait(driver, N).until(条件)，条件丰富、超时可定制")
print("  4. 三种条件: presence(DOM 里有) < visibility(可见) < clickable(可见且可用)")
print("  5. 简单页面用隐式等待，复杂页面用显式等待；两者不要混用，会互相干扰")