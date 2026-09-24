"""schedule 库 —— API 友好的定时任务

演示 schedule 第三方库：注册多个任务、各种间隔、run_pending 循环、限时退出。
schedule 把 time.sleep 循环包装成友好 API，适合管理多个定时任务。

运行: uv run python lessons/05_定时监控/02_schedule库.py
"""
import time
from datetime import datetime

import schedule


def now_str():
    return datetime.now().strftime("%H:%M:%S")


# 用计数器记录任务执行次数，方便演示
counter = {"backup": 0, "sync": 0, "report": 0}


def job_backup():
    """模拟备份任务"""
    counter["backup"] += 1
    print(f"    [备份任务] 第 {counter['backup']} 次执行，时间 {now_str()}")


def job_sync():
    """模拟同步任务"""
    counter["sync"] += 1
    print(f"    [同步任务] 第 {counter['sync']} 次执行，时间 {now_str()}")


def job_report():
    """模拟报告任务"""
    counter["report"] += 1
    print(f"    [报告任务] 第 {counter['report']} 次执行，时间 {now_str()}")


print("=" * 55)
print("1. schedule 基本用法：注册任务")
print("=" * 55)
# schedule.every(N).单位.do(函数) 注册一个定时任务
schedule.every(2).seconds.do(job_backup)
print("  注册: schedule.every(2).seconds.do(job_backup)  -> 每 2 秒跑一次备份")
print("  -> schedule 把'定时'变成了声明式：告诉它多久跑一次，不用自己算时刻")

print("\n" + "=" * 55)
print("2. 各种间隔：seconds / minutes / hour / day / monday")
print("=" * 55)
# 演示各种间隔写法（这里只注册几个会触发的，其他的只打印说明）
schedule.every(3).seconds.do(job_sync)
print("  schedule.every(2).seconds.do(job)      每 2 秒")
print("  schedule.every(3).seconds.do(job)      每 3 秒")
print("  schedule.every(30).minutes.do(job)     每 30 分钟")
print("  schedule.every().hour.do(job)          每小时整点")
print("  schedule.every().day.at('10:30').do(job)   每天 10:30")
print("  schedule.every().monday.at('09:00').do(job) 每周一 9 点")
print("  schedule.every().wednesday.do(job)     每周三")
print("  -> .day.at('10:30') 指定每天几点；.monday/.wednesday 指定周几")

print("\n" + "=" * 55)
print("3. run_pending：跑到点的任务就执行，没到就立刻返回")
print("=" * 55)
print("  开始循环跑 schedule.run_pending()，限时 8 秒退出")
print(f"  开始时间: {now_str()}")
print()

# 教学脚本不能无限跑：用 time 限制运行 8 秒
start = time.monotonic()
TIME_LIMIT = 8.0
while time.monotonic() - start < TIME_LIMIT:
    schedule.run_pending()        # 检查所有任务，到点的执行，没到立刻返回
    time.sleep(0.5)               # 循环间隔，控制检查频率

print()
print(f"  达到 {TIME_LIMIT:.0f} 秒上限，退出循环，时间 {now_str()}")
print(f"  执行统计: 备份 {counter['backup']} 次, 同步 {counter['sync']} 次")
print("  -> run_pending 每次调用检查一遍'到点没'，到点的任务立刻执行")
print("  -> 循环里的 sleep(0.5) 控制检查频率，太频繁浪费 CPU，太慢任务会迟到")

print("\n" + "=" * 55)
print("4. 取消任务 / 查看所有任务")
print("=" * 55)
# 取消某个任务
job_to_cancel = schedule.every(5).seconds.do(job_report)
print(f"  注册了一个每 5 秒的报告任务，当前任务数: {len(schedule.jobs)}")
schedule.cancel_job(job_to_cancel)
print(f"  cancel_job 后，任务数: {len(schedule.jobs)}")
print("  -> every().do() 返回 job 对象，用 cancel_job(job) 取消")
print("  -> schedule.jobs 是所有任务的列表，len() 看有几个")
# 清空所有任务
schedule.clear()
print(f"  clear() 清空所有任务后，任务数: {len(schedule.jobs)}")

print("\n" + "=" * 55)
print("5. 带参数的任务：do(job, arg1, arg2)")
print("=" * 55)

def job_with_name(name, count):
    print(f"    [带参任务] {name} 第 {count} 次执行")

schedule.every(2).seconds.do(job_with_name, name="数据检查", count=1)
print("  schedule.every(2).seconds.do(job, name='数据检查', count=1)")
print("  -> do() 后面传的关键字参数会原样传给任务函数")
# 这个任务就不跑了，只演示注册语法
schedule.clear()

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. schedule.every(N).单位.do(job) 声明式注册任务，API 比 time.sleep 友好")
print("  2. while 循环里调 run_pending() 驱动，sleep 控制检查频率")
print("  3. schedule 是纯 Python 单线程，任务串行执行，一个慢了后面全堵，不适合精确定时")
print("  4. 生产环境长期定时建议用系统 cron 或任务计划，schedule 适合脚本内多任务调度")