"""填表与点击 —— selenium 模拟人工操作

演示 selenium：send_keys 输入文字、click 点击、clear 清空、Select 下拉框选择。
用一个本地表单页面演示"自动填表单"的完整流程。

运行: uv run python lessons/07_浏览器自动化/03_填表与点击.py
"""
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
    ElementNotInteractableException,
)


SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)

# 本地表单页面：包含输入框、下拉框、单选、复选、提交按钮
# 提交后会用 JS 把填的内容显示出来，方便验证
HTML_CONTENT = """<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>注册表单</title></head>
<body>
  <h2>用户注册</h2>
  <form id="reg-form" onsubmit="return showResult(event)">
    <label>姓名: <input type="text" id="name" name="name"></label><br><br>
    <label>邮箱: <input type="text" id="email" name="email" value="默认邮箱@x.com"></label><br><br>
    <label>城市:
      <select id="city" name="city">
        <option value="">请选择</option>
        <option value="bj">北京</option>
        <option value="sh">上海</option>
        <option value="gz">广州</option>
        <option value="sz">深圳</option>
      </select>
    </label><br><br>
    <label>性别:
      <input type="radio" name="gender" value="m">男
      <input type="radio" name="gender" value="f">女
    </label><br><br>
    <label><input type="checkbox" id="agree" name="agree">同意条款</label><br><br>
    <button type="submit" id="submit">提交</button>
  </form>
  <div id="result" style="margin-top:20px;padding:10px;border:1px solid #ccc;"></div>
  <script>
    function showResult(e) {
      e.preventDefault();
      var form = document.getElementById('reg-form');
      var data = new FormData(form);
      var lines = [];
      for (var [k, v] of data.entries()) lines.push(k + ' = ' + v);
      document.getElementById('result').innerText = lines.join('\\n');
      return false;
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
html_path = SAMPLE_DIR / "注册表单.html"
html_path.write_text(HTML_CONTENT, encoding="utf-8")

print("=" * 55)
print("1. 启动浏览器并打开表单页")
print("=" * 55)
driver = create_driver()
if driver is None:
    print("\n  浏览器启动失败，请安装 Chrome 后重试。")
    raise SystemExit(1)
driver.get(html_path.resolve().as_uri())
print(f"  已打开: {driver.title!r}")

print("\n" + "=" * 55)
print("2. 输入文字：element.send_keys()")
print("=" * 55)
name_input = driver.find_element(By.ID, "name")
name_input.send_keys("张三")
print(f"  姓名框输入 '张三' 后的值: {name_input.get_attribute('value')!r}")
print("  -> send_keys() 往输入框里敲文字，就像人用键盘输入")

print("\n" + "=" * 55)
print("3. 清空输入框：element.clear()")
print("=" * 55)
email_input = driver.find_element(By.ID, "email")
print(f"  邮箱框默认值: {email_input.get_attribute('value')!r}")
email_input.clear()
print("  执行 clear() 后:")
print(f"    邮箱框的值: {email_input.get_attribute('value')!r}")
email_input.send_keys("zhangsan@example.com")
print(f"  重新输入后: {email_input.get_attribute('value')!r}")
print("  -> clear() 清空输入框；有默认值的框要先 clear 再 send_keys")

print("\n" + "=" * 55)
print("4. 下拉框选择：Select 类")
print("=" * 55)
city_select = Select(driver.find_element(By.ID, "city"))
# 按可见文字选
city_select.select_by_visible_text("深圳")
selected = city_select.first_selected_option
print(f"  select_by_visible_text('深圳') -> 选中: {selected.text!r} (value={selected.get_attribute('value')!r})")
# 按 value 选
city_select.select_by_value("sh")
selected = city_select.first_selected_option
print(f"  select_by_value('sh')          -> 选中: {selected.text!r} (value={selected.get_attribute('value')!r})")
# 列出所有选项
print(f"  所有选项: {[(o.text, o.get_attribute('value')) for o in city_select.options]}")
print("  -> 下拉框要用 Select 类包装，不能直接 send_keys 或 click")
print("  -> select_by_visible_text 按文字，select_by_value 按 value，select_by_index 按序号")

print("\n" + "=" * 55)
print("5. 单选框和复选框：element.click()")
print("=" * 55)
# 单选框：点击选中
radio_female = driver.find_element(By.CSS_SELECTOR, "input[name='gender'][value='f']")
radio_female.click()
print(f"  点击 '女' 单选框后是否选中: {radio_female.is_selected()}")
# 验证另一个没被选中
radio_male = driver.find_element(By.CSS_SELECTOR, "input[name='gender'][value='m']")
print(f"  '男' 单选框是否选中: {radio_male.is_selected()}")
# 复选框
agree = driver.find_element(By.ID, "agree")
print(f"  同意条款初始状态: {agree.is_selected()}")
agree.click()
print(f"  点击后是否选中: {agree.is_selected()}")
print("  -> 单选/复选用 click() 点击，用 is_selected() 判断是否选中")
print("  -> 单选框点一个，同组的其他自动取消选中")

print("\n" + "=" * 55)
print("6. 点击提交按钮：element.click() + 验证结果")
print("=" * 55)
submit_btn = driver.find_element(By.ID, "submit")
print(f"  提交按钮文字: {submit_btn.text!r}")
print(f"  按钮是否可点击: {submit_btn.is_enabled()}")
submit_btn.click()
# 等一下让 JS 执行完（这里页面是同步的，sleep 只是稳妥起见）
time.sleep(0.3)
result = driver.find_element(By.ID, "result")
print(f"  提交后页面显示的结果:")
for line in result.text.split("\n"):
    print(f"    {line}")
print("  -> click() 模拟鼠标点击；提交后 JS 把表单数据显示在 div#result 里")

print("\n" + "=" * 55)
print("7. 完整自动填表流程（重新填一遍，模拟真实自动化）")
print("=" * 55)
# 重新加载页面
driver.get(html_path.resolve().as_uri())
print("  步骤 1: 清空并填写姓名")
driver.find_element(By.ID, "name").send_keys("李四")
print("  步骤 2: 清空并填写邮箱")
email = driver.find_element(By.ID, "email")
email.clear()
email.send_keys("lisi@example.com")
print("  步骤 3: 选择城市")
Select(driver.find_element(By.ID, "city")).select_by_visible_text("北京")
print("  步骤 4: 选择性别")
driver.find_element(By.CSS_SELECTOR, "input[name='gender'][value='m']").click()
print("  步骤 5: 勾选同意条款")
driver.find_element(By.ID, "agree").click()
print("  步骤 6: 点击提交")
driver.find_element(By.ID, "submit").click()
time.sleep(0.3)
result = driver.find_element(By.ID, "result")
print(f"  提交结果:")
for line in result.text.split("\n"):
    print(f"    {line}")
print("  -> 自动填表就是: 定位元素 -> send_keys/click -> 提交 -> 验证结果")

print("\n" + "=" * 55)
print("8. 元素状态检查：是否可见、可用、选中")
print("=" * 55)
name_el = driver.find_element(By.ID, "name")
print(f"  姓名框 is_displayed() = {name_el.is_displayed()}  (是否可见)")
print(f"  姓名框 is_enabled()    = {name_el.is_enabled()}  (是否可用/没被禁用)")
print(f"  同意框 is_selected()    = {driver.find_element(By.ID, 'agree').is_selected()}  (是否选中)")
print("  -> 操作前先检查状态，避免操作不可见/被禁用的元素报错")

driver.quit()

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. send_keys() 输入文字，clear() 清空，click() 点击；有默认值要先 clear")
print("  2. 下拉框用 Select 类：select_by_visible_text / select_by_value / select_by_index")
print("  3. 单选/复选用 click() 点击，is_selected() 判断是否选中")
print("  4. 操作前用 is_displayed / is_enabled / is_selected 检查状态更稳妥")
print("  5. 自动填表流程: 定位 -> 输入/选择 -> 提交 -> 验证结果，和人手动操作步骤一样")