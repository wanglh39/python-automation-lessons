"""requests 库 —— Python 最常用的 HTTP 客户端

演示 requests：get/post、params/data/json、headers、timeout、自动解码。
requests 是第三方库但极其常用，代码量比 urllib 少一半，自动解码，API 直观。

运行: uv run python lessons/03_网络请求/02_requests库.py
"""
import requests

BASE = "https://httpbin.org"


def safe_request(method, url, **kwargs):
    """带异常处理的请求包装：网络不通时返回 None 而不是崩溃"""
    try:
        return requests.request(method, url, timeout=10, **kwargs)
    except requests.exceptions.Timeout:
        print("  [超时] 服务器 10 秒内没响应，请检查网络")
        return None
    except requests.exceptions.ConnectionError:
        print("  [连接失败] 无法连接服务器，请检查网络或 VPN")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  [请求错误] {type(e).__name__}: {e}")
        return None


print("=" * 55)
print("1. 最简单的 GET：requests.get + text")
print("=" * 55)
print(f"  请求: {BASE}/get")
resp = safe_request("GET", f"{BASE}/get")
if resp is not None:
    print(f"  状态码: {resp.status_code}")
    print(f"  响应头 Content-Type: {resp.headers.get('Content-Type')}")
    print(f"  响应体长度: {len(resp.text)} 字符")
    print(f"  响应体前 80 字: {resp.text[:80]}...")
print("  -> 对比 urllib：不用 with，不用 read()，不用 decode()，直接 .text")

print("\n" + "=" * 55)
print("2. 带参数的 GET：params 自动编码（中文也不用管）")
print("=" * 55)
params = {"page": 1, "size": 20, "keyword": "张三"}   # 直接传字典
print(f"  传入 params: {params}")
resp = safe_request("GET", f"{BASE}/get", params=params)
if resp is not None:
    print(f"  实际请求 URL: {resp.url}")   # requests 自动拼好参数
    data = resp.json()                      # 直接解析成字典
    print(f"  服务器收到的参数: {data.get('args')}")
print("  -> params 自动 urlencode，中文自动编码，不用手动拼 URL")

print("\n" + "=" * 55)
print("3. POST 表单：data 参数")
print("=" * 55)
form_data = {"username": "admin", "password": "secret"}
print(f"  POST 表单: {form_data}")
resp = safe_request("POST", f"{BASE}/post", data=form_data)
if resp is not None:
    result = resp.json()
    print(f"  服务器收到的表单: {result.get('form')}")
print("  -> data=  发送表单（Content-Type: application/x-www-form-urlencoded）")

print("\n" + "=" * 55)
print("4. POST JSON：json 参数（调 API 最常用）")
print("=" * 55)
json_data = {"name": "张三", "age": 25, "tags": ["python", "自动化"]}
print(f"  POST JSON: {json_data}")
resp = safe_request("POST", f"{BASE}/post", json=json_data)
if resp is not None:
    result = resp.json()
    print(f"  服务器收到的 JSON: {result.get('json')}")
    print(f"  请求头 Content-Type: {result['headers'].get('Content-Type')}")
print("  -> json=  自动序列化成 JSON 并设 Content-Type: application/json")

print("\n" + "=" * 55)
print("5. 设置请求头：headers 参数")
print("=" * 55)
headers = {
    "User-Agent": "MyBot/1.0",        # 模拟浏览器或自定义客户端
    "Authorization": "Bearer my-token",  # 认证 token
    "X-Custom-Header": "hello",
}
print(f"  请求头: {headers}")
resp = safe_request("GET", f"{BASE}/get", headers=headers)
if resp is not None:
    data = resp.json()
    received = data["headers"]
    print(f"  服务器收到的 User-Agent: {received.get('User-Agent')}")
    print(f"  服务器收到的 Authorization: {received.get('Authorization')}")
print("  -> headers=  传字典，比 urllib 的 add_header 简洁得多")

print("\n" + "=" * 55)
print("6. 超时设置：timeout 防止请求卡死")
print("=" * 55)
print("  timeout=10 表示 10 秒内没响应就抛 Timeout 异常")
print("  也可以传元组: timeout=(连接超时, 读取超时)，如 timeout=(5, 30)")
# 演示一个会超时的请求（连一个不存在的端口）
print("  尝试连接不存在的地址（演示超时处理）:")
try:
    requests.get("https://httpbin.org/delay/30", timeout=3)
except requests.exceptions.Timeout:
    print("  [已捕获] 3 秒超时，请求被中止（没有卡死）")
except requests.exceptions.RequestException as e:
    print(f"  [已捕获] {type(e).__name__}: {e}")
print("  -> 不设 timeout 的话，网络异常时脚本会一直卡着，自动化脚本必须设")

print("\n" + "=" * 55)
print("7. 会话 Session：复用连接，多次请求更快")
print("=" * 55)
print("  用 Session 设置公共 headers，后续请求自动带上:")
with requests.Session() as s:
    s.headers.update({"User-Agent": "MyBot/1.0", "Authorization": "Bearer xxx"})
    try:
        r1 = s.get(f"{BASE}/get", timeout=10)
        r2 = s.get(f"{BASE}/get", timeout=10)
        print(f"  第 1 次请求状态: {r1.status_code}")
        print(f"  第 2 次请求状态: {r2.status_code}")
        print(f"  两次请求都带了 User-Agent: {r1.json()['headers'].get('User-Agent')}")
    except requests.exceptions.RequestException as e:
        print(f"  [网络错误] {type(e).__name__}: {e}")
print("  -> Session 复用 TCP 连接，多次请求同一域名时更快")

print("\n" + "=" * 55)
print("8. 响应对象的常用属性一览")
print("=" * 55)
resp = safe_request("GET", f"{BASE}/get", params={"x": 1})
if resp is not None:
    print(f"  resp.status_code  -> {resp.status_code}        (int，状态码)")
    print(f"  resp.ok           -> {resp.ok}             (bool，2xx 为 True)")
    print(f"  resp.url          -> {resp.url[:50]}...  (最终 URL，含参数)")
    print(f"  resp.text[:30]    -> {resp.text[:30]}...   (str，自动解码)")
    print(f"  resp.json()       -> {type(resp.json()).__name__}            (直接解析成 dict)")
    print(f"  resp.headers      -> {type(resp.headers).__name__}            (响应头，像字典)")
    print(f"  resp.encoding     -> {resp.encoding!r}           (自动推断的编码)")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. requests 比 urllib 简洁：params 自动编码、text 自动解码、json() 直接解析")
print("  2. POST 表单用 data=，POST JSON 用 json=（调 API 最常用）")
print("  3. 必须设 timeout，否则网络异常时脚本会卡死；用 try/except 友好处理")
print("  4. 多次请求同一站点用 Session，复用连接更快，还能统一设 headers")