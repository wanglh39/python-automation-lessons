"""基础匹配 —— re.match / search / findall 与常用元字符

演示正则最基础的三个查找函数：match 从开头匹配、search 搜索任意位置、
findall 找全部；常用元字符 . * + ? ^ $ \d \w \s；re.IGNORECASE 标志；
匹配手机号、邮箱等简单模式。只用 re 标准库，一定能跑。

运行: uv run python lessons/09_正则与文本提取/01_基础匹配.py
"""
import re


print("=" * 55)
print("1. re.match：从字符串开头匹配")
print("=" * 55)
# match 要求从位置 0 开始就能匹配上，否则返回 None
m1 = re.match(r"Hello", "Hello world")
m2 = re.match(r"world", "Hello world")
print(f"  re.match(r'Hello', 'Hello world') = {m1!r}")
print(f"    m1.group() = {m1.group()!r}  匹配到的文字")
print(f"    m1.span()  = {m1.span()}    匹配的起止位置")
print(f"  re.match(r'world', 'Hello world') = {m2!r}")
print("  -> match 只看开头，开头不是 world 就返回 None")
print("  -> 想在任意位置找，用 search 或 findall")

print("\n" + "=" * 55)
print("2. re.search：在任意位置搜索第一个匹配")
print("=" * 55)
s1 = "订单号 ORD-2026-09-24 已发货"
m3 = re.search(r"\d{4}-\d{2}-\d{2}", s1)
print(f"  文本: {s1!r}")
print(f"  re.search(r'\\d{{4}}-\\d{{2}}-\\d{{2}}', s1) = {m3!r}")
print(f"    匹配到: {m3.group()!r}  位置: {m3.span()}")
print("  -> \\d 表示数字，{4} 表示重复 4 次；search 找到第一个就返回")
print("  -> match 从开头找，search 在任意位置找——这是最常用的两个")

print("\n" + "=" * 55)
print("3. re.findall：找出全部匹配，返回列表")
print("=" * 55)
text = "今天 2026-09-24，截止 2026-12-31，开始 2027-01-01"
all_dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
print(f"  文本: {text!r}")
print(f"  所有日期: {all_dates}")
print(f"  共 {len(all_dates)} 个")
print("  -> findall 返回所有匹配的列表；没有组时返回字符串列表")
print("  -> 找不到返回空列表 []，不会抛异常，比 search 更省判断")

print("\n" + "=" * 55)
print("4. match vs search vs findall 三者对比")
print("=" * 55)
sample = "电话 13800138000，备用 13912345678"
print(f"  文本: {sample!r}")
r_match = re.match(r"\d{11}", sample)
r_search = re.search(r"\d{11}", sample)
r_findall = re.findall(r"\d{11}", sample)
print(f"  match(r'\\d{{11}}')   = {r_match!r}  (开头不是数字，匹配不到)")
print(f"  search(r'\\d{{11}}')  = {r_search.group()!r}  (找到第一个 11 位数字)")
print(f"  findall(r'\\d{{11}}') = {r_findall}  (找到全部 11 位数字)")
print("  -> match 严格从头；search 找第一个；findall 找全部")

print("\n" + "=" * 55)
print("5. 常用元字符演示：. * + ? ^ $")
print("=" * 55)
# . 匹配任意一个字符（不含换行）
print(f"  re.findall(r'a.c', 'abc adc a_c a\\nc') = {re.findall(r'a.c', 'abc adc a_c a\nc')}")
print("    -> . 匹配任意一个字符，但不匹配换行符")
# * 0 次或多次，+ 1 次或多次
print(f"  re.findall(r'ab*c', 'ac abc abbc') = {re.findall(r'ab*c', 'ac abc abbc')}")
print(f"  re.findall(r'ab+c', 'ac abc abbc') = {re.findall(r'ab+c', 'ac abc abbc')}")
print("    -> * 允许 0 次（ac 也算），+ 至少 1 次（ac 不算）")
# ? 0 次或 1 次
print(f"  re.findall(r'colou?r', 'color colour') = {re.findall(r'colou?r', 'color colour')}")
print("    -> ? 表示可选，u? 让 u 可有可无（英美拼写都匹配）")
# ^ 开头 $ 结尾
print(f"  re.search(r'^Hello', 'Hello world') = {re.search(r'^Hello', 'Hello world')!r}")
print(f"  re.search(r'^Hello', 'say Hello')   = {re.search(r'^Hello', 'say Hello')!r}")
print(f"  re.search(r'end$',   'the end')     = {re.search(r'end$', 'the end')!r}")
print("    -> ^ 匹配开头，$ 匹配结尾，常用来限定整行格式")

print("\n" + "=" * 55)
print("6. 字符类简写：\\d \\w \\s 和大写取反")
print("=" * 55)
mixed = "abc 123 def 456 ghi"
print(f"  文本: {mixed!r}")
print(f"  \\d+ (数字)      : {re.findall(r'\d+', mixed)}")
print(f"  \\D+ (非数字)    : {re.findall(r'\D+', mixed)}")
print(f"  \\w+ (字母数字_) : {re.findall(r'\w+', mixed)}")
print(f"  \\s+ (空白)      : {re.findall(r'\s+', mixed)!r}")
print("  -> \\d 数字 \\w 字母数字下划线 \\s 空白；大写是对应的取反")

print("\n" + "=" * 55)
print("7. 字符集 [...] 和取反 [^...]")
print("=" * 55)
print(f"  [aeiou] 找元音  : {re.findall(r'[aeiou]', 'hello world')}")
print(f"  [a-z]+  连续小写 : {re.findall(r'[a-z]+', 'Hello World 2026')}")
print(f"  [^0-9]+ 连续非数字: {re.findall(r'[^0-9]+', 'abc123def456')}")
print("  -> [...] 匹配其中任一字符；[^...] 取反；可写范围 a-z 0-9")

print("\n" + "=" * 55)
print("8. re.IGNORECASE 忽略大小写")
print("=" * 55)
text_mixed = "Python python PYTHON pyThon"
print(f"  文本: {text_mixed!r}")
no_flag = re.findall(r"python", text_mixed)
with_flag = re.findall(r"python", text_mixed, re.IGNORECASE)
print(f"  不加标志 findall(r'python')            = {no_flag}")
print(f"  加 re.IGNORECASE findall(r'python', I) = {with_flag}")
print("  -> IGNORECASE 让模式忽略大小写；也可简写 re.I；常用于匹配关键字")

print("\n" + "=" * 55)
print("9. 实战：匹配手机号")
print("=" * 55)
# 国内手机号：1 开头，第二位 3-9，共 11 位数字
phone_pattern = r"1[3-9]\d{9}"
contacts = "联系方式：13800138000，办公室 010-12345678，备用 19912345678"
phones = re.findall(phone_pattern, contacts)
print(f"  文本: {contacts!r}")
print(f"  模式 r'1[3-9]\\d{{9}}' (1 开头 + 3-9 + 9 位数字)")
print(f"  匹配到的手机号: {phones}")
print("  -> 1[3-9] 限定前两位，\\d{9} 后面 9 位数字；固定电话 010-... 不匹配")

print("\n" + "=" * 55)
print("10. 实战：匹配邮箱地址")
print("=" * 55)
# 简化版邮箱：字母数字_.@字母数字.字母（2-4位）
email_pattern = r"[\w.]+@[\w.]+\.\w{2,4}"
text_email = "联系 alice@example.com 或 bob.smith@company.cn，勿发 test@x"
emails = re.findall(email_pattern, text_email)
print(f"  文本: {text_email!r}")
print(f"  模式 r'[\\w.]+@[\\w.]+\\.\\w{{2,4}}'")
print(f"  匹配到的邮箱: {emails}")
print("  -> 这是简化版，真实邮箱规范更复杂；实际项目可用更严格模式或库")
print("  -> 注意 . 在字符集 [...] 里就是普通点，不用转义")

print("\n" + "=" * 55)
print("11. re.fullmatch：要求整个字符串都匹配")
print("=" * 55)
# fullmatch 等价于 ^...$，要求从头到尾整体匹配
print(f"  re.fullmatch(r'\\d+', '12345')    = {re.fullmatch(r'\d+', '12345')!r}")
print(f"  re.fullmatch(r'\\d+', '12345abc') = {re.fullmatch(r'\d+', '12345abc')!r}")
print(f"  re.fullmatch(r'\\d+', 'abc')      = {re.fullmatch(r'\d+', 'abc')!r}")
print("  -> fullmatch 要求整串都匹配，校验输入格式很方便")
print("  -> 等价于 re.match(r'\\d+$', s)，但 fullmatch 语义更清晰")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. match 从开头匹配，search 找任意位置第一个，findall 找全部")
print("  2. \\d 数字 \\w 字母数字_ \\s 空白；大写取反；[...] 字符集，[^...] 取反")
print("  3. * 0+ 次，+ 1+ 次，? 0 或 1 次，{n} {m,n} 精确重复")
print("  4. ^ 开头 $ 结尾，re.IGNORECASE 忽略大小写，fullmatch 整串匹配")
print("  5. 正则一律用 r-string，避免 \\d 被 Python 当转义符处理")