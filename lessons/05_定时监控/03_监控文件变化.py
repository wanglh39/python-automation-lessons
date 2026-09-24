"""watchdog 监控文件变化

演示 watchdog 库监控目录的增删改：定义事件处理器、启动 Observer、自动触发事件。
watchdog 底层用操作系统事件（Windows ReadDirectoryChangesW / Linux inotify / Mac FSEvents），
不用轮询，文件一变操作系统就推过来。

运行: uv run python lessons/05_定时监控/03_监控文件变化.py
"""
import time
from datetime import datetime
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def now_str():
    return datetime.now().strftime("%H:%M:%S")


# 收集事件，方便最后统计
events_log = []


class MyHandler(FileSystemEventHandler):
    """自定义事件处理器，重写 on_created/on_modified/on_deleted"""

    def on_created(self, event):
        if event.is_directory:
            return
        msg = f"[新建] {Path(event.src_path).name}  ({now_str()})"
        print(f"    {msg}")
        events_log.append("created")

    def on_modified(self, event):
        if event.is_directory:
            return
        msg = f"[修改] {Path(event.src_path).name}  ({now_str()})"
        print(f"    {msg}")
        events_log.append("modified")

    def on_deleted(self, event):
        if event.is_directory:
            return
        msg = f"[删除] {Path(event.src_path).name}  ({now_str()})"
        print(f"    {msg}")
        events_log.append("deleted")


print("=" * 55)
print("1. 准备监控目录")
print("=" * 55)
# 在脚本同目录下建一个临时监控目录，跑完删掉
watch_dir = Path(__file__).parent / "_watch_test"
watch_dir.mkdir(exist_ok=True)
print(f"  监控目录: {watch_dir}")
print("  -> 教学脚本自己建目录、自己造文件变化，方便演示完自动清理")

print("\n" + "=" * 55)
print("2. 定义事件处理器：继承 FileSystemEventHandler")
print("=" * 55)
print("  class MyHandler(FileSystemEventHandler):")
print("      def on_created(self, event): ...   # 文件新建时触发")
print("      def on_modified(self, event): ...  # 文件修改时触发")
print("      def on_deleted(self, event): ...   # 文件删除时触发")
print("  -> event.src_path 是变化的文件路径，event.is_directory 判断是不是目录")

print("\n" + "=" * 55)
print("3. 启动 Observer 监控目录")
print("=" * 55)
observer = Observer()
observer.schedule(MyHandler(), path=str(watch_dir), recursive=False)
observer.start()
print(f"  Observer 已启动，监控: {watch_dir.name}")
print("  -> observer.schedule(handler, path, recursive) 把处理器挂到目录上")
print("  -> recursive=True 递归监控子目录，False 只监控顶层")
print("  -> observer.start() 在后台线程启动监听，不阻塞主线程")

print("\n" + "=" * 55)
print("4. 触发文件变化：自己造几个事件")
print("=" * 55)
# 给 watchdog 一点时间启动好
time.sleep(0.3)

# 触发新建 + 修改
print("  操作: 新建 a.txt")
test_file = watch_dir / "a.txt"
test_file.write_text("hello", encoding="utf-8")
time.sleep(0.5)

print("  操作: 修改 a.txt（追加内容）")
test_file.write_text("hello world", encoding="utf-8")
time.sleep(0.5)

print("  操作: 新建 b.txt")
test_file2 = watch_dir / "b.txt"
test_file2.write_text("second file", encoding="utf-8")
time.sleep(0.5)

print("  操作: 删除 a.txt")
test_file.unlink()
time.sleep(0.5)

print("  操作: 删除 b.txt")
test_file2.unlink()
time.sleep(0.5)

print("\n" + "=" * 55)
print("5. 停止监控并统计")
print("=" * 55)
observer.stop()           # 停止监听
observer.join()           # 等监听线程退出
print("  Observer 已停止")

# 统计事件
from collections import Counter
counts = Counter(events_log)
print(f"  共捕获 {len(events_log)} 个事件: {dict(counts)}")
print("  -> 注意：修改文件常常触发两次 on_modified（一次写内容、一次关文件），这是正常的")

# 清理临时目录
try:
    watch_dir.rmdir()
    print(f"  已清理临时目录: {watch_dir.name}")
except OSError:
    print(f"  目录非空，未清理: {watch_dir.name}")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. 继承 FileSystemEventHandler 重写 on_created/on_modified/on_deleted 处理变化")
print("  2. Observer 在后台线程监听，start 不阻塞，stop + join 优雅退出")
print("  3. watchdog 底层是操作系统事件（inotify/FSEvents/ReadDirectoryChangesW），不用轮询")
print("  4. 典型用途：日志监控、配置热更新、自动同步、构建触发")