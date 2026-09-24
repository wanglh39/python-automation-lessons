"""提取数据 —— 链接、表格、图片、CSS 选择器实战

演示从 HTML 提取结构化数据：所有链接、表格数据、CSS 选择器、图片 src。
用本地生成的 HTML 文件演示，不依赖网络，一定能跑。

运行: uv run python lessons/08_HTML解析爬虫/03_提取数据.py
"""
from pathlib import Path

from bs4 import BeautifulSoup


# sample 目录用来放测试 HTML，和脚本同目录
SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)


# 包含链接、表格、图片、多层嵌套的测试页面
SAMPLE_HTML = """<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="utf-8">
    <title>数据提取演示</title>
</head>
<body>
    <div id="header">
        <h1>商品列表</h1>
        <nav class="menu">
            <a href="/home">首页</a>
            <a href="/products">商品</a>
            <a href="/about">关于</a>
        </nav>
    </div>

    <div id="main">
        <table class="goods" id="goods-table">
            <tr><th>名称</th><th>价格</th><th>库存</th></tr>
            <tr><td>Python 书</td><td>59.00</td><td>10</td></tr>
            <tr><td>键盘</td><td>199.00</td><td>5</td></tr>
            <tr><td>鼠标</td><td>49.00</td><td>0</td></tr>
            <tr><td>显示器</td><td>899.00</td><td>3</td></tr>
        </table>

        <div class="gallery">
            <img src="/img/book.jpg" alt="Python 书封面">
            <img src="/img/keyboard.jpg" alt="键盘图片">
            <img src="/img/mouse.jpg" alt="鼠标图片">
        </div>

        <ul class="news">
            <li><a href="/news/1">新书上架</a> - 2024-01-01</li>
            <li><a href="/news/2">限时折扣</a> - 2024-01-05</li>
            <li><a href="/news/3">库存清仓</a> - 2024-01-10</li>
        </ul>
    </div>

    <div id="footer">
        <a href="/privacy">隐私政策</a>
        <a href="/contact">联系我们</a>
    </div>
</body>
</html>
"""


def prepare_sample():
    """把测试 HTML 写到 sample 目录，返回文件路径"""
    path = SAMPLE_DIR / "data_demo.html"
    path.write_text(SAMPLE_HTML, encoding="utf-8")
    return path


# 先准备并解析 HTML
html_path = prepare_sample()
soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")


print("=" * 55)
print("1. 提取所有链接：find_all('a')")
print("=" * 55)
print(f"  测试文件: {html_path}")
all_links = soup.find_all("a", href=True)
print(f"  共 {len(all_links)} 个链接:")
for i, a in enumerate(all_links, 1):
    text = a.get_text(strip=True)
    href = a["href"]
    print(f"    {i}. {text!r} -> {href}")
print("  -> href=True 过滤无 href 的 a；爬虫常这么收集页面里的全部超链接")

print("\n" + "=" * 55)
print("2. 提取表格数据：遍历 tr / td")
print("=" * 55)
table = soup.find("table", id="goods-table")
print(f"  找到表格: {table.get('id')!r}, class={table.get('class')}")
rows = []
for tr in table.find_all("tr"):
    cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
    rows.append(cells)
print(f"  共 {len(rows)} 行（含表头）:")
for row in rows:
    print(f"    {row}")
print("  -> 每行 tr 里找 td/th，get_text(strip=True) 去空白，得到二维列表")

print("\n" + "=" * 55)
print("3. 把表格转成字典列表（更实用的结构）")
print("=" * 55)
header = rows[0]
data_rows = rows[1:]
records = [dict(zip(header, row)) for row in data_rows]
print(f"  表头: {header}")
for rec in records:
    print(f"    {rec}")
print("  -> dict(zip(表头, 行)) 是把表格转成字典列表的常用技巧")

print("\n" + "=" * 55)
print("4. CSS 选择器：soup.select / select_one")
print("=" * 55)
print("  4.1 select('nav.menu a') —— 导航菜单里的链接:")
nav_links = soup.select("nav.menu a")
for a in nav_links:
    print(f"      {a.get_text(strip=True)!r} -> {a['href']}")
print("      -> CSS 选择器：nav.menu 表示 class=menu 的 nav，空格表示后代")

print("\n  4.2 select_one('#header h1') —— id=header 下的第一个 h1:")
header_h1 = soup.select_one("#header h1")
print(f"      {header_h1!r}")
print(f"      文字: {header_h1.get_text(strip=True)!r}")
print("      -> #header 表示 id=header，select_one 返回第一个匹配")

print("\n  4.3 select('div.gallery img') —— 画廊里的图片:")
gallery_imgs = soup.select("div.gallery img")
for img in gallery_imgs:
    print(f"      src={img['src']!r}, alt={img.get('alt')!r}")
print("      -> CSS 选择器层层定位，比 find 嵌套写法更简洁")

print("\n  4.4 select('ul.news li a') —— 新闻列表里的链接:")
news_links = soup.select("ul.news li a")
for a in news_links:
    print(f"      {a.get_text(strip=True)!r} -> {a['href']}")
print("      -> 同样的链接用 find_all 也能找，select 在结构深时更直观")

print("\n" + "=" * 55)
print("5. 提取所有图片 src")
print("=" * 55)
all_imgs = soup.find_all("img")
print(f"  共 {len(all_imgs)} 张图片:")
for i, img in enumerate(all_imgs, 1):
    print(f"    {i}. src={img['src']!r}, alt={img.get('alt')!r}")
print("  -> 下载图片就是拿到 src 再 requests.get(src)，注意相对路径要拼域名")

print("\n" + "=" * 55)
print("6. find_all 多标签 + 属性过滤")
print("=" * 55)
# 同时找 h1 和 h2
headings = soup.find_all(["h1", "h2"])
print(f"  所有 h1/h2 标题: {[h.get_text(strip=True) for h in headings]}")
# 找 class 含 menu 的元素
menu_elems = soup.find_all(class_="menu")
print(f"  class='menu' 的元素: {[type(e).__name__ for e in menu_elems]}")
# 找带 alt 属性的图片
imgs_with_alt = soup.find_all("img", alt=True)
print(f"  带 alt 属性的图片数: {len(imgs_with_alt)}")
print("  -> find_all 可传标签列表、class_、属性条件，组合过滤很灵活")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. find_all('a', href=True) 提取所有链接；遍历 tr/td 提取表格成二维列表")
print("  2. dict(zip(表头, 行)) 把表格转成字典列表，是爬虫常用数据结构")
print("  3. soup.select('CSS选择器') 按结构定位，深层嵌套比 find 链更简洁")
print("  4. select 返回列表，select_one 返回第一个；#id、.class、空格后代都支持")
print("  5. 提取图片 src 后拼完整 URL 再 requests.get 下载；相对路径要补域名")