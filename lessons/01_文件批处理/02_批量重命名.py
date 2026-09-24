"""批量重命名 —— 给目录下所有文件加日期前缀

演示 pathlib + datetime 配合做批量文件操作。
这是自动化最典型的场景：一个循环 + rename 搞定几百个文件。

运行: uv run python lessons/01_文件批处理/02_批量重命名.py
"""
from pathlib import Path
from datetime import datetime

# 定位 sample 目录（用 __file__ 保证从任何位置运行都能找到）
sample = Path(__file__).parent / "sample"
sample.mkdir(exist_ok=True)

# --- 准备测试文件（如果没有就生成）---
if not any(sample.glob("原始_*.txt")):
    for name in ["原始_笔记.txt", "原始_草稿.txt", "原始_清单.txt"]:
        (sample / name).write_text(f"{name} 的内容", encoding="utf-8")

# --- 批量重命名 ---
prefix = datetime.now().strftime("%Y%m%d_")  # 如 20260924_

print(f"目标目录: {sample}")
print(f"加前缀:   '{prefix}'")
print()

# 1. 先收集要改的文件（先收集再改，避免边遍历边改名出问题）
files = sorted(sample.glob("原始_*.txt"))

print("重命名前:")
for f in files:
    print(f"  {f.name}")

# 2. 逐个重命名
print("\n执行重命名...")
for f in files:
    new_name = prefix + f.name               # 拼新文件名
    new_path = f.with_name(new_name)         # 构造新 Path
    f.rename(new_path)                       # 真正改名（磁盘操作）
    print(f"  {f.name}  ->  {new_name}")

# 3. 看结果
print("\n重命名后:")
for f in sorted(sample.glob("*.txt")):
    print(f"  {f.name}")

print(f"\n完成! 共重命名 {len(files)} 个文件。")
print()
print("要点:")
print("  1. 先 glob 收集文件列表，再循环 rename —— 不要边遍历边改")
print("  2. f.with_name(新名) 生成新路径，f.rename(新路径) 执行改名")
print("  3. datetime.strftime 格式化日期: %Y%m%d = 20260924")