# 模块 5：定时任务与监控

> 自动化脚本写完一次跑就完事？真正的自动化要"自己跑"——定时执行、长期守护、盯着文件变化。本模块从最朴素的 `time.sleep` 循环起步，到 API 友好的 `schedule` 库，再到操作系统级的 `watchdog` 文件监控，最后讲清"让脚本长期在后台跑"的几种思路。

## 核心库一览

| 库 | 来源 | 用途 | 推荐度 |
|---|:---:|---|:---:|
| `time` | 标准库 | sleep 暂停、time 计时、最基础的定时循环 | ★★★★ |
| `datetime` | 标准库 | 获取/格式化当前时间，给日志和定时任务加时间戳 | ★★★★ |
| `schedule` | 第三方 | 友好的定时任务 API：every(10).seconds.do(job) | ★★★★ |
| `watchdog` | 第三方 | 监控文件/目录变化，操作系统事件驱动，不用轮询 | ★★★★★ |
| `threading` | 标准库 | 后台线程，让守护任务不阻塞主程序 | ★★★ |

## 三种定时方案对比

| 方案 | 怎么用 | 优点 | 缺点 | 适用场景 |
|---|---|---|---|---|
| **time.sleep 循环** | `while True: do(); time.sleep(60)` | 零依赖、最简单、好理解 | 长时间有漂移、重启会丢、单线程阻塞 | 临时脚本、间隔几秒的简单任务 |
| **schedule 库** | `schedule.every(10).minutes.do(job)` | API 友好、支持各种间隔、可注册多任务 | 纯 Python 单线程、仍要自己跑循环、不精确 | 中等复杂度、多任务、几分钟级间隔 |
| **系统 cron / 任务计划** | `crontab: */10 * * * * python x.py` | 系统级稳定、开机自启、精确到分钟 | 需要系统配置、跨平台不一致、不便调试 | 生产环境、每天/每小时级定时、长期运行 |

> **经验法则**：临时跑着玩用 `time.sleep`；要在脚本里管几个定时任务用 `schedule`；要"每天凌晨备份"这种生产级定时，直接用系统 cron（Linux）或任务计划程序（Windows），别让 Python 一直挂着。

## 核心 API 速查

```python
# --- time（最基础定时）---
import time

time.sleep(5)            # 暂停 5 秒（浮点数也行：0.5 秒）
time.time()              # 当前时间戳（秒，浮点）
time.monotonic()         # 单调递增时钟，不受系统时间调整影响，适合算间隔

# 精确间隔循环（避免漂移）
next_run = time.monotonic()
while True:
    do_job()
    next_run += 60                       # 下次该跑的时刻
    time.sleep(max(0, next_run - time.monotonic()))
```

```python
# --- datetime（格式化时间）---
from datetime import datetime

now = datetime.now()                     # 当前本地时间
datetime.now().strftime("%Y-%m-%d %H:%M:%S")   # '2025-09-24 14:30:05'
datetime.now().strftime("%H:%M:%S")             # '14:30:05'
```

```python
# --- schedule（友好的定时任务）---
import schedule, time

def job():
    print("干活")

schedule.every(10).seconds.do(job)              # 每 10 秒
schedule.every(30).minutes.do(job)              # 每 30 分钟
schedule.every().hour.do(job)                   # 每小时
schedule.every().day.at("10:30").do(job)        # 每天 10:30
schedule.every().monday.at("09:00").do(job)     # 每周一 9 点

while True:
    schedule.run_pending()              # 跑到点的任务，没到就立刻返回
    time.sleep(1)
```

```python
# --- watchdog（监控文件变化）---
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event): print(f"新建: {event.src_path}")
    def on_modified(self, event): print(f"修改: {event.src_path}")
    def on_deleted(self, event): print(f"删除: {event.src_path}")

observer = Observer()
observer.schedule(MyHandler(), path=".", recursive=False)
observer.start()                        # 启动后台线程监听
# ... 程序主体 ...
observer.stop()                         # 停止
observer.join()                         # 等监听线程退出
```

## 本模块示例

| 脚本 | 演示 |
|---|---|
| [01_time_sleep循环.py](01_time_sleep循环.py) | time.sleep 做定时循环、用 time.monotonic 避免漂移、datetime 格式化 |
| [02_schedule库.py](02_schedule库.py) | schedule 注册多任务、各种间隔、run_pending 循环、限时退出 |
| [03_监控文件变化.py](03_监控文件变化.py) | watchdog 监控目录、事件处理器、自动触发增删改、限时退出 |
| [04_守护进程思路.py](04_守护进程思路.py) | while True 守护、threading 后台线程、nohup/systemd/cron/PM2 思路 |

运行方式：
```bash
uv run python lessons/05_定时监控/01_time_sleep循环.py
uv run python lessons/05_定时监控/02_schedule库.py
uv run python lessons/05_定时监控/03_监控文件变化.py
uv run python lessons/05_定时监控/04_守护进程思路.py
```

## 底层原理（简单了解）

1. **time.sleep 底层是操作系统调用**：Linux/Mac 上是 `nanosleep`，Windows 上是 `SleepEx`，都是让出 CPU 给操作系统的"挂起"系统调用，不是忙等待（不会空转烧 CPU）。所以 `time.sleep(60)` 这 60 秒里 Python 进程基本不占 CPU。
2. **schedule 是纯 Python 循环**：`schedule` 库没有用任何系统定时器，它只是把"下次该跑的时刻"记在内存里，每次 `run_pending()` 检查一遍"到点了没"。所以它依赖你自己的 `while + sleep` 循环来驱动，单线程下任务串行执行，一个任务慢了后面全堵着。
3. **watchdog 底层是操作系统文件事件**：Windows 用 `ReadDirectoryChangesW`，Linux 用 `inotify`，Mac 用 `FSEvents`——都是操作系统提供的"文件变化主动通知"机制。所以 watchdog 不用轮询（不用每秒扫一遍目录），文件一变操作系统就推过来，既快又省 CPU。
4. **守护进程的本质是"不让程序退出"**：`while True` 让主线程永远循环、`threading` 让任务在后台跑、`nohup` 让进程脱离终端、`systemd` 让操作系统帮你管（崩了自动拉起）。从 `while True` 到 `systemd`，是从"自己管"到"交给系统管"的升级——越往后越稳，但配置也越重。