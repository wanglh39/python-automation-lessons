# 模块 8：HTML 解析爬虫

> 模块 3 学了 requests 抓网页，拿到的是一大段 HTML 文本——要从中取出标题、链接、表格数据，就得"解析 HTML"。正则太难写、容易漏，BeautifulSoup 是 Python 爬虫的事实标准：把 HTML 变成一棵树，用标签名、class、id、CSS 选择器精准定位元素，再取文本和属性。本模块从本地 HTML 起步（不依赖网络一定能跑），再到 requests + bs4 完整流程，最后落到提取链接、表格、图片等实战场景。

## 核心库一览

| 库 | 来源 | 用途 | 推荐度 |
|---|:---:|---|:---:|
| `requests` | 第三方 | 抓网页 HTML（模块 3 已学），给 bs4 提供原料 | ★★★★★ |
| `beautifulsoup4` | 第三方 | 解析 HTML/XML，按标签/class/id/CSS 选择器定位元素 | ★★★★★ |
| `lxml` | 第三方 | C 实现的高速解析器，可作 bs4 后端，也能直接用 XPath | ★★★★ |
| `html.parser` | 标准库 | Python 自带的 HTML 解析器，bs4 的默认后端之一 | ★★★ |

> `beautifulsoup4` 是解析层的高层 API，底层解析器可在 `html.parser`（标准库，零依赖）、`lxml`（最快，需安装）、`html5lib`（最容错，慢）之间切换。本模块示例统一用 `html.parser`，保证不装 lxml 也能跑；追求速度时把 `'html.parser'` 换成 `'lxml'` 即可。

## bs4 vs lxml vs re：解析方式对比

**正则 re**：把 HTML 当纯文本匹配，看似万能实则脆弱——标签嵌套、属性顺序、换行空格都会让正则失效，维护噩梦。
```python
import re
# 想提取所有链接，正则写法（容易漏掉换行、单引号、多属性的情况）
links = re.findall(r'<a href="([^"]+)">', html)
```

**BeautifulSoup**：把 HTML 解析成一棵树，按结构定位，容错好、API 友好，是绝大多数爬虫的首选。
```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
links = [a['href'] for a in soup.find_all('a', href=True)]
```

**lxml / XPath**：C 实现，速度最快，XPath 表达力强，适合大体积或结构固定的 XML/HTML；API 没 bs4 直观。
```python
from lxml import html as lxml_html
tree = lxml_html.fromstring(html)
links = tree.xpath('//a/@href')
```

| 对比项 | 正则 re | BeautifulSoup | lxml + XPath |
|---|---|---|---|
| 思路 | 文本匹配 | 解析成树，按结构查 | 解析成树，XPath 查 |
| 容错性 | 差（标签一变就漏） | 好（坏 HTML 也能解析） | 中（要求相对规范） |
| 速度 | 快（但写对难） | 中（够用） | 最快（C 实现） |
| 学习成本 | 看似低实则高 | 低，API 直观 | 中，要学 XPath 语法 |
| 适用场景 | 简单固定文本 | 绝大多数 HTML 爬虫 | 大体积、性能敏感、XML |

> **经验法则**：抓 HTML 优先 BeautifulSoup，解析器先用 `html.parser`（零依赖），量大或求速度再装 lxml 换后端。正则只用来处理 HTML 之外的纯文本（日志、配置）。XPath 在结构固定、要批量提取时很顺手，可以单独学 lxml。

## 核心 API 速查

```python
from bs4 import BeautifulSoup

# --- 解析 ---
soup = BeautifulSoup(html_string, 'html.parser')   # 标准库后端，零依赖
soup = BeautifulSoup(html_string, 'lxml')           # lxml 后端，最快（需安装）
soup = BeautifulSoup(resp.text, 'html.parser')      # 配合 requests

# --- 直接取标签（取第一个）---
soup.title                  # <title> 标签元素
soup.title.string           # 标签里的文字
soup.p                      # 第一个 <p>
soup.a['href']              # 第一个 <a> 的 href 属性

# --- find / find_all：按条件查 ---
soup.find('h1')                              # 第一个 h1
soup.find_all('p')                           # 所有 p，返回列表
soup.find('div', id='main')                  # id='main' 的 div
soup.find_all('div', class_='article')       # class 含 article 的 div
soup.find_all('a', limit=5)                  # 只取前 5 个
soup.find_all(['h1', 'h2', 'h3'])            # 多种标签一起查

# --- CSS 选择器：soup.select / select_one ---
soup.select('div.article a')                 # 所有 article 下的 a，返回列表
soup.select_one('#main h1')                  # id=main 下的第一个 h1
soup.select('ul > li:first-child')           # 支持 CSS 伪类（lxml 后端更全）

# --- 取数据 ---
elem.get_text()            # 取所有文字（含子标签），自动拼接
elem.get_text(strip=True)  # 去掉首尾空白
elem['href']               # 取属性（KeyError 若不存在）
elem.get('href')           # 取属性，不存在返回 None（更安全）
elem.attrs                 # 所有属性的字典
```

```python
# --- 配合 requests 的完整流程 ---
import requests
from bs4 import BeautifulSoup

resp = requests.get("https://example.com", timeout=10)
resp.raise_for_status()                          # 状态码非 2xx 抛异常
soup = BeautifulSoup(resp.text, 'html.parser')
print(soup.title.string)
for a in soup.find_all('a', href=True):
    print(a.get_text(strip=True), a['href'])
```

```python
# --- 遍历表格 ---
table = soup.find('table')
for tr in table.find_all('tr'):
    cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
    print(cells)                                 # 每行一个列表
```

## 本模块示例

| 脚本 | 演示 |
|---|---|
| [01_解析本地HTML.py](01_解析本地HTML.py) | 自动生成测试 HTML、BeautifulSoup 解析、soup.title/find/find_all、按标签/class/id 查、取文本和属性 |
| [02_配合requests抓取.py](02_配合requests抓取.py) | requests.get 抓网页 + bs4 解析完整流程、状态码检查、网络不通优雅提示 |
| [03_提取数据.py](03_提取数据.py) | 提取所有链接、遍历表格 tr/td、CSS 选择器 select/select_one、提取图片 src |

运行方式：
```bash
uv run python lessons/08_HTML解析爬虫/01_解析本地HTML.py
uv run python lessons/08_HTML解析爬虫/02_配合requests抓取.py
uv run python lessons/08_HTML解析爬虫/03_提取数据.py
```

> 01 和 03 用本地生成的 HTML 演示，不依赖网络，一定能跑。02 需要联网抓 example.com / python.org，网络不通时打印友好提示，不会崩溃。脚本会在 `sample/` 目录下生成测试 HTML 文件，不碰你真实文件。

## 底层原理（简单了解）

1. **HTML 解析成树**：浏览器和 bs4 都把 HTML 解析成一棵 DOM 树。`<html>` 是根，`<head>`/`<body>` 是子节点，层层嵌套。`soup.find('p')` 本质是遍历这棵树找第一个 `<p>` 节点，`a['href']` 是读该节点的属性。理解了树结构，"父节点/子节点/兄弟节点"这些概念就顺了：`elem.parent`、`elem.children`、`elem.find_next_sibling()` 都是树上操作。
2. **bs4 底层可换解析器**：BeautifulSoup 自己不解析 HTML，它把活儿交给后端解析器：`html.parser`（Python 标准库写，纯 Python，慢但零依赖）、`lxml`（C 写，最快，需安装）、`html5lib`（纯 Python，最容错，最慢）。所以 `BeautifulSoup(html, 'lxml')` 比 `BeautifulSoup(html, 'html.parser')` 快几倍，但代码完全一样——换后端只改一个字符串。坏 HTML（标签没闭合、嵌套错乱）用 `html5lib` 或 `lxml` 容错更好。
3. **CSS 选择器 vs XPath**：两者都是"在树里找节点"的表达式，思路不同。CSS 选择器（`soup.select`）走前端路线，写法和写 CSS 一样（`div.article > a`、`#main h1`），前端熟悉、够用；XPath（lxml 的 `tree.xpath`）走 XML 路线，表达力更强（能"取父节点""取第 N 个""按文本内容筛"），但语法更绕（`//div[@class='article']/a/@href`）。抓网页优先 CSS 选择器，结构复杂或要向上找父节点时再上 XPath。
4. **get_text() 为什么能拼子标签文字**：`<p>你好 <b>世界</b>！</p>` 的 `.get_text()` 返回 `"你好 世界！"`，因为它递归把所有后代节点的文字拼起来。想只取直接文字用 `.string`（仅当只有一个文本子节点时返回，否则 None）。`strip=True` 去首尾空白，处理换行缩进很方便。