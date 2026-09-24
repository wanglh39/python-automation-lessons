"""解析本地 HTML —— BeautifulSoup 入门第一课

演示 BeautifulSoup：自动生成一个测试 HTML 文件，解析成树，
按标签名/class/id 查找元素，取文本和属性。不依赖网络，一定能跑。

运行: uv run python lessons/08_HTML解析爬虫/01_解析本地HTML.py
"""
from pathlib import Path

from bs4 import BeautifulSoup


# sample 目录用来放测试 HTML，和脚本同目录
SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)


# 这是一个包含标题、段落、链接、表格、列表的测试页面
SAMPLE_HTML = """<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="utf-8">
    <title>演示页面 - BeautifulSoup 入门</title>
</head>
<body>
    <h1 id="main-title">BeautifulSoup 入门演示</h1>
    <p class="intro">这是一个用来练习 HTML 解析的测试页面。</p>

    <div class="content">
        <h2>常用链接</h2>
        <ul>
            <li><a href="https://www.python.org">Python 官网</a></li>
            <li><a href="https://www.crummy.com/software/BeautifulSoup/">BeautifulSoup 文档</a></li>
            <li><a href="https://example.com" class="external">示例站点</a></li>
        </ul>

        <h2>价格表</h2>
        <table id="price-table">
            <tr><th>商品</th><th>价格</th><th>库存</th></tr>
            <tr><td>Python 书</td><td>59.00</td><td>10</td></tr>
            <tr><td>键盘</td><td>199.00</td><td>5</td></tr>
            <tr><td>鼠标</td><td>49.00</td><td>0</td></tr>
        </table>

        <p class="footer">页面底部说明文字</p>
    </div>
</body>
</html>
"""


def prepare_sample():
    """把测试 HTML 写到 sample 目录，返回文件路径"""
    path = SAMPLE_DIR / "demo.html"
    path.write_text(SAMPLE_HTML, encoding="utf-8")
    return path


print("=" * 55)
print("1. 准备测试 HTML 文件")
print("=" * 55)
html_path = prepare_sample()
print(f"  已生成: {html_path}")
print(f"  文件大小: {html_path.stat().st_size} 字节")
print("  -> 真实爬虫里这步是 requests.get() 抓回来的，这里用本地文件保证能跑")

print("\n" + "=" * 55)
print("2. 解析 HTML：BeautifulSoup(html, 'html.parser')")
print("=" * 55)
html_text = html_path.read_text(encoding="utf-8")
soup = BeautifulSoup(html_text, "html.parser")
print(f"  解析完成，对象类型: {type(soup).__name__}")
print("  -> 'html.parser' 是标准库后端，零依赖；求速度可换成 'lxml'")

print("\n" + "=" * 55)
print("3. 直接取标签：soup.title / soup.p / soup.h1")
print("=" * 55)
print(f"  soup.title        = {soup.title!r}")
print(f"  soup.title.string = {soup.title.string!r}")
print(f"  soup.h1           = {soup.h1!r}")
print(f"  soup.h1.string    = {soup.h1.string!r}")
print(f"  soup.p            = {soup.p!r}")
print("  -> soup.标签名 取第一个该标签；.string 取里面的文字")

print("\n" + "=" * 55)
print("4. find / find_all：按标签名查找")
print("=" * 55)
first_h2 = soup.find("h2")
all_h2 = soup.find_all("h2")
all_p = soup.find_all("p")
print(f"  soup.find('h2')        = {first_h2!r}")
print(f"  soup.find_all('h2') 数量 = {len(all_h2)}")
for i, h2 in enumerate(all_h2, 1):
    print(f"    第 {i} 个 h2: {h2.string!r}")
print(f"  soup.find_all('p') 数量  = {len(all_p)}")
print("  -> find 返回第一个，find_all 返回列表")

print("\n" + "=" * 55)
print("5. 按 class 和 id 查找")
print("=" * 55)
intro = soup.find("p", class_="intro")
print(f"  soup.find('p', class_='intro') = {intro!r}")
print(f"    文字: {intro.get_text(strip=True)!r}")
title_h1 = soup.find("h1", id="main-title")
print(f"  soup.find('h1', id='main-title') = {title_h1!r}")
print(f"    文字: {title_h1.get_text(strip=True)!r}")
external = soup.find("a", class_="external")
print(f"  soup.find('a', class_='external') = {external!r}")
print("  -> class_ 注意带下划线（class 是 Python 关键字）；id 直接传")

print("\n" + "=" * 55)
print("6. 获取文本 .get_text() 和属性 ['href']")
print("=" * 55)
first_a = soup.find("a")
print(f"  第一个 a 标签: {first_a!r}")
print(f"  文字 first_a.get_text()       = {first_a.get_text()!r}")
print(f"  属性 first_a['href']          = {first_a['href']!r}")
print(f"  安全取属性 first_a.get('href') = {first_a.get('href')!r}")
print(f"  不存在的属性 first_a.get('target') = {first_a.get('target')!r}  (返回 None)")
print("  -> ['href'] 不存在会抛 KeyError；.get('href') 不存在返回 None，更安全")

print("\n" + "=" * 55)
print("7. 遍历所有链接：find_all('a')")
print("=" * 55)
links = soup.find_all("a")
print(f"  共 {len(links)} 个链接:")
for i, a in enumerate(links, 1):
    text = a.get_text(strip=True)
    href = a.get("href", "(无 href)")
    print(f"    {i}. {text} -> {href}")
print("  -> 这是爬虫最常见操作：提取页面里所有超链接")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. BeautifulSoup(html, 'html.parser') 解析，html.parser 零依赖，lxml 更快")
print("  2. soup.标签名 / find / find_all 查元素；class_ 带下划线，id 直接传")
print("  3. .get_text() 取文字，['href'] 或 .get('href') 取属性，.get() 更安全")
print("  4. find 返回第一个，find_all 返回列表；爬虫常遍历 find_all('a') 收集链接")