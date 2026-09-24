"""管道与重定向 —— 把多个命令串成流水线

演示 subprocess.Popen 做链式管道、重定向输出到文件、用 input 参数给命令传输入。
管道是自动化的核心能力：把一个工具的输出喂给下一个工具。

运行: uv run python lessons/04_系统命令行/04_管道与重定向.py
"""
import subprocess
import sys
from pathlib import Path

# 跨平台：Windows 用 findstr，Linux/Mac 用 grep
IS_WIN = sys.platform == "win32"


print("=" * 55)
print("1. 管道：把一个命令的输出传给另一个命令")
print("=" * 55)
# 演示：python 生成几行文本，传给 findstr/grep 找含 'world' 的行
producer = [sys.executable, "-c", "print('hello'); print('world'); print('hello world')"]
if IS_WIN:
    consumer = ["findstr", "world"]
else:
    consumer = ["grep", "world"]

print(f"  生产者: {producer}")
print(f"  消费者: {consumer}")
print()
# 第一步：启动生产者，把它的 stdout 用管道接出来（不打到屏幕）
p1 = subprocess.Popen(producer, stdout=subprocess.PIPE, text=True)
# 第二步：启动消费者，把它的 stdin 接到生产者的 stdout
p2 = subprocess.Popen(consumer, stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
# 关掉 p1.stdout 在父进程的引用（重要！否则 p1 等不到 EOF 不会结束）
p1.stdout.close()
# 拿消费者的输出
output = p2.communicate()[0]
p1.wait()
print(f"  管道结果（含 'world' 的行）:")
for line in output.strip().splitlines():
    print(f"    {line.strip()}")
print("  -> p1 的 stdout 通过 PIPE 接到 p2 的 stdin，这就是管道")
print("  -> 记得 p1.stdout.close()，否则 p1 不知道输出读完了会卡住")

print("\n" + "=" * 55)
print("2. 重定向输出到文件：stdout=open(...)")
print("=" * 55)
# 把命令输出直接写到文件，不经过屏幕
out_file = Path("lessons/04_系统命令行/_管道输出.txt")
print(f"  执行: python --version，输出写到 {out_file.name}")
with open(out_file, "w", encoding="utf-8") as f:
    result = subprocess.run(
        [sys.executable, "--version"],
        stdout=f,               # stdout 指向文件对象，输出就进文件
        text=True,
    )
print(f"  返回码: {result.returncode}")
print(f"  文件内容: {out_file.read_text(encoding='utf-8').strip()!r}")
print("  -> stdout=文件对象，命令输出直接进文件，等价于 shell 的 command > file")

print("\n" + "=" * 55)
print("3. input 参数：给命令传输入（不用 Popen 也能喂 stdin）")
print("=" * 55)
# 演示：给一个读 stdin 的 python 脚本传输入，让它转大写
script = "import sys; print(sys.stdin.read().upper())"
print(f"  脚本: {script}")
print(f"  输入: 'hello pipe'")
result = subprocess.run(
    [sys.executable, "-c", script],
    input="hello pipe",         # input 参数喂给命令的 stdin
    capture_output=True,
    text=True,
)
print(f"  输出: {result.stdout.strip()!r}")
print("  -> input='...' 等价于 echo '...' | command，但不用真起管道")

print("\n" + "=" * 55)
print("4. 多级管道：两个 python 命令串起来")
print("=" * 55)
# 演示：生成几行文本 -> 去重排序输出
gen_script = "print('banana'); print('apple'); print('cherry'); print('apple')"
print(f"  原始数据: banana, apple, cherry, apple")
print(f"  管道: 生成 -> 去重排序")
# 第一个命令：生成文本
p1 = subprocess.Popen(
    [sys.executable, "-c", gen_script],
    stdout=subprocess.PIPE,
    text=True,
)
# 第二个命令：读 stdin，去重排序输出（用 chr(10) 当换行，避免转义麻烦）
sort_script = "import sys; lines=sorted(set(sys.stdin.read().splitlines())); print(chr(10).join(lines))"
p2 = subprocess.Popen(
    [sys.executable, "-c", sort_script],
    stdin=p1.stdout,
    stdout=subprocess.PIPE,
    text=True,
)
p1.stdout.close()
output = p2.communicate()[0]
p1.wait()
print(f"  去重排序后:")
for line in output.strip().splitlines():
    print(f"    {line}")
print("  -> 任意多个命令都能这样串：每个的 stdout 喂给下一个的 stdin")

print("\n" + "=" * 55)
print("5. 捕获 stderr：错误流和输出流分开")
print("=" * 55)
# 让 python 同时输出 stdout 和 stderr，分开捕获
result = subprocess.run(
    [sys.executable, "-c", "import sys; print('正常输出'); print('出错信息', file=sys.stderr)"],
    capture_output=True,
    text=True,
)
print(f"  stdout: {result.stdout.strip()!r}")
print(f"  stderr: {result.stderr.strip()!r}")
print("  -> capture_output=True 把 stdout 和 stderr 分开存，不会混在一起")
print("  -> 想合并可以 stderr=subprocess.STDOUT，让错误也进 stdout")

# 清理临时文件
out_file.unlink(missing_ok=True)

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. 管道用 Popen + PIPE：p1.stdout 喂给 p2 的 stdin，记得 close p1.stdout")
print("  2. 重定向到文件：stdout=open('x.txt','w')，等价于 shell 的 > file")
print("  3. input 参数是喂 stdin 的简写，不用 Popen 也能给命令传输入")
print("  4. capture_output 把 stdout/stderr 分开；管道是自动化的核心，把工具串成流水线")