"""argparse 做命令行工具 —— 几行代码做出带 --help 的专业 CLI

做一个"文件统计工具"：传目录路径，统计文件数量、总大小、按扩展名分类。
演示 argparse 的位置参数、可选参数、--help 自动生成。

运行: uv run python lessons/04_系统命令行/03_argparse做CLI.py
      uv run python lessons/04_系统命令行/03_argparse做CLI.py --help
      uv run python lessons/04_系统命令行/03_argparse做CLI.py lessons/01_文件批处理/sample
"""
import argparse
import sys
from pathlib import Path


def format_size(n):
    """字节数转人类可读：1.2 KB / 3.4 MB"""
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}" if unit != "B" else f"{int(n)} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def count_directory(target, verbose=False, ext_filter=None):
    """统计目录：文件数、总大小、按扩展名分类"""
    if not target.exists():
        print(f"错误: 目录不存在 -> {target}", file=sys.stderr)
        sys.exit(1)
    if not target.is_dir():
        print(f"错误: 不是目录 -> {target}", file=sys.stderr)
        sys.exit(1)

    if verbose:
        print(f"扫描目录: {target}")
        print(f"扩展名过滤: {ext_filter or '无'}")
        print()

    # 收集所有文件
    files = [f for f in target.rglob("*") if f.is_file()]

    # 按扩展名过滤
    if ext_filter:
        ext_norm = ext_filter if ext_filter.startswith(".") else f".{ext_filter}"
        files = [f for f in files if f.suffix.lower() == ext_norm.lower()]

    # 统计
    total_size = sum(f.stat().st_size for f in files)
    by_ext = {}
    for f in files:
        ext = f.suffix.lower() or "(无扩展名)"
        by_ext.setdefault(ext, []).append(f)

    # 输出结果
    print("=" * 55)
    print(f"目录统计: {target}")
    print("=" * 55)
    print(f"  文件总数: {len(files)}")
    print(f"  总大小:   {format_size(total_size)}")
    print()
    print("  按扩展名分类:")
    for ext in sorted(by_ext, key=lambda e: -len(by_ext[e])):
        group = by_ext[ext]
        size = sum(f.stat().st_size for f in group)
        print(f"    {ext:<14} {len(group):>3} 个  {format_size(size):>10}")

    if verbose:
        print()
        print("  文件清单:")
        for f in files:
            print(f"    {f.stat().st_size:>8} 字节  {f.name}")


def build_parser():
    """构造 argparse 解析器：定义有哪些参数"""
    parser = argparse.ArgumentParser(
        prog="03_argparse做CLI",
        description="文件统计工具 —— 统计目录里的文件数量、总大小、按扩展名分类",
        epilog=(
            "示例:\n"
            "  %(prog)s lessons/01_文件批处理/sample\n"
            "  %(prog)s lessons/01_文件批处理/sample --ext txt\n"
            "  %(prog)s lessons/01_文件批处理/sample -v"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # 位置参数：目录路径（nargs='?' 表示可省略，用 default）
    parser.add_argument(
        "directory",
        nargs="?",
        default="lessons/01_文件批处理/sample",
        help="要统计的目录路径（默认: lessons/01_文件批处理/sample）",
    )
    # 可选参数：开关（不带值，出现就是 True）
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细文件清单",
    )
    # 可选参数：带值
    parser.add_argument(
        "--ext",
        default=None,
        help="只统计指定扩展名，如 --ext txt 或 --ext .txt",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()      # 自动读 sys.argv，出错/--help 会自动退出

    # 没传任何参数时，先讲一下这个工具的设计（教学演示模式）
    if len(sys.argv) == 1:
        print("=" * 55)
        print("argparse 做的 CLI 工具 —— 文件统计")
        print("=" * 55)
        print("  这个脚本用标准库 argparse 做了一个命令行工具。")
        print("  它定义了三个参数：")
        print("    directory     位置参数（目录路径），不传就用默认 sample 目录")
        print("    -v/--verbose  开关参数，出现就是 True")
        print("    --ext         可选参数，带值，过滤扩展名")
        print("  argparse 自动生成 --help，不用自己写帮助文档。")
        print("  试试: uv run python lessons/04_系统命令行/03_argparse做CLI.py --help")
        print()

    count_directory(Path(args.directory), verbose=args.verbose, ext_filter=args.ext)

    # 教学演示模式下打印要点总结
    if len(sys.argv) == 1:
        print()
        print("=" * 55)
        print("完成!")
        print("=" * 55)
        print("要点:")
        print("  1. argparse 是做 CLI 工具的标准库，位置参数和 --可选参数都能定义")
        print("  2. action='store_true' 做开关，nargs='?' 让位置参数可省略")
        print("  3. --help 是 argparse 免费送的，description/epilog/help 字符串会拼进去")
        print("  4. parse_args() 读的是 sys.argv，所以 argparse 和 sys 是上下游关系")


if __name__ == "__main__":
    main()