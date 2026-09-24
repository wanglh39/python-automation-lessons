"""urllib 标准库 —— 不装第三方也能发 HTTP 请求

演示 Python 内置 urllib：urlopen 发 GET、读响应、urlencode 编码参数、quote 编码中文。
urllib 是标准库，不用 pip install，但 API 繁琐；了解它有助于理解 requests 做了什么简化。

运行: uv run python lessons/03_网络请求/01_urllib标准库.py
"""
import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote
from urllib.error import URLError, HTTPError

# 测试站点：httpbin.org 会把你发的请求原样回显，适合学习
BASE = "https://httpbin.org"


def safe_get(url, timeout=10):
    """带异常处理的 urlopen 包装：网络不通时返回 None 而不是崩溃"""
    try:
        return urlopen(url, timeout=timeout)
    except HTTPError as e:
        print(f"  [HTTP 错误] 状态码 {e.code}: {e.reason}")
        return None
    except URLError as e:
        print(f"  [网络错误] {e.reason}")
        print("  -> 请检查网络连接或 VPN 设置")
        return None
    except Exception as e:
        print(f"  [未知错误] {type(e).__name__}: {e}")
        return None


print("=" * 55)
print("1. 最简单的 GET 请求：urlopen + read")
print("=" * 55)
print(f"  请求: {BASE}/get")
resp = safe_get(f"{BASE}/get")
if resp is not None:
    with resp:
        print(f"  状态码: {resp.status}")
        print(f"  响应头 Server: {resp.headers.get('Server')}")
        print(f"  响应头 Content-Type: {resp.headers.get('Content-Type')}")
        body = resp.read().decode("utf-8")   # read 返回字节，要手动 decode
        print(f"  响应体长度: {len(body)} 字符")
        print(f"  响应体前 80 字: {body[:80]}...")
print("  -> urllib 的 read() 返回字节串，必须自己 .decode('utf-8')")

print("\n" + "=" * 55)
print("2. 带查询参数：urlencode 编码后拼到 URL")
print("=" * 55)
# 手动拼参数：?key=value&key2=value2
params = {"page": 1, "size": 20, "sort": "desc"}
query = urlencode(params)              # page=1&size=20&sort=desc
url = f"{BASE}/get?{query}"
print(f"  原始参数: {params}")
print(f"  urlencode 后: {query}")
print(f"  完整 URL: {url}")
resp = safe_get(url)
if resp is not None:
    with resp:
        data = json.loads(resp.read().decode("utf-8"))
        # httpbin.org/get 会把你的请求参数回显在 args 字段
        print(f"  服务器收到的参数: {data.get('args')}")
print("  -> urllib 不会自动拼参数，要自己 urlencode 再用 ? 连到 URL")

print("\n" + "=" * 55)
print("3. 中文参数：quote 编码单个字符串")
print("=" * 55)
chinese = "张三"
encoded = quote(chinese)               # %E5%BC%A0%E4%B8%89
print(f"  原始中文: {chinese}")
print(f"  quote 编码: {encoded}")
# urlencode 也能处理中文（内部会调 quote）
params_cn = {"name": "张三", "city": "北京"}
query_cn = urlencode(params_cn)
print(f"  urlencode 中文参数: {query_cn}")
url = f"{BASE}/get?{query_cn}"
resp = safe_get(url)
if resp is not None:
    with resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"  服务器收到的中文参数: {data.get('args')}")
print("  -> URL 不允许直接写中文，必须 percent-encode（%E5%BC%A0...）")

print("\n" + "=" * 55)
print("4. POST 请求：要构造 Request 对象")
print("=" * 55)
# urllib 发 POST 比 GET 麻烦：要构造 Request，data 要 encode 成字节
post_data = urlencode({"username": "admin", "action": "login"}).encode("utf-8")
req = Request(f"{BASE}/post", data=post_data, method="POST")
print(f"  POST 到: {BASE}/post")
print(f"  表单数据: username=admin, action=login")
try:
    with urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"  状态码: {resp.status}")
        print(f"  服务器收到的表单: {data.get('form')}")
except (URLError, HTTPError) as e:
    print(f"  [网络错误] {e}")
except Exception as e:
    print(f"  [未知错误] {type(e).__name__}: {e}")
print("  -> 对比 requests：requests.post(url, data={...}) 一行搞定")

print("\n" + "=" * 55)
print("5. 设置请求头：User-Agent")
print("=" * 55)
# 有些网站会拒绝默认的 User-Agent (Python-urllib/3.x)
req = Request(f"{BASE}/get")
req.add_header("User-Agent", "MyBot/1.0")
req.add_header("X-Custom", "hello")
print(f"  请求头: User-Agent=MyBot/1.0, X-Custom=hello")
resp = safe_get(req)
if resp is not None:
    with resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"  服务器收到的 User-Agent: {data['headers'].get('User-Agent')}")
        print(f"  服务器收到的 X-Custom: {data['headers'].get('X-Custom')}")
print("  -> 设置请求头要构造 Request 再 add_header，比较繁琐")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. urllib 是标准库不用装，但 API 繁琐：read() 要手动 decode，POST 要构造 Request")
print("  2. 中文/特殊字符参数必须用 quote 或 urlencode 编码，不能直接拼到 URL")
print("  3. 网络请求必须 try/except，否则断网时脚本会直接崩溃")
print("  4. 了解 urllib 有助于理解 requests 做了哪些简化（下一节讲）")