"""pathlib 基础 —— 现代化的路径操作（推荐替代 os.path）

运行: uv run python lessons/01_文件批处理/01_pathlib基础.py
"""
from pathlib import Path

print("=" * 55)
print("1. 创建 Path 对象")
print("=" * 55)
# 用 / 运算符拼接路径，自动适配 Windows(\) 和 macOS(/)
p = Path("sample") / "报告.docx"
print(f"  Path('sample') / '报告.docx' = {p}")
print(f"  类型: {type(p).__name__}  <- 不是字符串，是 Path 对象")

print("\n" + "=" * 55)
print("2. 拆解路径的各个部分（纯字符串操作，不访问磁盘）")
print("=" * 55)
print(f"  p.name   = {p.name!r:20s} # 完整文件名")
print(f"  p.stem   = {p.stem!r:20s} # 去掉扩展名")
print(f"  p.suffix = {p.suffix!r:20s} # 扩展名")
print(f"  p.parent = {p.parent!r:20s} # 父目录")
print(f"  p.parts  = {p.parts}")

print("\n" + "=" * 55)
print("3. 常用特殊路径")
print("=" * 55)
print(f"  当前工作目录 Path.cwd() = {Path.cwd()}")
print(f"  用户家目录   Path.home() = {Path.home()}")

print("\n" + "=" * 55)
print("4. 判断：存在？是文件还是目录？（这些才真正访问磁盘）")
print("=" * 55)
cwd = Path.cwd()
print(f"  cwd.exists() = {cwd.exists()}    # 路径是否存在")
print(f"  cwd.is_dir()  = {cwd.is_dir()}    # 是否目录")
print(f"  cwd.is_file() = {cwd.is_file()}   # 是否文件")

print("\n" + "=" * 55)
print("5. 遍历目录：iterdir / glob / rglob")
print("=" * 55)

# 准备 sample 测试文件
sample = Path(__file__).parent / "sample"
sample.mkdir(exist_ok=True)
if not any(sample.iterdir()):
    for name in ["报告.docx", "照片.jpg", "数据.csv", "笔记.txt"]:
        (sample / name).write_text(f"这是 {name} 的内容", encoding="utf-8")
    (sample / "子文件夹").mkdir(exist_ok=True)
    (sample / "子文件夹" / "备份.txt").write_text("备份内容", encoding="utf-8")

print("  iterdir() —— 列出直接子项（不递归）:")
for item in sorted(sample.iterdir()):
    tag = "[目录]" if item.is_dir() else "[文件]"
    print(f"    {tag} {item.name}")

print("\n  glob('*.txt') —— 通配符匹配（仅当前层）:")
for item in sorted(sample.glob("*.txt")):
    print(f"    [文件] {item.name}")

print("\n  rglob('*.txt') —— 递归搜索所有子目录:")
for item in sorted(sample.rglob("*.txt")):
    print(f"    [文件] {item.relative_to(sample)}")

print("\n" + "=" * 55)
print("6. 读写小文件：Path 对象自带读写方法，不用 open()")
print("=" * 55)
f = sample / "笔记.txt"
content = f.read_text(encoding="utf-8")
print(f"  原内容: {content}")
f.write_text("被脚本修改过的内容", encoding="utf-8")
print(f"  write_text() 后: {f.read_text(encoding='utf-8')}")
# 改回去，方便其他脚本重复运行
f.write_text("这是 笔记.txt 的内容", encoding="utf-8")

print("\n" + "=" * 55)
print("7. 路径变换：换扩展名、换文件名、转绝对路径")
print("=" * 55)
print(f"  p.with_suffix('.pdf')  = {p.with_suffix('.pdf')}")
print(f"  p.with_name('新名.docx') = {p.with_name('新名.docx')}")
print(f"  p.resolve() (绝对路径)   = {p.resolve()}")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点: Path 对象用 / 拼接，用 .xxx 取属性，用 glob/rglob 遍历。")
print("      read_text/write_text 直接读写，不用 open()。")