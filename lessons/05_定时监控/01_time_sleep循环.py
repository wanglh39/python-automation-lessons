"""time.sleep 做最简单的定时循环

演示用 time.sleep 暂停、用 time.monotonic 避免漂移、用 datetime 格式化时间。
这是最原始也最简单的定时方式，适合临时脚本和几秒级的简单任务。

运行: uv run python lessons/05_定时监控/01_time_sleep循环.py
"""
import time
from datetime import datetime


def now_str():
    """返回当前时间字符串，方便日志输出"""
    return datetime.now().strftime("%H:%M:%S")


print("=" * 55)
print("1. time.sleep：最简单的暂停")
print("=" * 55)
print(f"  开始时间: {now_str()}")
print("  准备 sleep 2 秒...")
time.sleep(2)
print(f"  醒来时间: {now_str()}")
print("  -> time.sleep(n) 让程序暂停 n 秒，期间不占 CPU（操作系统挂起）")
print("  -> n 可以是浮点数：time.sleep(0.5) 暂停半秒")

print("\n" + "=" * 55)
print("2. 定时循环：每隔 2 秒打印一次，跑 3 轮退出")
print("=" * 55)
# 教学脚本不能无限跑，用计数器限制轮数
for i in range(1, 4):
    print(f"  第 {i} 轮，当前时间: {now_str()}")
    if i < 3:
        time.sleep(2)
print("  -> 最朴素的定时：循环里干活 + sleep，跑完就退出")
print("  -> 注意：这种写法每轮实际间隔 = 任务耗时 + sleep 时间，会有漂移")

print("\n" + "=" * 55)
print("3. 精确间隔：用 time.monotonic 消除漂移")
print("=" * 55)
# 漂移问题：如果任务本身花了 0.5 秒，再 sleep(2) 实际间隔就变成 2.5 秒
# 解决：记录"下次该跑的时刻"，sleep 到那个时刻，任务耗时被自动扣除
interval = 2.0
next_run = time.monotonic()         # 单调递增时钟，不受系统时间调整影响
print(f"  目标间隔: {interval} 秒，跑 3 轮")
for i in range(1, 4):
    # 模拟任务有耗时
    task_start = time.monotonic()
    print(f"  第 {i} 轮开始: {now_str()}")
    time.sleep(0.3)                 # 假装任务花了 0.3 秒
    elapsed = time.monotonic() - task_start
    print(f"    任务耗时: {elapsed:.2f} 秒")

    # 关键：sleep 到 next_run，而不是 sleep(interval)
    next_run += interval
    sleep_time = next_run - time.monotonic()
    if sleep_time > 0 and i < 3:
        print(f"    只 sleep {sleep_time:.2f} 秒（扣除任务耗时）")
        time.sleep(sleep_time)
print("  -> next_run += interval 累加目标时刻，sleep 到那个时刻")
print("  -> 任务花的时间被自动扣除，间隔始终是 2 秒，不会越漂越远")
print("  -> time.monotonic 不受系统时间被改的影响，比 time.time 更稳")

print("\n" + "=" * 55)
print("4. datetime 格式化：给定时任务加时间戳")
print("=" * 55)
now = datetime.now()
print(f"  完整时间: {now}")
print(f"  格式化:   {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  只到分:   {now.strftime('%Y年%m月%d日 %H:%M')}")
print(f"  时分秒:   {now.strftime('%H:%M:%S')}")
print(f"  日期:     {now.strftime('%Y-%m-%d')}")
print("  -> strftime 用 %Y年 %m月 %d日 %H时 %M分 %S秒 拼格式")
print("  -> 定时任务的日志一般带时间戳，方便排查'那次跑失败是几点'")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. time.sleep 最简单，但每轮间隔 = 任务耗时 + sleep，长时间会漂移")
print("  2. 用 time.monotonic 累加目标时刻可消除漂移，适合需要精确间隔的场景")
print("  3. datetime.now().strftime 给日志加时间戳，是定时任务的基本功")
print("  4. time.sleep 适合临时脚本；生产环境长期定时建议用 schedule 库或系统 cron")