"""配合 requests 抓取 —— requests + BeautifulSoup 完整流程

演示真实爬虫流程：requests.get 抓网页 -> 检查状态码 -> BeautifulSoup 解析 -> 提取数据。
网络不通时优雅提示，不崩溃。用 example.com 和 python.org 测试。

运行: uv run python lessons/08_HTML解析爬虫/02_配合requests抓取.py
"""
import requests
from bs4 import BeautifulSoup


def fetch(url, timeout=10):
    """带异常处理的请求包装：网络不通时返回 None 而不是崩溃"""
    try:
        return requests.get(url, timeout=timeout)
    except requests.exceptions.Timeout:
        print(f"  [超时] {timeout} 秒内没响应，请检查网络")
        return None
    except requests.exceptions.ConnectionError:
        print(f"  [连接失败] 无法连接 {url}，请检查网络或 VPN")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  [请求错误] {type(e).__name__}: {e}")
        return None


print("=" * 55)
print("1. 完整流程：请求 -> 检查状态码 -> 解析 -> 提取")
print("=" * 55)
url = "https://example.com"
print(f"  抓取: {url}")
resp = fetch(url)
if resp is None:
    print("  网络不通，跳过本节演示。")
else:
    print(f"  状态码: {resp.status_code}")
    print(f"  响应长度: {len(resp.text)} 字符")
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")
        print(f"  解析完成，页面标题: {soup.title.string!r}")
        print(f"  第一个 h1: {soup.find('h1')!r}")
        first_p = soup.find("p")
        if first_p:
            print(f"  第一个 p 文字: {first_p.get_text(strip=True)!r}")
        print("  -> 这就是爬虫四步走：抓 -> 验 -> 解析 -> 提取")
    else:
        print(f"  状态码非 200，响应可能异常")

print("\n" + "=" * 55)
print("2. raise_for_status：状态码非 2xx 自动抛异常")
print("=" * 55)
print("  resp.raise_for_status() 在 404/500 时抛 HTTPError，比手动判断更省事")
resp = fetch(url)
if resp is not None:
    try:
        resp.raise_for_status()
        print(f"  状态码 {resp.status_code} 正常，没有抛异常")
    except requests.exceptions.HTTPError as e:
        print(f"  [HTTP 错误] {type(e).__name__}: {e}")
print("  -> 爬虫里常用：resp.raise_for_status() 一行搞定状态码校验")

print("\n" + "=" * 55)
print("3. 提取页面所有链接：find_all('a')")
print("=" * 55)
resp = fetch(url)
if resp is not None and resp.status_code == 200:
    soup = BeautifulSoup(resp.text, "html.parser")
    links = soup.find_all("a", href=True)
    print(f"  example.com 共 {len(links)} 个带 href 的链接:")
    for i, a in enumerate(links, 1):
        print(f"    {i}. {a.get_text(strip=True)!r} -> {a['href']}")
    if not links:
        print("    (example.com 页面很简单，可能没有链接)")
print("  -> href=True 过滤掉没有 href 属性的 a 标签，避免 KeyError")

print("\n" + "=" * 55)
print("4. 抓更丰富的页面：python.org")
print("=" * 55)
url2 = "https://www.python.org"
print(f"  抓取: {url2}")
resp2 = fetch(url2)
if resp2 is None:
    print("  网络不通，跳过本节演示。")
else:
    print(f"  状态码: {resp2.status_code}")
    if resp2.status_code == 200:
        soup2 = BeautifulSoup(resp2.text, "html.parser")
        print(f"  页面标题: {soup2.title.string!r}")
        # 顶部导航通常在 nav 或 ul 中
        nav_links = soup2.select("ul.menu li a")
        print(f"  导航菜单链接数: {len(nav_links)}")
        for i, a in enumerate(nav_links[:5], 1):
            print(f"    {i}. {a.get_text(strip=True)!r} -> {a.get('href')}")
        if len(nav_links) > 5:
            print(f"    ... 还有 {len(nav_links) - 5} 个")
        all_links = soup2.find_all("a", href=True)
        print(f"  页面全部链接数: {len(all_links)}")
print("  -> 真实页面结构复杂，用 CSS 选择器 select() 精准定位导航")

print("\n" + "=" * 55)
print("5. 设置 User-Agent：有些网站会拦默认请求头")
print("=" * 55)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
}
print(f"  用浏览器 User-Agent 请求 {url}")
try:
    resp3 = requests.get(url, headers=headers, timeout=10)
    print(f"  状态码: {resp3.status_code}")
    print(f"  响应长度: {len(resp3.text)} 字符")
except requests.exceptions.RequestException as e:
    print(f"  [请求失败] {type(e).__name__}: {e}")
print("  -> requests 默认 User-Agent 是 'python-requests/x.x'，有的网站会拦")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. 爬虫四步走：requests.get 抓 -> 检查状态码 -> BeautifulSoup 解析 -> 提取数据")
print("  2. resp.raise_for_status() 一行校验状态码，非 2xx 自动抛异常")
print("  3. 网络请求必须 try/except，处理 Timeout/ConnectionError，别让脚本崩溃")
print("  4. 真实页面结构复杂，CSS 选择器 select() 比层层 find 更简洁精准")
print("  5. 有的网站拦默认 User-Agent，伪装成浏览器请求头能解决一部分")