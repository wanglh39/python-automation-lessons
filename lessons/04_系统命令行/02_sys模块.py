"""sys 模块 —— Python 解释器的"系统状态"

演示 sys.argv 命令行参数、sys.exit 退出、sys.path 模块搜索路径、
sys.platform 操作系统、sys.stdin/stdout/stderr 标准流、sys.version 版本。

运行: uv run python lessons/04_系统命令行/02_sys模块.py
"""
import sys


print("=" * 55)
print("1. sys.argv：命令行参数列表")
print("=" * 55)
# argv[0] 永远是脚本名，argv[1:] 才是用户传的参数
print(f"  sys.argv = {sys.argv}")
print(f"  argv[0] (脚本名): {sys.argv[0]}")
print(f"  argv[1:] (用户参数): {sys.argv[1:]}")
print("  -> argv[0] 是脚本路径，argv[1] 开始才是真正的参数")
print("  -> 试试: uv run python lessons/04_系统命令行/02_sys模块.py foo bar")
print("     再看 argv 就会多出 ['foo', 'bar']")

print("\n" + "=" * 55)
print("2. sys.platform：当前操作系统")
print("=" * 55)
print(f"  sys.platform = {sys.platform!r}")
# 常见值：'win32' (Windows)、'linux' (Linux)、'darwin' (Mac)
if sys.platform == "win32":
    print("  -> 当前是 Windows")
elif sys.platform == "linux":
    print("  -> 当前是 Linux")
elif sys.platform == "darwin":
    print("  -> 当前是 macOS")
print("  -> 写跨平台脚本时用它判断系统，比如选 dir 还是 ls")

print("\n" + "=" * 55)
print("3. sys.version：Python 版本信息")
print("=" * 55)
print(f"  sys.version = {sys.version}")
print(f"  version_info.major = {sys.version_info.major}")
print(f"  version_info.minor = {sys.version_info.minor}")
print(f"  version_info.micro = {sys.version_info.micro}")
print(f"  完整版本号: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
# 版本比较：version_info 支持元组比较
if sys.version_info >= (3, 11):
    print("  -> 当前 Python >= 3.11，可以用 match-case 等新语法")
else:
    print("  -> 当前 Python < 3.11")
print("  -> version_info 可以直接比较：sys.version_info >= (3, 11)")

print("\n" + "=" * 55)
print("4. sys.path：模块搜索路径")
print("=" * 55)
# import 时 Python 就按 sys.path 的顺序找模块
print(f"  sys.path 共 {len(sys.path)} 个路径:")
for i, p in enumerate(sys.path):
    print(f"    [{i}] {p}")
print("  -> import xxx 时，Python 按这个列表顺序找 xxx.py")
print("  -> 第一个通常是脚本所在目录，所以同目录下的 .py 能直接 import")

print("\n" + "=" * 55)
print("5. sys.stdin / stdout / stderr：标准输入输出流")
print("=" * 55)
# stdout 就是 print 默认写的地方
print(f"  sys.stdout = {sys.stdout}")
print(f"  sys.stderr = {sys.stderr}")
print(f"  sys.stdin  = {sys.stdin}")
print("  -> print() 默认写到 sys.stdout，报错写到 sys.stderr")
print()
print("  [演示] 直接写 sys.stdout（和 print 等价）:")
sys.stdout.write("    这一行是用 sys.stdout.write 写的\n")
print("  -> print 内部就是调 sys.stdout.write，print 只是加了换行和 sep/end")

print("\n" + "=" * 55)
print("6. sys.stdin：从标准输入读（管道用法）")
print("=" * 55)
# isatty 判断 stdin 是不是终端；被管道喂时为 False
print(f"  sys.stdin.isatty() = {sys.stdin.isatty()}")
print("  -> isatty()=True 表示终端人手敲，False 表示被管道或重定向喂了数据")
print()
print("  读 stdin 的两种写法（在命令行里用管道试）:")
print("    # 写法1：逐行读")
print("    for line in sys.stdin:")
print("        print(f'收到: {line.strip()}')")
print("    # 写法2：一次读完")
print("    data = sys.stdin.read()")
print()
print("  管道示例:")
print("    echo 'hello' | uv run python lessons/04_系统命令行/02_sys模块.py")
print("  -> 被管道喂时 isatty()=False，上面两段代码就能读到 'hello'")
print("  -> 注意：交互运行时不要直接 read()，会卡住等输入")

print("\n" + "=" * 55)
print("7. sys.exit()：退出程序并给状态码")
print("=" * 55)
print("  sys.exit(0)   # 正常退出，状态码 0")
print("  sys.exit(1)   # 异常退出，状态码 1（shell 里用 $? 能看到）")
print("  sys.exit('出错信息')  # 打印信息到 stderr，状态码 1")
print("  -> 状态码约定：0 成功，非 0 失败；shell 脚本靠这个判断上一条命令成没成")
print("  -> 这里不真退出（不然后面的演示跑不了），只演示写法")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. sys.argv[0] 是脚本名，argv[1:] 是用户参数；argparse 内部就是读它")
print("  2. sys.platform 判断系统写跨平台代码，sys.version_info 比较版本")
print("  3. sys.stdin.isatty() 判断有没有管道输入，避免交互运行时卡住")
print("  4. sys.exit(0) 正常退出，非 0 异常；状态码是和 shell/CI 打交道的约定")