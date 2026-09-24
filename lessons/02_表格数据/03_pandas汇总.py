"""pandas 汇总 —— 数据分析全家桶

演示 pandas：读 CSV/Excel、加计算列、筛选、排序、分组汇总、导出。
pandas 最强大但也最重，适合数据分析；简单读写用 csv/openpyxl 更轻量。

运行: uv run python lessons/02_表格数据/03_pandas汇总.py
"""
from pathlib import Path
import pandas as pd

# 定位 sample 目录
sample = Path(__file__).parent / "sample"
sample.mkdir(exist_ok=True)

# --- 依赖前两个脚本生成的数据，没有就现场生成 ---
score_csv = sample / "成绩单.csv"
xlsx_file = sample / "销售数据.xlsx"
if not score_csv.exists():
    import csv
    students = [
        ("张三", 85, 92, 78), ("李四", 76, 88, 90), ("王五", 92, 95, 89),
        ("赵六", 68, 72, 75), ("钱七", 88, 91, 94),
    ]
    with open(score_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["姓名", "语文", "数学", "英语"])
        w.writerows(students)

print("=" * 55)
print("1. 读取 CSV：pd.read_csv()")
print("=" * 55)
df = pd.read_csv(score_csv, encoding="utf-8")
print(f"  读取: {score_csv.name}")
print(f"  类型: {type(df).__name__}  <- 二维表，类似 Excel")
print(f"  形状: {df.shape}  (行数, 列数)")
print(df)

print("\n" + "=" * 55)
print("2. 认识 DataFrame：head / info / describe")
print("=" * 55)
print("--- df.head(3)  看前 3 行 ---")
print(df.head(3))
print("\n--- df.info()  看列名、类型、非空数 ---")
df.info()
print("\n--- df.describe()  数值列统计摘要 ---")
print(df.describe())

print("\n" + "=" * 55)
print("3. 加计算列：df['新列'] = ...")
print("=" * 55)
df["总分"] = df["语文"] + df["数学"] + df["英语"]   # 向量化，一行搞定
df["平均分"] = df["总分"] / 3
print(df[["姓名", "总分", "平均分"]])
print("  -> 向量化运算，不用 for 循环，整列同时算")

print("\n" + "=" * 55)
print("4. 筛选：df[df['列'] > 值]")
print("=" * 55)
high = df[df["总分"] > 240]
print("  总分 > 240 的学生:")
print(high[["姓名", "总分"]])
print(f"  -> 筛出 {len(high)} 条")

print("\n" + "=" * 55)
print("5. 排序：df.sort_values()")
print("=" * 55)
sorted_df = df.sort_values("总分", ascending=False)  # 降序
print("  按总分降序:")
print(sorted_df[["姓名", "总分"]])

print("\n" + "=" * 55)
print("6. 分组汇总：df.groupby()")
print("=" * 55)
# 给数据加个"班级"列好演示分组
df["班级"] = ["A", "B", "A", "B", "A"]
print("  加'班级'列后:")
print(df[["姓名", "班级", "总分"]])
print("\n  按班级分组求总分均值:")
group_mean = df.groupby("班级")["总分"].mean()
print(group_mean)
print("\n  按班级分组多种统计 (agg):")
group_stats = df.groupby("班级")["总分"].agg(["mean", "max", "min", "count"])
print(group_stats)

print("\n" + "=" * 55)
print("7. 导出：df.to_csv()")
print("=" * 55)
out_csv = sample / "pandas汇总结果.csv"
sorted_df.to_csv(out_csv, index=False, encoding="utf-8")
print(f"  已导出: {out_csv.name}")
print(f"  index=False  -> 不写行索引那列")
print(f"  encoding='utf-8'  -> 中文不乱码")

print("\n" + "=" * 55)
print("8. 读 Excel：pd.read_excel()")
print("=" * 55)
if xlsx_file.exists():
    df_xlsx = pd.read_excel(xlsx_file)
    print(f"  读取: {xlsx_file.name}")
    print(f"  形状: {df_xlsx.shape}")
    print(df_xlsx.head(3))
    print("  -> pandas 读 Excel 底层调 openpyxl，自动转成 DataFrame")
else:
    print("  (销售数据.xlsx 不存在，跳过；先运行 02_openpyxl读写.py 生成)")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. pandas 适合数据分析：筛选/排序/分组/统计 一行搞定")
print("  2. df['新列'] = ... 是向量化运算，比 for 循环快几十倍")
print("  3. 简单读写用 csv/openpyxl 更轻量，数据分析才上 pandas")