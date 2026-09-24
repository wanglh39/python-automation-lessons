"""csv 标准库 —— 零依赖读写 CSV 表格

演示 Python 内置 csv 模块：writer / reader / DictReader / DictWriter。
csv 是纯文本格式，标准库够用，不用装任何第三方库。

运行: uv run python lessons/02_表格数据/01_csv标准库.py
"""
import csv
from pathlib import Path

# 定位 sample 目录
sample = Path(__file__).parent / "sample"
sample.mkdir(exist_ok=True)

# --- 准备测试数据 ---
students = [
    ("张三", 85, 92, 78),
    ("李四", 76, 88, 90),
    ("王五", 92, 95, 89),
    ("赵六", 68, 72, 75),
    ("钱七", 88, 91, 94),
]
score_csv = sample / "成绩单.csv"

print("=" * 55)
print("1. 用 csv.writer 写 CSV（最基本的写法）")
print("=" * 55)
# encoding='utf-8' 防中文乱码；newline='' 防 Windows 多出空行
with open(score_csv, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["姓名", "语文", "数学", "英语"])  # 表头
    writer.writerows(students)                          # 一次写多行
print(f"  已写入: {score_csv.name}")
print(f"  行数: {len(students) + 1} 行（含表头）")

print("\n" + "=" * 55)
print("2. 用 csv.reader 读 CSV（按位置访问，row[0]、row[1]）")
print("=" * 55)
with open(score_csv, encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(f"  {row}")  # row 是列表，如 ['张三', '85', '92', '78']
print("  -> 缺点：row[0] 是姓名还是别的？要数下标，不直观")

print("\n" + "=" * 55)
print("3. 用 csv.DictReader 读 CSV（按列名访问，推荐）")
print("=" * 55)
with open(score_csv, encoding="utf-8") as f:
    reader = csv.DictReader(f)  # 第一行自动当表头
    print(f"  字段名: {reader.fieldnames}")
    for row in reader:
        # row 是字典，按列名取值，代码自解释
        print(f"  {row['姓名']}: 语文{row['语文']} 数学{row['数学']} 英语{row['英语']}")
print("  -> 优点：row['姓名'] 一眼看出取的是哪列，不用数下标")

print("\n" + "=" * 55)
print("4. 用 csv.DictWriter 写汇总 CSV（加一列总分）")
print("=" * 55)
summary_csv = sample / "成绩汇总.csv"
# 先算每个人的总分
with open(score_csv, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# 写新 CSV，多一列"总分"
with open(summary_csv, "w", encoding="utf-8", newline="") as f:
    fieldnames = ["姓名", "语文", "数学", "英语", "总分"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()  # 写表头
    for row in rows:
        total = int(row["语文"]) + int(row["数学"]) + int(row["英语"])
        row["总分"] = total
        writer.writerow(row)
print(f"  已写入: {summary_csv.name}")

# 读回来验证
print("  内容预览:")
with open(summary_csv, encoding="utf-8") as f:
    for line in f:
        print(f"    {line.rstrip()}")

print("\n" + "=" * 55)
print("5. 关键参数说明（踩坑预警）")
print("=" * 55)
print("  encoding='utf-8'  -> 中文不乱码（Windows 默认 GBK 会乱）")
print("  newline=''        -> 写 CSV 时防止 Windows 多出空行")
print("  csv 模块是标准库  -> 不用 pip install，Python 自带")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. 写 CSV 用 csv.writer，读 CSV 用 csv.DictReader（按列名更直观）")
print("  2. open() 必须指定 encoding='utf-8'，写时还要加 newline=''")
print("  3. 简单表格读写用标准库 csv 就够，不必引入第三方库")