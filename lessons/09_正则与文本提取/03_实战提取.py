"""实战提取 —— 从日志和文本中批量提取结构化数据

演示从模拟日志文本提取 IP、时间、HTTP 状态码、URL；从文本提取所有邮箱
和手机号；提取金额数字；re.compile 预编译及性能对比；实用日志解析场景。
只用 re 标准库，一定能跑。

运行: uv run python lessons/09_正则与文本提取/03_实战提取.py
"""
import re
import time


# 模拟一段 Web 服务器访问日志（Apache/Nginx 常见格式）
SAMPLE_LOG = """192.168.1.10 - - [24/Sep/2026:10:15:30 +0800] "GET /api/users HTTP/1.1" 200 1234
10.20.30.40 - - [24/Sep/2026:10:15:31 +0800] "POST /api/login HTTP/1.1" 401 567
172.16.0.5 - - [24/Sep/2026:10:15:35 +0800] "GET /index.html HTTP/1.1" 200 2048
8.8.8.8 - - [24/Sep/2026:10:15:40 +0800] "GET /static/logo.png HTTP/1.1" 304 0
192.168.1.20 - - [24/Sep/2026:10:15:42 +0800] "DELETE /api/order/123 HTTP/1.1" 500 89
203.0.113.7 - - [24/Sep/2026:10:15:50 +0800] "GET /search?q=python HTTP/1.1" 200 4096"""

# 模拟一段含邮箱、手机号、金额的混合文本
SAMPLE_TEXT = """
订单确认：客户张三，手机 13800138000，邮箱 zhangsan@example.com。
订单金额 1280.50 元，优惠 -50.00 元，实付 1230.50 元。
联系客服 400-123-4567 或 18500001111，邮箱 service@company.cn。
第二单客户李四 13912345678，邮箱 lisi.wang@sub.domain.org，金额 99.9 元。
国际客户 +86 13700138000，邮箱 john.doe@mail.co.uk，金额 1500.00 元。
"""


print("=" * 55)
print("1. 从日志提取 IP 地址")
print("=" * 55)
# IP 四段数字，每段 0-255；这里用简化版 \d{1,3}，严格版要限定范围
ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
ips = re.findall(ip_pattern, SAMPLE_LOG)
print(f"  日志共 {len(SAMPLE_LOG.splitlines())} 行")
print(f"  模式 r'\\b\\d{{1,3}}\\.\\d{{1,3}}\\.\\d{{1,3}}\\.\\d{{1,3}}\\b'")
print(f"  提取到的 IP:")
for i, ip in enumerate(ips, 1):
    print(f"    {i}. {ip}")
print("  -> \\b 是单词边界，防止匹配到 IP 中间一段；\\. 转义点号")
print("  -> 严格校验每段 0-255 要用更复杂模式或拆开判断，这里够用")

print("\n" + "=" * 55)
print("2. 从日志提取时间戳")
print("=" * 55)
# 时间格式 [24/Sep/2026:10:15:30 +0800]
time_pattern = r"\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) [+\-]\d{4}\]"
times = re.findall(time_pattern, SAMPLE_LOG)
print(f"  模式 r'\\[(\\d{{2}}/\\w{{3}}/\\d{{4}}:\\d{{2}}:\\d{{2}}:\\d{{2}}) [+\\-]\\d{{4}}\\]'")
print(f"  提取到的时间（捕获组只取日期时间部分）:")
for i, t in enumerate(times, 1):
    print(f"    {i}. {t}")
print("  -> 外层 \\[ \\] 匹配方括号本身；里面 () 捕获纯时间，去掉时区")
print("  -> \\w{3} 匹配月份缩写 Sep；[+\\-] 匹配 + 或 - 号")

print("\n" + "=" * 55)
print("3. 从日志提取 HTTP 状态码")
print("=" * 55)
# 状态码在请求方法后面，3 位数字，常见 200/301/404/500
status_pattern = r'" \d{3} '
statuses = re.findall(status_pattern, SAMPLE_LOG)
status_only = [s.strip().strip('"').strip() for s in statuses]
print(f"  模式 r'\" \\d{{3}} '  (引号+空格+3位数字+空格)")
print(f"  提取到的状态码: {status_only}")
# 统计各状态码出现次数
from collections import Counter
counter = Counter(status_only)
print(f"  状态码统计: {dict(counter)}")
print("  -> 状态码是 3 位数字，用 \\d{3} 匹配；前后加限定避免误匹配")
print("  -> 配合 collections.Counter 统计，是日志分析的常见组合")

print("\n" + "=" * 55)
print("4. 从日志提取请求方法和 URL")
print("=" * 55)
# "GET /api/users HTTP/1.1" 这种结构，用捕获组分别取方法和路径
req_pattern = r'"(\w+) (\S+) HTTP'
requests = re.findall(req_pattern, SAMPLE_LOG)
print(f"  模式 r'\"(\\w+) (\\S+) HTTP'  (方法 + 路径)")
print(f"  提取到的请求:")
for i, (method, url) in enumerate(requests, 1):
    print(f"    {i}. {method:6} {url}")
print("  -> \\w+ 匹配方法 GET/POST/DELETE；\\S+ 匹配非空白（URL 不含空格）")
print("  -> findall 有两个组返回元组列表，直接解包很方便")

print("\n" + "=" * 55)
print("5. 从文本提取所有邮箱地址")
print("=" * 55)
# 邮箱：用户名@域名，用户名可含 . _，域名可含多级 .
email_pattern = r"[\w.]+@[\w.]+\.\w{2,4}"
emails = re.findall(email_pattern, SAMPLE_TEXT)
print(f"  文本片段: {SAMPLE_TEXT.strip()[:60]}...")
print(f"  模式 r'[\\w.]+@[\\w.]+\\.\\w{{2,4}}'")
print(f"  提取到的邮箱:")
for i, e in enumerate(emails, 1):
    print(f"    {i}. {e}")
print("  -> [\\w.] 字母数字下划线和点；@ 后多级域名用 [\\w.]+ 匹配")
print("  -> 末尾 \\.\\w{2,4} 匹配顶级域名（com/cn/org/co.uk 简化处理）")

print("\n" + "=" * 55)
print("6. 从文本提取所有手机号")
print("=" * 55)
# 国内手机号：1 开头，第二位 3-9，共 11 位
phone_pattern = r"1[3-9]\d{9}"
phones = re.findall(phone_pattern, SAMPLE_TEXT)
print(f"  模式 r'1[3-9]\\d{{9}}'")
print(f"  提取到的手机号: {phones}")
print("  -> 1[3-9] 限定前两位（13x-19x），\\d{9} 后 9 位")
print("  -> 400-123-4567 和 +86 前缀不会被误匹配，因为格式对不上")

print("\n" + "=" * 55)
print("7. 从文本提取金额数字")
print("=" * 55)
# 金额：数字.数字，可能带负号；用捕获组只取数字部分
amount_pattern = r"(-?\d+\.\d{2})\s*元"
amounts = re.findall(amount_pattern, SAMPLE_TEXT)
print(f"  模式 r'(-?\\d+\\.\\d{{2}})\\s*元'")
print(f"  提取到的金额:")
for i, a in enumerate(amounts, 1):
    print(f"    {i}. {a} 元")
total = sum(float(a) for a in amounts)
print(f"  金额合计: {total:.2f} 元")
print("  -> -? 允许负号（优惠 -50.00）；\\d+\\.\\d{2} 整数+两位小数")
print("  -> \\s*元 限定后面跟'元'字，避免误匹配其他小数")

print("\n" + "=" * 55)
print("8. re.compile 预编译：把模式编译成 Pattern 对象")
print("=" * 55)
# 预编译后可重复使用，API 和 re 模块函数一致
compiled_ip = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
compiled_email = re.compile(r"[\w.]+@[\w.]+\.\w{2,4}")
print(f"  compiled_ip   = {compiled_ip}")
print(f"  compiled_email= {compiled_email}")
print(f"  compiled_ip.findall(SAMPLE_LOG) 前 3 个: {compiled_ip.findall(SAMPLE_LOG)[:3]}")
print(f"  compiled_email.findall(SAMPLE_TEXT) 前 2 个: {compiled_email.findall(SAMPLE_TEXT)[:2]}")
print("  -> compile 返回 Pattern 对象，有 match/search/findall/sub 等全部方法")
print("  -> 用法和 re.xxx 完全一样，只是把模式从字符串变成对象")

print("\n" + "=" * 55)
print("9. 预编译 vs 不编译：性能对比")
print("=" * 55)
# 高频调用时，预编译省去重复解析模式的开销
# re 模块内部有 LRU 缓存，所以差距没那么夸张，但循环里编译更明确
big_text = "test 192.168.1.1 end " * 10000
N = 1000

# 不预编译：每次都传模式字符串（命中 re 内部缓存）
start = time.perf_counter()
for _ in range(N):
    re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", big_text)
t_no_compile = time.perf_counter() - start

# 预编译：模式只解析一次
start = time.perf_counter()
pat = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
for _ in range(N):
    pat.findall(big_text)
t_compile = time.perf_counter() - start

print(f"  文本长度 {len(big_text)} 字符，循环 {N} 次:")
print(f"  不预编译: {t_no_compile:.3f} 秒")
print(f"  预编译  : {t_compile:.3f} 秒")
print(f"  加速比  : {t_no_compile / t_compile:.2f}x")
print("  -> re 内部有 LRU 缓存，差距不大；但循环里编译语义更清晰")
print("  -> 模式是常量就预编译，明确表达'这个模式只解析一次'")

print("\n" + "=" * 55)
print("10. 实战：完整解析一行日志成结构化数据")
print("=" * 55)
# 用一个大模式 + 命名分组一次性解析整行日志
log_pattern = re.compile(
    r"(?P<ip>\S+) "
    r"\S+ \S+ "
    r"\[(?P<time>[^\]]+)\] "
    r'"(?P<method>\w+) (?P<url>\S+) (?P<proto>[^"]+)" '
    r"(?P<status>\d{3}) "
    r"(?P<size>\d+)"
)
print(f"  日志模式（命名分组）:")
print(f"    ip / time / method / url / proto / status / size")
print(f"  解析结果:")
parsed = []
for line in SAMPLE_LOG.splitlines():
    m = log_pattern.search(line)
    if m:
        rec = m.groupdict()
        parsed.append(rec)
        print(f"    {rec['ip']:14} {rec['method']:6} {rec['url']:22} -> {rec['status']} ({rec['size']} 字节)")
print(f"  共解析 {len(parsed)} 条日志记录")
print("  -> 一个模式 + 命名分组把整行日志拆成字典，groupdict() 直接拿到")
print("  -> 这是日志分析的标准套路：写好模式，每行 search 一次")

print("\n" + "=" * 55)
print("11. 实战：按状态码分组统计")
print("=" * 55)
status_groups = {"2xx": [], "3xx": [], "4xx": [], "5xx": []}
for rec in parsed:
    code = int(rec["status"])
    if 200 <= code < 300:
        status_groups["2xx"].append(rec)
    elif 300 <= code < 400:
        status_groups["3xx"].append(rec)
    elif 400 <= code < 500:
        status_groups["4xx"].append(rec)
    elif 500 <= code < 600:
        status_groups["5xx"].append(rec)
print(f"  按状态码分组:")
for k, v in status_groups.items():
    print(f"    {k}: {len(v)} 条")
print("  -> 解析成字典后，统计分析就是普通 Python 数据处理")
print("  -> 正则负责'提取'，后续分析交给列表/字典/Counter 等标准工具")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. 提取 IP/邮箱/手机号/金额等结构化片段，是正则最常见实战场景")
print("  2. \\b 单词边界、\\. 转义点、\\S+ 非空白，是写实用模式的常用构件")
print("  3. re.compile 预编译模式成 Pattern 对象，循环高频调用时语义更清晰")
print("  4. 一个大模式 + 命名分组能把一行日志解析成字典，groupdict() 直接取")
print("  5. 正则负责'提取结构化片段'，后续统计/分析交给普通 Python 数据工具")
print("  6. 简化模式够用就行；严格校验（IP 每段 0-255、邮箱完整规范）要更复杂模式或专用库")