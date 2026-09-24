"""分组与替换 —— 捕获组、命名分组、re.sub、re.split、非贪婪

演示捕获组 () 和 group(1)/group(2)、命名分组 (?P<name>...)、
re.sub 替换并在替换串里用 \\1 \\2 引用分组、re.split 按模式分割、
非贪婪匹配 *? +?，实战把日期 2026-09-24 转成 24/09/2026。
只用 re 标准库，一定能跑。

运行: uv run python lessons/09_正则与文本提取/02_分组与替换.py
"""
import re


print("=" * 55)
print("1. 捕获组 () 和 group(1) / group(2)")
print("=" * 55)
# 用括号把模式的一部分"捕获"起来，匹配后用 group(1) group(2) 取
m = re.search(r"(\d+)-(\d+)-(\d+)", "今天日期 2026-09-24 周四")
print(f"  文本: '今天日期 2026-09-24 周四'")
print(f"  模式 r'(\\d+)-(\\d+)-(\\d+)'")
print(f"  m.group()   = {m.group()!r}   整个匹配")
print(f"  m.group(0)  = {m.group(0)!r}   同上")
print(f"  m.group(1)  = {m.group(1)!r}   第 1 个组：年")
print(f"  m.group(2)  = {m.group(2)!r}   第 2 个组：月")
print(f"  m.group(3)  = {m.group(3)!r}   第 3 个组：日")
print(f"  m.groups()  = {m.groups()}  所有组组成的元组")
print("  -> 括号从左到右编号；group(0) 是整个匹配，group(1) 起是各捕获组")

print("\n" + "=" * 55)
print("2. findall 遇到捕获组：返回元组列表")
print("=" * 55)
text = "日期 2026-09-24 和 2026-12-31"
result = re.findall(r"(\d{4})-(\d{2})-(\d{2})", text)
print(f"  文本: {text!r}")
print(f"  findall(r'(\\d{{4}})-(\\d{{2}})-(\\d{{2}})', text) = {result}")
print("  -> 有捕获组时，findall 返回元组列表，每项是各组组成的元组")
print("  -> 想要整个匹配字符串，用非捕获组 (?:...) 或 finditer + .group()")

print("\n" + "=" * 55)
print("3. 命名分组 (?P<name>...)：用名字取，比编号清晰")
print("=" * 55)
pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
m2 = re.search(pattern, "截止日期 2026-09-24")
print(f"  模式 r'(?P<year>\\d{{4}})-(?P<month>\\d{{2}})-(?P<day>\\d{{2}})'")
print(f"  m2.group('year')  = {m2.group('year')!r}")
print(f"  m2.group('month') = {m2.group('month')!r}")
print(f"  m2.group('day')   = {m2.group('day')!r}")
print(f"  m2.groupdict()    = {m2.groupdict()}")
print("  -> (?P<名字>模式) 给组起名，group('名字') 取；groupdict() 一次全取")
print("  -> 命名分组在复杂模式里可读性远好于 group(1) group(2)...")

print("\n" + "=" * 55)
print("4. re.sub 基本替换")
print("=" * 55)
# re.sub(模式, 替换串, 原文) 把所有匹配替换掉
original = "电话 13800138000 和 13912345678"
masked = re.sub(r"\d{11}", "[手机号]", original)
print(f"  原文: {original!r}")
print(f"  re.sub(r'\\d{{11}}', '[手机号]', 原文)")
print(f"  结果: {masked!r}")
print("  -> re.sub 默认替换所有匹配；脱敏、清洗文本常用")

print("\n" + "=" * 55)
print("5. re.sub 替换中用分组引用 \\1 \\2")
print("=" * 55)
# 替换串里 \1 \2 引用前面捕获的组，可以重组字符串
date_text = "日期 2026-09-24，截止 2026-12-31"
# 把 年-月-日 调成 日/月/年
reordered = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", date_text)
print(f"  原文: {date_text!r}")
print(f"  模式 r'(\\d{{4}})-(\\d{{2}})-(\\d{{2}})'  替换 r'\\3/\\2/\\1'")
print(f"  结果: {reordered!r}")
print("  -> \\1 \\2 \\3 在替换串里引用对应捕获组，可任意重排顺序")
print("  -> 注意替换串也用 r-string，否则 \\1 会被 Python 当成 \\x01")

print("\n" + "=" * 55)
print("6. re.sub 用命名分组引用 \\g<name>")
print("=" * 55)
# 命名分组在替换里用 \g<名字> 引用，比 \1 更清晰
reordered2 = re.sub(
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})",
    r"\g<day>/\g<month>/\g<year>",
    date_text,
)
print(f"  原文: {date_text!r}")
print(f"  替换 r'\\g<day>/\\g<month>/\\g<year>'")
print(f"  结果: {reordered2!r}")
print("  -> \\g<名字> 引用命名分组，比 \\1 \\2 \\3 更不容易写错位置")

print("\n" + "=" * 55)
print("7. re.sub 用函数做替换：动态计算替换内容")
print("=" * 55)
# 替换串可以是一个函数，入参是 Match 对象，返回替换结果
def mask_phone(m):
    """把手机号中间 4 位替换成 ****"""
    phone = m.group()
    return phone[:3] + "****" + phone[7:]

phones_text = "联系 13800138000 或 13912345678"
masked_phones = re.sub(r"\d{11}", mask_phone, phones_text)
print(f"  原文: {phones_text!r}")
print(f"  re.sub(r'\\d{{11}}', mask_phone, 原文)  把中间 4 位打码")
print(f"  结果: {masked_phones!r}")
print("  -> 传函数时，每个匹配调用一次，返回值作为替换内容")
print("  -> 比纯字符串替换灵活得多：能脱敏、能查表、能格式化")

print("\n" + "=" * 55)
print("8. re.sub 限定替换次数 count")
print("=" * 55)
multi = "a-b-c-d-e-f"
only2 = re.sub(r"-", "+", multi, count=2)
print(f"  原文: {multi!r}")
print(f"  re.sub(r'-', '+', 原文, count=2) = {only2!r}")
print("  -> count=N 只替换前 N 个，剩下的保留；默认 count=0 表示全替换")

print("\n" + "=" * 55)
print("9. re.split：按模式分割，比 str.split 更灵活")
print("=" * 55)
# str.split 只能按固定字符串切；re.split 能按"一类分隔符"切
line = "姓名  张三   年龄 25  城市 北京"
# 按一个或多个空白切
parts = re.split(r"\s+", line.strip())
print(f"  原文: {line!r}")
print(f"  re.split(r'\\s+', strip 后) = {parts}")
print("  -> \\s+ 表示一个或多个空白，能一次切掉连续多空格，str.split() 也能")
# 按多种分隔符切
mixed_sep = "苹果,香蕉;橙子|西瓜-葡萄"
fruits = re.split(r"[,;|-]", mixed_sep)
print(f"  原文: {mixed_sep!r}")
print(f"  re.split(r'[,;|-]', 原文) = {fruits}")
print("  -> 字符集 [,;|-] 让任一分隔符都能切，str.split 做不到一次切多种")
# 分割带捕获组：分隔符也会出现在结果里
with_group = re.split(r"(\s+)", line.strip())
print(f"  带捕获组 re.split(r'(\\s+)', ...) = {with_group}")
print("  -> 模式里有捕获组时，分隔符也保留在结果里，便于还原")

print("\n" + "=" * 55)
print("10. 非贪婪匹配 *? +?：尽量少匹配")
print("=" * 55)
# 贪婪 * 默认尽量多匹配，非贪婪 *? 尽量少匹配
html_snippet = '<a href="url1">链接1</a> <a href="url2">链接2</a>'
greedy = re.findall(r'<a.*>.*</a>', html_snippet)
lazy = re.findall(r'<a.*?>.*?</a>', html_snippet)
print(f"  文本: {html_snippet!r}")
print(f"  贪婪 r'<a.*>.*</a>'   = {greedy}")
print(f"  非贪婪 r'<a.*?>.*?</a>' = {lazy}")
print("  -> 贪婪 .* 一路吃到最后一个 </a>，两个标签被当成一个长匹配")
print("  -> 非贪婪 .*? 找到第一个 </a> 就停，正确分出两个标签")
print("  -> 提取有明确结束标志的内容（引号串、标签）一律用非贪婪")

print("\n" + "=" * 55)
print("11. 非贪婪实战：提取引号里的内容")
print("=" * 55)
config = 'name="张三" age="25" city="北京"'
# 贪婪会从第一个 " 吃到最后一个 "
wrong = re.findall(r'"(.*)"', config)
right = re.findall(r'"(.*?)"', config)
print(f"  文本: {config!r}")
print(f"  贪婪 r'\"(.*)\"'    = {wrong}  (一把抓了全部)")
print(f"  非贪婪 r'\"(.*?)\"' = {right}  (正确分出每个引号串)")
print("  -> 提取引号、括号、标签内容这类场景，必须用非贪婪 *? 或 +?")

print("\n" + "=" * 55)
print("12. 实战：日期 2026-09-24 转成 24/09/2026")
print("=" * 55)
samples = ["2026-09-24", "2025-01-01", "2024-12-31"]
print("  用 re.sub + 分组引用一次完成格式转换：")
for s in samples:
    converted = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", s)
    print(f"    {s}  ->  {converted}")
print("  -> 模式 r'(\\d{{4}})-(\\d{{2}})-(\\d{{2}})' 捕获年月日三个组")
print("  -> 替换 r'\\3/\\2/\\1' 把第 3 组(日)放前面，第 2 组(月)中间，第 1 组(年)放后")
print("  -> 这就是分组+替换的典型用法：识别结构、重组输出")

print("\n" + "=" * 55)
print("13. 非捕获组 (?:...)：分组但不编号")
print("=" * 55)
# 有时括号只是用来分组，不想占用组编号，用 (?:...)
m3 = re.search(r"(?:\d{4})-(\d{2})-(\d{2})", "2026-09-24")
print(f"  模式 r'(?:\\d{{4}})-(\\d{{2}})-(\\d{{2}})'")
print(f"  m3.group(1) = {m3.group(1)!r}  (?:...) 不占编号，所以 1 是月")
print(f"  m3.group(2) = {m3.group(2)!r}")
print(f"  m3.groups() = {m3.groups()}")
print("  -> (?:...) 只分组不捕获，不占用 group 编号")
print('  -> 想用括号表达"或"或重复，又不想污染组编号时用非捕获组')

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. () 捕获组，group(1)/group(2) 取；findall 有组时返回元组列表")
print("  2. (?P<name>...) 命名分组，group('name') 取，可读性更好")
print("  3. re.sub 替换；替换串里 \\1 \\2 或 \\g<name> 引用分组重组字符串")
print("  4. re.sub 替换串可以是函数，入参 Match，返回替换内容，非常灵活")
print("  5. re.split 按模式分割，能一次切多种分隔符；有捕获组时分隔符也保留")
print("  6. *? +? 非贪婪尽量少匹配，提取引号/标签内容必须用非贪婪")
print("  7. (?:...) 非捕获组，只分组不占编号；替换串一律用 r-string")