"""subprocess —— 调用外部命令的标准方式

演示 subprocess.run 调命令、捕获输出、check_output、异常处理、shell=True 的用法与风险。
subprocess 是 Python 调外部程序的官方推荐方式，替代老掉牙的 os.system。

运行: uv run python lessons/04_系统命令行/01_subprocess.py
"""
import subprocess
import sys

# 跨平台判断：Windows 和 Linux/Mac 都有 echo/python，但部分命令不同
IS_WIN = sys.platform == "win32"


print("=" * 55)
print("1. 最基本：subprocess.run 执行一条命令")
print("=" * 55)
# 传列表：第一个是命令，后面是参数。这是最推荐的写法（不走 shell，防注入）
print("  执行: python --version")
result = subprocess.run([sys.executable, "--version"])
print(f"  返回码: {result.returncode}")
print("  -> run 直接把命令输出打到屏幕，returncode=0 表示成功")
print("  -> 用列表传参 [命令, 参数1, 参数2]，比拼字符串安全")

print("\n" + "=" * 55)
print("2. 捕获输出：capture_output=True")
print("=" * 55)
# 默认 run 让输出直接显示，拿不到。加 capture_output=True 才能拿到 stdout/stderr
result = subprocess.run(
    [sys.executable, "--version"],
    capture_output=True,
    text=True,            # text=True 把输出当文本（自动 decode），不加就是字节
)
print(f"  returncode: {result.returncode}")
print(f"  stdout: {result.stdout.strip()!r}")
print(f"  stderr: {result.stderr.strip()!r}")
print("  -> capture_output=True 把输出截下来存进 .stdout / .stderr")
print("  -> text=True 让输出是字符串，否则是 bytes（要手动 .decode()）")

print("\n" + "=" * 55)
print("3. check_output：只想要输出，出错自动抛异常")
print("=" * 55)
# check_output = run + check=True + 只要 stdout 的简写
try:
    out = subprocess.check_output([sys.executable, "--version"], text=True)
    print(f"  输出: {out.strip()!r}")
except subprocess.CalledProcessError as e:
    print(f"  命令失败: {e}")
print("  -> check_output 适合'我只要输出，出错你直接报错'的场景")

print("\n" + "=" * 55)
print("4. 命令执行失败：捕获 CalledProcessError")
print("=" * 55)
# 故意跑一条会失败的命令：python --bad-flag
print("  故意执行: python --不存在的参数")
try:
    subprocess.run(
        [sys.executable, "--不存在的参数"],
        capture_output=True,
        text=True,
        check=True,          # check=True 时返回码非 0 就抛异常
    )
except subprocess.CalledProcessError as e:
    print(f"  捕获到异常: CalledProcessError")
    print(f"  返回码: {e.returncode}")
    print(f"  命令: {e.cmd}")
    print(f"  stderr: {e.stderr.strip()[:60]}...")
print("  -> check=True 让'命令失败'变成 Python 异常，方便 try/except 统一处理")

print("\n" + "=" * 55)
print("5. shell=True：能写管道和通配符，但有风险")
print("=" * 55)
# shell=True 把整串交给 shell 解释，可以用 | > * 等 shell 语法
if IS_WIN:
    cmd = "echo hello & echo world"
else:
    cmd = "echo hello; echo world"
print(f"  shell 命令: {cmd}")
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print(f"  输出: {result.stdout.strip()!r}")
print("  -> shell=True 能用 shell 语法（管道、通配、变量），写起来省事")
print()
print("  [风险演示] shell=True + 用户输入 = 命令注入漏洞:")
user_input = "hello; echo 被注入了"   # 假装这是用户传进来的
dangerous = f"echo {user_input}"
print(f"  拼出来的命令: {dangerous}")
result = subprocess.run(dangerous, shell=True, capture_output=True, text=True)
print(f"  实际执行结果: {result.stdout.strip()!r}")
print("  -> 攻击者用分号塞了第二条命令！这就是为什么 shell=True 不推荐")
print("  -> 安全写法：传列表，subprocess.run(['echo', user_input]) 不走 shell")

print("\n" + "=" * 55)
print("6. 实战：用 subprocess 跑 pip list 看装了哪些包")
print("=" * 55)
result = subprocess.run(
    [sys.executable, "-m", "pip", "list"],
    capture_output=True,
    text=True,
)
if result.returncode == 0:
    lines = result.stdout.strip().splitlines()
    print(f"  pip list 共 {len(lines)} 行，前 5 行:")
    for line in lines[:5]:
        print(f"    {line}")
else:
    print(f"  pip list 失败（返回码 {result.returncode}）")
    print(f"  stderr: {result.stderr.strip()[:80]}")
print("  -> 调 pip 用 [python, '-m', 'pip', 'list']，比直接 ['pip', 'list'] 更稳")
print("  -> sys.executable 是当前 Python 的完整路径，保证调的是同一个解释器")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. subprocess.run 是调外部命令的标准方式，传列表参数防注入，别用 os.system")
print("  2. capture_output=True + text=True 拿到字符串输出；check=True 让失败变异常")
print("  3. shell=True 能用管道通配符，但有命令注入风险，只在命令完全可控时用")
print("  4. 用 sys.executable 调 python，保证用的是同一个解释器环境")