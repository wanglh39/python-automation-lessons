# 模块 3：网络请求与爬虫

> 自动化脚本经常要"上网"：调接口拿数据、下载文件、抓网页。Python 标准库自带 `urllib` 能发请求，但大家更爱用第三方库 `requests`——代码少一半、自动解码、API 直观。本模块从 urllib 起步，再到 requests，最后落到实际场景：调 API 拿 JSON、下载文件带进度。

## 核心库一览

| 库 | 来源 | 用途 | 推荐度 |
|---|:---:|---|:---:|
| `urllib` | 标准库 | 发 HTTP 请求，**零依赖**，但 API 繁琐 | ★★ |
| `requests` | 第三方 | 发 HTTP 请求，**事实标准**，代码简洁 | ★★★★★ |
| `json` | 标准库 | 解析 JSON 响应（requests 的 `.json()` 内部就用它） | ★★★★ |

## requests vs urllib：为什么推荐 requests

**urllib 是标准库**，不用安装，但写法啰嗦：
```python
# urllib：发个带参数的 GET 请求
from urllib.request import urlopen
from urllib.parse import urlencode
url = "https://httpbin.org/get?" + urlencode({"key": "值", "page": 1})
with urlopen(url, timeout=10) as resp:
    body = resp.read().decode("utf-8")   # 要手动 decode
print(resp.status, body[:50])
```

**requests 是第三方库**，要 `pip install requests`，但代码量少一半：
```python
# requests：同样的请求
import requests
resp = requests.get("https://httpbin.org/get",
                    params={"key": "值", "page": 1}, timeout=10)
print(resp.status_code, resp.text[:50])   # text 已自动解码
```

> **经验法则**：写自动化脚本无脑选 `requests`。只有在"不能装第三方库"的受限环境（比如某些服务器、嵌入式 Python）才退而求其次用 `urllib`。本模块两个都讲，先 urllib 知其所以然，再 requests 实战。

## 核心 API 速查

```python
# --- urllib（标准库，不用安装）---
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote

# GET 请求
with urlopen("https://example.com", timeout=10) as resp:
    status = resp.status          # 状态码
    body = resp.read().decode()   # 读字节并解码
    headers = resp.headers        # 响应头

# 带查询参数：手动 urlencode 再拼到 URL
url = "https://httpbin.org/get?" + urlencode({"q": "中文", "n": 10})

# POST 请求：要构造 Request 对象
req = Request("https://httpbin.org/post",
              data=urlencode({"name": "张三"}).encode(),
              method="POST")
with urlopen(req) as resp:
    print(resp.read().decode())
```

```python
# --- requests（第三方，推荐）---
import requests

# GET
resp = requests.get("https://httpbin.org/get",
                    params={"q": "中文", "n": 10},   # 自动编码
                    timeout=10)
resp.status_code    # 200
resp.text           # 响应文本（自动解码）
resp.json()         # 直接解析成 dict/list
resp.headers        # 响应头

# POST
requests.post("https://httpbin.org/post",
              data={"name": "张三"},        # 表单
              json={"name": "张三"},        # JSON body（二选一）
              headers={"User-Agent": "bot"},
              timeout=10)

# 会话（多次请求复用连接）
with requests.Session() as s:
    s.headers["User-Agent"] = "bot"
    r1 = s.get("https://httpbin.org/get")
    r2 = s.get("https://httpbin.org/anything")

# 下载大文件：流式
with requests.get(url, stream=True) as r:
    for chunk in r.iter_content(8192):
        f.write(chunk)
```

## 本模块示例

| 脚本 | 演示 |
|---|---|
| [01_urllib标准库.py](01_urllib标准库.py) | urlopen 发 GET、urlencode 编码参数、quote 编码中文、读响应 |
| [02_requests库.py](02_requests库.py) | get/post、params/data/json、headers、timeout、对比 urllib |
| [03_调API.py](03_调API.py) | 调 JSONPlaceholder 公开 API，解析 JSON，遍历提取字段，异常处理 |
| [04_下载文件.py](04_下载文件.py) | 简单下载、流式下载大文件、显示进度条 |

运行方式：
```bash
uv run python lessons/03_网络请求/01_urllib标准库.py
uv run python lessons/03_网络请求/02_requests库.py
uv run python lessons/03_网络请求/03_调API.py
uv run python lessons/03_网络请求/04_下载文件.py
```

脚本会下载文件到 `sample/` 目录，不碰你真实文件。网络不通时打印友好提示，不会崩溃。

## 底层原理（简单了解）

1. **HTTP 请求过程**：发请求 = 建立 TCP 连接 → 发请求行+头+体 → 收响应行+头+体 → 关连接。`urlopen` / `requests.get` 把这些全包了，你只管传 URL 和参数。HTTPS 多一层 TLS 握手，Python 自动处理证书验证。
2. **urllib 底层是 http.client**：`urllib.request` 是高层封装，底层调 `http.client.HTTPConnection`，再底层是 socket。所以 urllib 不用装，但层级多，API 拼凑感强（发 POST 要自己构造 Request 对象）。
3. **requests 底层是 urllib3**：`requests` 不是从零写的，它封装了 `urllib3`（一个比 urllib 更好用的底层库，连接池、重试都内置）。所以 `requests` = 好用的高层 API + 稳定的底层实现，这就是它代码简洁又可靠的原因。
4. **JSON 响应为什么要 `.json()`**：HTTP 传的是文本/字节，`.text` 拿到字符串，`.json()` 内部调标准库 `json.loads()` 把字符串解析成 Python 字典/列表。所以 `resp.json()` 等价于 `json.loads(resp.text)`，只是少写一步。