"""截图与找图 —— pyautogui 视觉 API

演示 pyautogui 截图和找图：screenshot 全屏截图、region 区域截图、
locateOnScreen 找图、locateCenterOnScreen 找中心、locateAllOnScreen 找全部。
截图功能可以真实运行（保存到 sample 目录，安全）。找图用刚才截的图做完整
流程演示。confidence 模糊匹配需要 opencv，本环境未安装时会说明。

运行: uv run python lessons/10_GUI桌面自动化/03_截图与找图.py
"""
from pathlib import Path

import pyautogui


# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

# 截图保存到 sample 目录
SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)


print("=" * 55)
print("1. screenshot：全屏截图（真实执行，安全）")
print("=" * 55)
print("  即将截取全屏，保存到 sample/full_screen.png")
img = pyautogui.screenshot()
full_path = SAMPLE_DIR / "full_screen.png"
img.save(str(full_path))
print(f"  截图已保存: {full_path}")
print(f"  图片尺寸: {img.size}  (宽, 高)")
print(f"  文件大小: {full_path.stat().st_size} 字节")
print("  -> screenshot() 返回 PIL.Image.Image 对象，能直接 save/crop/getpixel")
print("  -> 不传参数就是全屏；不 save 的话图片只在内存里")

print("\n" + "=" * 55)
print("2. screenshot(region=...)：区域截图")
print("=" * 55)
# region 是 (left, top, width, height)，不是 (x1, y1, x2, y2)
region = (0, 0, 300, 200)
print(f"  即将截取区域 region={region} (左, 上, 宽, 高)")
region_img = pyautogui.screenshot(region=region)
region_path = SAMPLE_DIR / "region.png"
region_img.save(str(region_path))
print(f"  区域截图已保存: {region_path}")
print(f"  图片尺寸: {region_img.size}")
print("  -> region=(left, top, width, height)，注意是宽高不是右下角坐标")
print("  -> 适合只截某个窗口/某块区域，比全屏截图小、找图更快")

print("\n" + "=" * 55)
print("3. locateOnScreen：在屏幕上找一张图（完整流程演示）")
print("=" * 55)
# 用刚才截的小区域图去全屏找，肯定能找到（就是屏幕左上角那块）
print(f"  用刚才的区域截图 {region_path.name} 作为目标图，在全屏找它的位置")
print("  -> locateOnScreen(image) 返回 Box(left, top, width, height) 或 None")
try:
    box = pyautogui.locateOnScreen(str(region_path))
    if box:
        print(f"  找到了! Box(left={box.left}, top={box.top}, "
              f"width={box.width}, height={box.height})")
        print(f"  -> 应该就是 ({region[0]}, {region[1]}, "
              f"{region[2]}, {region[3]})，跟截的区域一致")
    else:
        print("  没找到（返回 None）")
        print("  -> 可能屏幕内容变了（区域截图后屏幕有变化）")
except pyautogui.ImageNotFoundException:
    print("  没找到（抛 ImageNotFoundException）")
    print("  -> pyautogui 较新版本找不到图会抛异常，老版本返回 None")
except Exception as e:
    print(f"  [找图出错] {type(e).__name__}: {e}")
print("  -> 精确匹配要求像素完全一致，差一点颜色就找不到（见第 6 节 confidence）")

print("\n" + "=" * 55)
print("4. locateCenterOnScreen：找图的中心点")
print("=" * 55)
print("  -> locateCenterOnScreen 返回 (x, y) 中心点，方便直接 click")
print("  -> 等价于 locateOnScreen 拿到 Box 再算中心，但一步到位")
try:
    center = pyautogui.locateCenterOnScreen(str(region_path))
    if center:
        cx, cy = center
        print(f"  中心点: ({cx}, {cy})")
        print(f"  -> 应该是 ({region[0] + region[2]//2}, "
              f"{region[1] + region[3]//2})")
        print("  -> 典型用法：pyautogui.click(*pyautogui.locateCenterOnScreen('btn.png'))")
    else:
        print("  没找到（返回 None）")
except pyautogui.ImageNotFoundException:
    print("  没找到（抛 ImageNotFoundException）")
except Exception as e:
    print(f"  [找图出错] {type(e).__name__}: {e}")

print("\n" + "=" * 55)
print("5. locateAllOnScreen：找所有匹配位置")
print("=" * 55)
print("  -> locateAllOnScreen 返回生成器，每个元素是一个 Box")
print("  -> 适合屏幕上有多个相同图标（如多个相同按钮）都要点的情况")
print("  演示找刚才的区域图（应该只有一处匹配）：")
try:
    all_boxes = list(pyautogui.locateAllOnScreen(str(region_path)))
    print(f"  共找到 {len(all_boxes)} 处匹配:")
    for i, b in enumerate(all_boxes):
        print(f"    第 {i+1} 处: Box(left={b.left}, top={b.top}, "
              f"width={b.width}, height={b.height})")
except pyautogui.ImageNotFoundException:
    print("  没找到（抛 ImageNotFoundException）")
except Exception as e:
    print(f"  [找图出错] {type(e).__name__}: {e}")
print("  -> 注意 locateAllOnScreen 返回的是生成器，要 list() 才能取长度/重复遍历")

print("\n" + "=" * 55)
print("6. confidence 模糊匹配（需要 opencv）")
print("=" * 55)
try:
    import cv2  # noqa: F401
    has_cv2 = True
except ImportError:
    has_cv2 = False

if has_cv2:
    print("  检测到 opencv 已安装，可以使用 confidence 参数")
    print("  -> confidence=0.9 表示相似度 ≥ 90% 就算匹配")
    try:
        box = pyautogui.locateOnScreen(str(region_path), confidence=0.9)
        print(f"  confidence=0.9 找图结果: {box}")
    except Exception as e:
        print(f"  [模糊找图出错] {type(e).__name__}: {e}")
else:
    print("  检测到 opencv 未安装，不能用 confidence 参数")
    print("  -> 装上后才能用：uv add opencv-python")
    print("  -> 不装也能用 locateOnScreen，只是精确像素匹配，容易因抗锯齿/主题变化找不到")
print("  -> confidence 取值 0~1，常用 0.9~0.95；太低会误匹配，太高又找不到")
print("  -> 模糊匹配底层用 cv2.matchTemplate 算相似度矩阵，比精确匹配慢但鲁棒")

print("\n" + "=" * 55)
print("7. 找图实战套路与注意事项")
print("=" * 55)
print("  典型流程：")
print("    1. 手动截一张按钮的小图存成 btn.png（用系统截图工具框选按钮）")
print("    2. 脚本里 center = pyautogui.locateCenterOnScreen('btn.png', confidence=0.9)")
print("    3. if center: pyautogui.click(*center)")
print("    4. else: print('按钮没找到，可能界面变了')")
print("  注意：")
print("    - 目标图要尽量小，只截按钮本身，别带背景，匹配快且准")
print("    - 不同分辨率/主题/DPI 下按钮长得不一样，换机器可能要重新截")
print("    - 找图很慢（遍历每个位置），别在循环里高频调，找到后记住坐标复用")
print("    - grayscale=True 可灰度匹配，速度快一倍，颜色不重要时用")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. screenshot() 全屏截图，screenshot(region=(l,t,w,h)) 区域截图，返回 PIL.Image")
print("  2. locateOnScreen 找图返回 Box，locateCenterOnScreen 返回中心点 (x,y)")
print("  3. locateAllOnScreen 找全部匹配，返回生成器，list() 转列表")
print("  4. confidence 模糊匹配需要 opencv-python，精确匹配差一像素就找不到")
print("  5. 找图慢且脆，目标图要小、换机器要重截，找到后记住坐标复用")