"""按扩展名整理文件 —— 把散乱的文件归类到子文件夹

演示 pathlib 遍历 + mkdir + shutil.move 配合使用。
常见场景：下载文件夹一堆乱文件，按类型自动归档。

运行: uv run python lessons/01_文件批处理/03_按类型整理.py
"""
from pathlib import Path
import shutil

sample = Path(__file__).parent / "sample"
sample.mkdir(exist_ok=True)

# --- 准备散乱的测试文件 ---
test_files = ["报告.docx", "简历.pdf", "照片1.jpg", "照片2.png",
              "数据.csv", "表格.xlsx", "笔记.txt", "代码.py"]
for name in test_files:
    p = sample / name
    if not p.exists():
        p.write_text(f"{name} 的内容", encoding="utf-8")

# --- 整理前 ---
print(f"目标目录: {sample}")
print("\n整理前（散乱的文件）:")
for f in sorted(sample.iterdir()):
    if f.is_file():
        print(f"  {f.name}")

# --- 按扩展名归类 ---
print("\n开始按扩展名整理...\n")

moved = 0
for f in sample.iterdir():
    if not f.is_file():
        continue
    # 取扩展名，去掉点号；没扩展名的归到"无扩展名"
    ext = f.suffix.lstrip(".") or "无扩展名"

    # 创建归类子目录
    target_dir = sample / ext
    target_dir.mkdir(exist_ok=True)

    # 移动文件
    target = target_dir / f.name
    shutil.move(str(f), str(target))
    print(f"  {f.name:12s}  ->  {ext}/{f.name}")
    moved += 1

# --- 整理后 ---
print(f"\n整理后目录结构:")
for item in sorted(sample.iterdir()):
    if item.is_dir():
        count = sum(1 for _ in item.iterdir())
        print(f"  [{item.name}/]  ({count} 个文件)")
        for sub in sorted(item.iterdir()):
            print(f"      {sub.name}")

print(f"\n完成! 共整理 {moved} 个文件。")
print()
print("要点:")
print("  1. f.suffix 取扩展名，lstrip('.') 去掉点号")
print("  2. mkdir(exist_ok=True) 目录已存在不报错")
print("  3. shutil.move 跨磁盘移动，Path.rename 只能同磁盘")
print("  4. shutil.move 要传字符串，所以 str(f) 转一下")