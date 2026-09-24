"""填表与点击 —— Playwright 自动填表单

对比 Selenium: element.send_keys() + element.click()
Playwright: locator.fill() + locator.click()，自动等待元素可交互

运行: uv run python lessons/14_浏览器自动化_playwright/03_填表与点击.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

sample = Path(__file__).parent / "sample"
sample.mkdir(exist_ok=True)

# 生成一个带表单的本地 HTML
html_content = """<!DOCTYPE html>
<html>
<head><title>表单测试</title></head>
<body>
  <form id="myform">
    <input type="text" id="name" placeholder="姓名">
    <input type="email" id="email" placeholder="邮箱">
    <select id="city">
      <option value="">选择城市</option>
      <option value="bj">北京</option>
      <option value="sh">上海</option>
      <option value="gz">广州</option>
    </select>
    <input type="checkbox" id="agree">
    <label for="agree">同意条款</label>
    <button type="submit" id="submit">提交</button>
  </form>
  <div id="result" style="display:none">提交成功！</div>
  <script>
    document.getElementById('myform').addEventListener('submit', function(e) {
      e.preventDefault();
      document.getElementById('result').style.display = 'block';
    });
  </script>
</body>
</html>"""
html_file = sample / "test_form.html"
html_file.write_text(html_content, encoding="utf-8")

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        page.goto(f"file:///{html_file.resolve()}")

        print("=" * 55)
        print("1. 填写文本框 (fill)")
        print("=" * 55)
        page.locator("#name").fill("张三")
        print(f"  #name 填入: {page.locator('#name').input_value()}")
        page.locator("#email").fill("zhangsan@example.com")
        print(f"  #email 填入: {page.locator('#email').input_value()}")

        print("\n" + "=" * 55)
        print("2. 下拉选择 (select_option)")
        print("=" * 55)
        page.locator("#city").select_option("sh")
        print(f"  #city 选中: {page.locator('#city').input_value()}")

        print("\n" + "=" * 55)
        print("3. 勾选复选框 (check)")
        print("=" * 55)
        page.locator("#agree").check()
        print(f"  #agree 是否勾选: {page.locator('#agree').is_checked()}")

        print("\n" + "=" * 55)
        print("4. 点击提交按钮 (click)")
        print("=" * 55)
        page.locator("#submit").click()
        result = page.locator("#result")
        print(f"  提交后结果: {result.text_content()}")
        print(f"  结果是否可见: {result.is_visible()}")

        print("\n" + "=" * 55)
        print("5. fill vs type 的区别")
        print("=" * 55)
        page.locator("#name").fill("")  # 先清空
        page.locator("#name").type("李四", delay=50)  # 逐字输入，delay模拟打字速度
        print(f"  type 输入: {page.locator('#name').input_value()}")
        print("  fill: 一次性填入（快，适合表单）")
        print("  type: 逐字输入（慢，模拟真人，触发更多事件）")

        print("\n" + "=" * 55)
        print("6. 按键操作 (press)")
        print("=" * 55)
        page.locator("#name").press("Control+a")  # 全选
        page.locator("#name").press("Backspace")  # 删除
        print(f"  Ctrl+A -> Backspace 后: '{page.locator('#name').input_value()}'")

        browser.close()

    print("\n" + "=" * 55)
    print("完成!")
    print("=" * 55)
    print("要点:")
    print("  1. fill() 一次性填入并清空原有值，适合表单填写")
    print("  2. type() 逐字输入，delay 模拟打字速度，触发 keydown/keyup 事件")
    print("  3. select_option() 选下拉框，check() 勾选复选框")
    print("  4. press() 按键，支持组合键如 Control+a")

except Exception as e:
    print(f"\n  失败: {e}")
    print("  请确保系统已装 Chrome，或运行 uv run playwright install chromium")