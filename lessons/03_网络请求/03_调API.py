"""调用公开 API —— 实战：拿 JSON、解析、遍历提取

演示调用 JSONPlaceholder 公开 API：获取用户列表、带参数查询、解析 JSON、异常处理。
API 返回 JSON，用 response.json() 直接解析成 Python 字典/列表，不用手动 json.loads。

运行: uv run python lessons/03_网络请求/03_调API.py
"""
import requests

# JSONPlaceholder：一个免费的假 REST API，专门给开发者练习用
# 返回 JSON 格式的模拟数据（用户、帖子、评论等）
API = "https://jsonplaceholder.typicode.com"


def safe_get(url, **kwargs):
    """带完整异常处理的 GET 请求：区分网络错误、404、非 JSON 响应"""
    try:
        resp = requests.get(url, timeout=15, **kwargs)
    except requests.exceptions.Timeout:
        print("  [超时] 服务器 15 秒内没响应，请检查网络")
        return None
    except requests.exceptions.ConnectionError:
        print("  [连接失败] 无法连接 API 服务器，请检查网络或 VPN")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  [请求错误] {type(e).__name__}: {e}")
        return None

    # 检查状态码
    if resp.status_code == 404:
        print(f"  [404] 资源不存在: {url}")
        return None
    if not resp.ok:
        print(f"  [HTTP {resp.status_code}] 请求失败: {resp.reason}")
        return None

    # 检查是否是 JSON
    content_type = resp.headers.get("Content-Type", "")
    if "json" not in content_type:
        print(f"  [格式错误] 期望 JSON，实际 Content-Type: {content_type}")
        return None
    return resp


print("=" * 55)
print("1. 获取用户列表：GET /users")
print("=" * 55)
print(f"  API: {API}/users")
resp = safe_get(f"{API}/users")
if resp is not None:
    users = resp.json()                  # 直接解析成 list[dict]
    print(f"  返回类型: {type(users).__name__}，共 {len(users)} 个用户")
    print(f"  第一个用户的字段: {list(users[0].keys())}")
    print("  前 3 个用户:")
    for u in users[:3]:
        print(f"    {u['id']:>2}. {u['name']:<20} email={u['email']}")
print("  -> .json() 把 JSON 数组解析成 Python list，每个对象是 dict")

print("\n" + "=" * 55)
print("2. 遍历提取字段：从嵌套结构里取数据")
print("=" * 55)
resp = safe_get(f"{API}/users")
if resp is not None:
    users = resp.json()
    # 演示提取嵌套字段（address.city 在嵌套字典里）
    print("  用户的公司和所在城市:")
    for u in users[:5]:
        company = u["company"]["name"]       # 嵌套字典
        city = u["address"]["city"]          # 嵌套字典
        print(f"    {u['name']:<20} 公司={company:<25} 城市={city}")
print("  -> API 数据常嵌套，按 dict['key']['subkey'] 逐层取")

print("\n" + "=" * 55)
print("3. 带参数查询：GET /posts?userId=1")
print("=" * 55)
# params 会被 requests 自动拼成 ?userId=1
params = {"userId": 1}
print(f"  API: {API}/posts，参数: {params}")
resp = safe_get(f"{API}/posts", params=params)
if resp is not None:
    posts = resp.json()
    print(f"  userId=1 的帖子数: {len(posts)}")
    print("  前 3 个帖子标题:")
    for p in posts[:3]:
        print(f"    [{p['id']}] {p['title'][:40]}")
print("  -> 查询参数用 params= 传字典，requests 自动拼 URL 和编码")

print("\n" + "=" * 55)
print("4. 获取单个资源：GET /users/1")
print("=" * 55)
resp = safe_get(f"{API}/users/1")
if resp is not None:
    user = resp.json()                  # 单个对象，解析成 dict
    print(f"  用户名: {user['name']}")
    print(f"  电话: {user['phone']}")
    print(f"  网站: {user['website']}")
    print(f"  经纬度: {user['address']['geo']['lat']}, {user['address']['geo']['lng']}")
print("  -> 单个资源返回对象（dict），列表资源返回数组（list）")

print("\n" + "=" * 55)
print("5. 错误处理演示：请求不存在的资源（404）")
print("=" * 55)
print(f"  请求: {API}/users/99999（不存在的用户）")
resp = safe_get(f"{API}/users/99999")
if resp is None:
    print("  -> safe_get 已捕获 404 并返回 None，脚本继续运行不崩溃")
else:
    print(f"  返回: {resp.json()}（空对象，API 设计如此）")

print("\n" + "=" * 55)
print("6. POST 创建资源：演示提交数据（JSONPlaceholder 不会真存）")
print("=" * 55)
new_post = {"title": "学 Python 自动化", "body": "requests 真好用", "userId": 1}
print(f"  POST 数据: {new_post}")
try:
    resp = requests.post(f"{API}/posts", json=new_post, timeout=15)
    if resp.ok:
        created = resp.json()
        print(f"  服务器返回: id={created.get('id')}（模拟分配的 ID）")
        print(f"  状态码: {resp.status_code}（201 Created）")
    else:
        print(f"  [HTTP {resp.status_code}] 创建失败")
except requests.exceptions.RequestException as e:
    print(f"  [网络错误] {type(e).__name__}: {e}")
print("  -> POST 用 json= 传 body，API 返回新建资源（含服务器分配的 id）")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. API 返回 JSON，用 resp.json() 直接解析成 dict/list，不用 json.loads")
print("  2. 嵌套数据按 dict['key']['subkey'] 逐层取，先 print 看结构再写代码")
print("  3. 异常处理要分情况：网络错误、404、非 JSON 响应，分别给不同提示")
print("  4. 查询参数用 params=，提交数据用 json=（POST）或 data=（表单）")