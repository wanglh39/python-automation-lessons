"""下载文件 —— 简单下载 + 流式下载大文件 + 进度显示

演示用 requests 下载文件：小文件直接下、大文件用 stream 流式下、显示下载进度。
大文件必须用 stream=True + iter_content 分块写，否则会一次性读进内存。

运行: uv run python lessons/03_网络请求/04_下载文件.py
"""
from pathlib import Path
import requests

# sample 目录存下载的文件
sample = Path(__file__).parent / "sample"
sample.mkdir(exist_ok=True)

# 测试用的小图片（httpbin.org 提供）
IMAGE_URL = "https://httpbin.org/image/png"
# 一个稍大的文件用于演示流式下载（httpbin 的 /stream 生成多行 JSON）
STREAM_URL = "https://httpbin.org/stream/20"


def safe_download(url, timeout=15):
    """带异常处理的下载请求：返回 response 或 None"""
    try:
        return requests.get(url, timeout=timeout, stream=True)
    except requests.exceptions.Timeout:
        print("  [超时] 下载超时，请检查网络速度")
        return None
    except requests.exceptions.ConnectionError:
        print("  [连接失败] 无法连接下载服务器，请检查网络或 VPN")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  [下载错误] {type(e).__name__}: {e}")
        return None


print("=" * 55)
print("1. 简单下载：小文件直接 get + 写文件")
print("=" * 55)
print(f"  下载: {IMAGE_URL}")
print(f"  保存到: sample/downloaded.png")
resp = safe_download(IMAGE_URL)
if resp is not None and resp.ok:
    img_path = sample / "downloaded.png"
    # 小文件可以直接 resp.content（字节串）一次写入
    img_path.write_bytes(resp.content)
    size = len(resp.content)
    print(f"  下载完成: {size} 字节（约 {size / 1024:.1f} KB）")
    print(f"  Content-Type: {resp.headers.get('Content-Type')}")
elif resp is not None:
    print(f"  [HTTP {resp.status_code}] 下载失败")
print("  -> 小文件用 resp.content 一次性读字节，write_bytes 一次性写")

print("\n" + "=" * 55)
print("2. 流式下载：大文件分块写，不撑爆内存")
print("=" * 55)
print(f"  下载: {STREAM_URL}")
print("  用 stream=True + iter_content 分块读取:")
resp = safe_download(STREAM_URL)
if resp is not None and resp.ok:
    big_path = sample / "stream_data.txt"
    # stream=True 时 resp.content 不会立即下载，要 iter_content 逐块读
    chunk_size = 1024   # 每块 1KB
    total = 0
    with open(big_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size):
            if chunk:                  # 过滤掉 keep-alive 的空块
                f.write(chunk)
                total += len(chunk)
    print(f"  下载完成: {total} 字节（约 {total / 1024:.1f} KB）")
    print(f"  保存到: sample/stream_data.txt")
elif resp is not None:
    print(f"  [HTTP {resp.status_code}] 下载失败")
print("  -> stream=True 不立即下载，iter_content 按块读，内存占用恒定")

print("\n" + "=" * 55)
print("3. 带进度条的下载：显示已下载/总大小")
print("=" * 55)
print(f"  下载: {IMAGE_URL}")
print("  进度显示:")
resp = safe_download(IMAGE_URL)
if resp is not None and resp.ok:
    img_path = sample / "downloaded_progress.png"
    # 从响应头取总大小（不一定都有）
    total_size = int(resp.headers.get("Content-Length", 0))
    downloaded = 0
    chunk_size = 512   # 小块，方便看进度
    with open(img_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                # 打印进度
                if total_size > 0:
                    percent = downloaded * 100 // total_size
                    bar = "#" * (percent // 5) + "-" * (20 - percent // 5)
                    print(f"\r  [{bar}] {percent:>3}% ({downloaded}/{total_size} 字节)", end="")
                else:
                    print(f"\r  已下载 {downloaded} 字节", end="")
    print()   # 换行
    print(f"  下载完成: {downloaded} 字节")
elif resp is not None:
    print(f"  [HTTP {resp.status_code}] 下载失败")
print("  -> Content-Length 给总大小，iter_content 累加已下载，算百分比")

print("\n" + "=" * 55)
print("4. 下载到指定路径 + 文件名从 URL 取")
print("=" * 55)
# 从 URL 提取文件名（实际项目里常用）
url = "https://httpbin.org/image/png"
filename = url.rsplit("/", 1)[-1]   # 取 URL 最后一段当文件名
print(f"  URL: {url}")
print(f"  提取文件名: {filename}")
dest = sample / filename
resp = safe_download(url)
if resp is not None and resp.ok:
    dest.write_bytes(resp.content)
    print(f"  保存到: {dest}")
    print(f"  大小: {dest.stat().st_size} 字节")
elif resp is not None:
    print(f"  [HTTP {resp.status_code}] 下载失败")
print("  -> url.rsplit('/', 1)[-1] 取最后一段当文件名，简单场景够用")

print("\n" + "=" * 55)
print("5. 关键参数说明")
print("=" * 55)
print("  stream=True       -> 不立即下载，配合 iter_content 流式读")
print("  iter_content(n)   -> 每次返回最多 n 字节的块，循环写到文件")
print("  resp.content      -> 一次性读全部（小文件才用，大文件会撑爆内存）")
print("  Content-Length    -> 响应头里的总大小，用于算进度百分比")
print("  write_bytes(data) -> pathlib 的方法，等价于 open('wb').write(data)")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. 小文件用 resp.content 一次读写，大文件必须 stream=True + iter_content")
print("  2. 进度条靠 Content-Length（总大小）+ 累加已下载字节数算百分比")
print("  3. 下载和请求一样要 try/except，网络断了要友好提示而不是崩溃")
print("  4. iter_content 的 chunk_size 一般设 8KB~64KB，太小慢，太大占内存")