"""守护进程思路 —— 让脚本在后台长期运行

讲解让脚本长期在后台跑的几种方式：while True 守护、threading 后台线程、
nohup/systemd/cron/任务计划/supervisor/PM2 等系统级方案。
本脚本以讲解为主，代码片段演示，不真的长期运行。

运行: uv run python lessons/05_定时监控/04_守护进程思路.py
"""
import time
import threading
from datetime import datetime


def now_str():
    return datetime.now().strftime("%H:%M:%S")


print("=" * 55)
print("1. 最简单：while True + time.sleep 守护循环")
print("=" * 55)
print("  思路：主程序用 while True 一直循环，每轮干活 + sleep")
print("  代码:")
print("    while True:")
print("        do_job()")
print("        time.sleep(60)")
print()
print("  实际演示（跑 3 轮就退出，不真的无限跑）:")
for i in range(1, 4):
    print(f"    第 {i} 轮守护，时间 {now_str()}")
    time.sleep(0.5)
print("  -> 优点：零依赖、好理解、改起来快")
print("  -> 缺点：关了终端就没了、崩了没人管、开机不会自启")
print("  -> 适合：临时跑几小时的脚本、开发调试")

print("\n" + "=" * 55)
print("2. threading：让任务在后台线程跑，主程序不阻塞")
print("=" * 55)
# 演示后台线程：daemon=True 的线程会随主线程退出而退出
stop_flag = threading.Event()


def background_worker():
    """后台工作线程"""
    count = 0
    while not stop_flag.is_set():
        count += 1
        print(f"    [后台线程] 第 {count} 次干活，时间 {now_str()}")
        stop_flag.wait(0.5)     # 等 0.5 秒或被 stop_flag 唤醒


print("  启动后台线程，主线程同时干别的事...")
worker = threading.Thread(target=background_worker, daemon=True)
worker.start()

# 主线程干点别的
time.sleep(1.8)
print("  [主线程] 我在干别的事，后台线程一直在跑")

# 停止后台线程
stop_flag.set()
worker.join(timeout=2)
print("  已通知后台线程停止")
print("  -> daemon=True 的线程是'守护线程'，主线程退出时它跟着退")
print("  -> threading.Event 用来优雅通知线程停止，比直接 kill 干净")
print("  -> 适合：一个程序里既要响应前台又要后台定时干活（如 Web 服务 + 定时清理）")

print("\n" + "=" * 55)
print("3. Windows 后台运行：pythonw.exe")
print("=" * 55)
print("  python script.py       -> python.exe，带控制台窗口，关窗口就停")
print("  pythonw script.py      -> pythonw.exe，无窗口后台运行")
print()
print("  启动后关掉命令行窗口，脚本继续跑。要停止得用任务管理器结束 pythonw.exe 进程")
print("  -> 适合：Windows 上简单后台脚本，不想看到黑窗口")
print("  -> 缺点：看不到输出、崩了不知道、开机不自启")

print("\n" + "=" * 55)
print("4. Linux 后台运行：nohup / & / systemd")
print("=" * 55)
print("  方式 A: nohup + &  (临时后台)")
print("    nohup python script.py > output.log 2>&1 &")
print("    -> nohup 让进程忽略挂断信号（关 SSH 也不停）")
print("    -> & 放到后台，> output.log 把输出存日志，2>&1 错误也进日志")
print("    -> 停止: kill <PID>  或  pkill -f script.py")
print()
print("  方式 B: systemd  (生产级，推荐)")
print("    写一个 /etc/systemd/system/myapp.service:")
print("      [Unit]")
print("      Description=My Python App")
print("      [Service]")
print("      ExecStart=/usr/bin/python /path/to/script.py")
print("      Restart=always            # 崩了自动重启")
print("      User=myuser")
print("      [Install]")
print("      WantedBy=multi-user.target")
print("    然后: systemctl enable myapp   # 开机自启")
print("          systemctl start myapp    # 启动")
print("          systemctl status myapp   # 看状态")
print("    -> systemd 是 Linux 现代发行版的标准进程管理器，生产环境首选")
print("    -> 自带重启、日志、开机自启、权限隔离，比 nohup 专业得多")

print("\n" + "=" * 55)
print("5. 系统级定时：cron / 任务计划程序")
print("=" * 55)
print("  Linux: crontab -e 编辑定时任务")
print("    # 每天凌晨 2 点备份")
print("    0 2 * * * /usr/bin/python /path/to/backup.py")
print("    # 每 10 分钟同步一次")
print("    */10 * * * * /usr/bin/python /path/to/sync.py")
print("    -> 5 个字段: 分 时 日 月 周，* 表示任意，*/10 表示每 10 分钟")
print()
print("  Windows: 任务计划程序（taskschd.msc）或 schtasks 命令")
print("    schtasks /create /tn MyTask /tr 'python C:\\script.py' /sc daily /st 02:00")
print("    -> /sc daily 每天跑，/st 02:00 凌晨 2 点，/tn 任务名")
print("    -> 也可以在图形界面里点'创建基本任务'，按向导设")
print()
print("  -> 系统级定时不要求 Python 一直挂着，到点系统自动拉起脚本跑完就退")
print("  -> 适合：每天/每小时级的定期任务，比让 Python 一直 sleep 稳得多")

print("\n" + "=" * 55)
print("6. 进程管理工具：supervisor / PM2")
print("=" * 55)
print("  supervisor (Python 生态，Linux):")
print("    配置 /etc/supervisor/conf.d/myapp.conf:")
print("      [program:myapp]")
print("      command=python /path/to/script.py")
print("      autorestart=true")
print("    supervisorctl start/stop/status myapp")
print()
print("  PM2 (Node 生态，跨平台):")
print("    pm2 start script.py --interpreter python --name myapp")
print("    pm2 list / pm2 logs / pm2 restart myapp")
print("    pm2 startup        # 开机自启")
print("    pm2 save           # 保存当前进程列表")
print()
print("  -> 这类工具帮你管进程：崩了自动拉起、统一看日志、统一启停")
print("  -> 比裸 nohup 强，比 systemd 轻，跨平台（PM2）或 Python 友好（supervisor）")

print("\n" + "=" * 55)
print("7. 方案选择速查")
print("=" * 55)
print("  场景                        -> 推荐方案")
print("  临时跑几小时                -> while True + sleep")
print("  程序内多任务定时            -> schedule 库 或 threading")
print("  Windows 简单后台            -> pythonw.exe")
print("  Linux 临时后台              -> nohup + &")
print("  Linux 生产长期              -> systemd")
print("  每天定时跑一次              -> cron / 任务计划程序")
print("  多进程统一管理              -> supervisor / PM2")
print("  -> 越往下越稳但配置越重，按需选，别一上来就 systemd 杀鸡用牛刀")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. while True + sleep 最简单但最脆弱，适合临时脚本和调试")
print("  2. threading 让任务在后台跑，主程序不阻塞，适合程序内多任务")
print("  3. 生产环境用系统级方案：Linux systemd / Windows 任务计划，崩了能自启")
print("  4. 系统级定时（cron/任务计划）到点拉起脚本跑完就退，比 Python 一直挂着稳")