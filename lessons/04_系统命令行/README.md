# 模块 4：系统与命令行

> 自动化的尽头是"把工具串起来"：调外部命令、读命令行参数、做自己的 CLI 工具。Python 标准库的 `subprocess` 是调用外部程序的标准方式（替代老掉牙的 `os.system`），`sys` 暴露解释器状态和 `argv`，`argparse` 让你几行代码做出带 `--help` 的专业命令行工具。本模块从 subprocess 起步，经 sys、argparse，最后落到管道与重定向——把多个工具串成一条流水线。

## 核心库一览

| 库 | 来源 | 用途 | 推荐度 |
|---|:---:|---|:---:|
| `subprocess` | 标准库 | 调用外部命令、捕获输出、管道串联 | ★★★★★ |
| `sys` | 标准库 | 访问解释器状态：argv、platform、path、stdin/stdout | ★★★★ |
| `argparse` | 标准库 | 解析命令行参数，自动生成 --help | ★★★★★ |

## subprocess vs os.system：为什么用 subprocess

**os.system** 老办法，只能"执行 + 拿返回码"，拿不到命令输出：
```python
import os
ret = os.system("echo hello")   # 只打印到屏幕，拿不到 "hello" 这个字符串
```

**subprocess** 是官方推荐的新方式，能捕获输出、能传参数、能做管道、能控制超时：
```python
import subprocess
r = subprocess.run(["echo", "hello"], capture_output=True, text=True)
print(r.stdout)       # "hello\n"  —— 输出拿到了
print(r.returncode)   # 0
```

> **经验法则**：永远用 `subprocess`，别用 `os.system`。`os.system` 在新代码里基本没有用武之地，它只是"调 shell 跑一下"，既拿不到输出又有 shell 注入风险。`subprocess.run()` 是现代写法，传列表参数还自动避开注入问题。

## 核心 API 速查

```python
# --- subprocess（调用外部命令）---
import subprocess

# 基本调用
subprocess.run(["python", "--version"])          # 直接打印到屏幕

# 捕获输出
r = subprocess.run(["python", "--version"],
                   capture_output=True, text=True)
r.stdout        # 标准输出（字符串）
r.stderr        # 标准错误
r.returncode    # 退出码，0 表示成功

# 只要输出（出错会抛 CalledProcessError）
out = subprocess.check_output(["python", "--version"], text=True)

# 传输入 / 设超时
subprocess.run(["cat"], input="hello\n", text=True, timeout=5)
```

```python
# --- sys（解释器状态）---
import sys

sys.argv          # 命令行参数列表，argv[0] 是脚本名
sys.platform      # 'win32' / 'linux' / 'darwin'
sys.path          # 模块搜索路径
sys.version_info  # Python 版本 (sys.version_info.major)
sys.stdin         # 标准输入（可读）
sys.stdout        # 标准输出（可写）
sys.exit(0)       # 退出程序，0 正常 / 非 0 异常
```

```python
# --- argparse（做命令行工具）---
import argparse

parser = argparse.ArgumentParser(description="工具说明")
parser.add_argument("path", help="要处理的目录")             # 位置参数
parser.add_argument("-v", "--verbose", action="store_true")  # 开关
parser.add_argument("--ext", default=None, help="只统计某扩展名")
args = parser.parse_args()      # 自动读 sys.argv

args.path        # 拿到参数值
args.verbose     # True/False
# 自动支持 --help，无需自己写
```

## 本模块示例

| 脚本 | 演示 |
|---|---|
| [01_subprocess.py](01_subprocess.py) | run 调命令、捕获输出、check_output、异常处理、shell=True 的风险 |
| [02_sys模块.py](02_sys模块.py) | argv、exit、path、platform、stdin/stdout、版本信息 |
| [03_argparse做CLI.py](03_argparse做CLI.py) | 做一个"文件统计"CLI 工具，位置参数 + 可选参数 + --help |
| [04_管道与重定向.py](04_管道与重定向.py) | Popen 链式管道、重定向到文件、input 传输入 |

运行方式：
```bash
uv run python lessons/04_系统命令行/01_subprocess.py
uv run python lessons/04_系统命令行/02_sys模块.py
uv run python lessons/04_系统命令行/03_argparse做CLI.py
uv run python lessons/04_系统命令行/03_argparse做CLI.py --help
uv run python lessons/04_系统命令行/04_管道与重定向.py
```

## 底层原理（简单了解）

1. **subprocess 底层是 fork+exec / CreateProcess**：在 Linux/Mac 上，启动子进程靠 `fork()` 复制当前进程再 `exec()` 载入新程序；Windows 没有 fork，用 `CreateProcess` 一步到位。`subprocess` 把这两套差异藏起来了，你写一份代码三个平台都能跑。
2. **shell=True 是把命令交给 shell 解释**：`subprocess.run("ls | grep x", shell=True)` 等价于起一个 `/bin/sh` 或 `cmd.exe`，把整串丢给它解释。方便但危险：用户输入拼进命令就有注入风险（`rm -rf /` 都可能）。传列表参数（`shell=False`）则直接 exec 程序，不走 shell，天然防注入。
3. **argparse 解析的是 sys.argv**：`parse_args()` 默认读 `sys.argv[1:]`（去掉脚本名），按你定义的规则拆成参数对象。所以 `argparse` 和 `sys.argv` 是上下游关系——`sys.argv` 是原始字符串列表，`argparse` 是把它变成好用的对象。
4. **管道本质是共享一个文件描述符**：`a | b` 在 shell 里是让 a 的 stdout 和 b 的 stdin 指向同一根管道。`subprocess.Popen` 暴露了 `.stdout`，你可以把它喂给下一个命令的 `stdin=`，手动串起任意长的管道链。