"""模块12 示例02：缩放与裁剪

演示 img.resize、img.thumbnail、img.crop，以及不同重采样滤镜的效果差异，
最后批量遍历 sample 目录给所有图片生成缩略图。

运行命令：
    uv run python lessons/12_图像批处理/02_缩放与裁剪.py
"""

from pathlib import Path
import numpy as np
from PIL import Image


SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)


def make_gradient(width, height):
    """用 numpy 向量化生成 RGB 渐变图（比 putpixel 快几百倍）"""
    arr = np.zeros((height, width, 3), dtype=np.uint8)
    arr[:, :, 0] = np.linspace(0, 255, width, dtype=np.uint8)                    # 红色横向渐变
    arr[:, :, 1] = np.linspace(0, 255, height, dtype=np.uint8).reshape(-1, 1)    # 绿色纵向渐变
    arr[:, :, 2] = 128                                                           # 蓝色固定
    return Image.fromarray(arr)


# ============================================================
# 第一部分：准备一张测试图片
# ============================================================
print("=" * 55)
print("第一部分：准备测试图片")
print("=" * 55)

src = make_gradient(400, 300)
src_path = SAMPLE_DIR / "src_渐变.png"
src.save(src_path)
print(f"  已生成源图: {src_path.name} ({src.size[0]}x{src.size[1]})")
print("  -> 用 numpy 向量化生成，比 putpixel 快几百倍")
print("  -> 后续缩放/裁剪都基于这张图")


# ============================================================
# 第二部分：resize 缩放
# ============================================================
print("\n" + "=" * 55)
print("第二部分：img.resize((w, h)) 缩放")
print("=" * 55)

# resize 返回新图片，原图不变
small = src.resize((200, 150))
small.save(SAMPLE_DIR / "resize_200x150.png")
print(f"  resize((200, 150)): {src.size} -> {small.size}  # 缩小")
print("  -> resize 返回新图，原图不变；尺寸是 (宽, 高)")

big = src.resize((800, 600))
big.save(SAMPLE_DIR / "resize_800x600.png")
print(f"  resize((800, 600)): {src.size} -> {big.size}  # 放大也行")


# ============================================================
# 第三部分：重采样滤镜对比
# ============================================================
print("\n" + "=" * 55)
print("第三部分：重采样滤镜 NEAREST / BILINEAR / LANCZOS")
print("=" * 55)

# 放大时滤镜差异最明显：先把图缩成小图，再放大对比
tiny = src.resize((40, 30))
filters = {
    "NEAREST":  Image.NEAREST,    # 最近邻：最快，有锯齿
    "BILINEAR": Image.BILINEAR,   # 双线性：平滑，中等速度
    "LANCZOS":  Image.LANCZOS,    # 高质量，最慢（resize 默认就是它）
}
for name, flt in filters.items():
    up = tiny.resize((400, 300), resample=flt)
    up.save(SAMPLE_DIR / f"滤镜_{name}.png")
    print(f"  {name:8s}: 小图放大到 400x300，已存 滤镜_{name}.png")
print("  -> NEAREST 有锯齿、BILINEAR 平滑、LANCZOS 最清晰边缘锐利")
print("  -> resize 默认用 LANCZOS；速度敏感换 NEAREST/BILINEAR")


# ============================================================
# 第四部分：thumbnail 缩略图（原地修改）
# ============================================================
print("\n" + "=" * 55)
print("第四部分：img.thumbnail((max_w, max_h)) 缩略图")
print("=" * 55)

# thumbnail 和 resize 的关键区别：
#   1. 原地修改，返回 None（不是新图）
#   2. 保持宽高比，只给一个上限框，自动算比例
#   3. 只缩小不放大（比框大才缩，比框小不动）
img_t = src.copy()  # 先 copy，因为 thumbnail 会原地改
print(f"  copy 后: {img_t.size}")
img_t.thumbnail((100, 100))
print(f"  thumbnail((100,100)) 后: {img_t.size}  # 保持比例缩到框内")
img_t.save(SAMPLE_DIR / "thumbnail_100.png")
print("  -> thumbnail 原地修改、保持宽高比、只缩不放")
print("  -> 适合做缩略图：给个上限尺寸，它自动算比例，不会变形")


# ============================================================
# 第五部分：crop 裁剪
# ============================================================
print("\n" + "=" * 55)
print("第五部分：img.crop((left, top, right, bottom)) 裁剪")
print("=" * 55)

# crop 的参数是 (左, 上, 右, 下) 四个坐标，不是 (x, y, 宽, 高)
# 坐标原点在左上角，y 轴向下
box = (100, 75, 300, 225)  # 左100 上75 右300 下225
cropped = src.crop(box)
cropped.save(SAMPLE_DIR / "crop_中间.png")
print(f"  crop((100, 75, 300, 225)): {src.size} -> {cropped.size}")
print(f"  裁出来的尺寸 = (右-左, 下-上) = ({box[2]-box[0]}, {box[3]-box[1]})")
print("  -> 参数是 (左, 上, 右, 下) 四个坐标，不是 (x, y, 宽, 高)，新手常搞错")

# 裁左上角四分之一
w, h = src.size
quarter = src.crop((0, 0, w // 2, h // 2))
quarter.save(SAMPLE_DIR / "crop_左上四分之一.png")
print(f"  裁左上四分之一: -> {quarter.size}")


# ============================================================
# 第六部分：批量缩放——遍历目录生成缩略图
# ============================================================
print("\n" + "=" * 55)
print("第六部分：批量生成缩略图（遍历 sample 目录）")
print("=" * 55)

# 实战场景：一个目录里一堆大图，全部生成缩略图存到子目录
EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}
thumb_dir = SAMPLE_DIR / "thumbs"
thumb_dir.mkdir(exist_ok=True)

count = 0
for p in sorted(SAMPLE_DIR.iterdir()):
    if p.suffix.lower() not in EXTS:
        continue  # 跳过非图片和子目录
    with Image.open(p) as im:
        im = im.convert("RGB")  # 统一转 RGB，避免 RGBA/P 模式存 jpg 报错
        im.thumbnail((120, 120))
        out = thumb_dir / f"thumb_{p.stem}.png"
        im.save(out)
        count += 1
        print(f"  {p.name:24s} -> thumbs/{out.name}  {im.size}")
print(f"  共生成 {count} 张缩略图")
print("  -> 批量套路：iterdir 遍历 -> open -> thumbnail -> save 到子目录")
print("  -> 存 jpg 前要 convert('RGB')，jpg 不支持 RGBA/P 模式")


# ============================================================
# 完成
# ============================================================
print("=" * 55)
print("完成!")
print("=" * 55)
print("""
要点:
1. img.resize((w,h), resample=...) 返回新图，可放大可缩小
2. img.thumbnail((max_w, max_h)) 原地改、保比例、只缩不放，做缩略图首选
3. img.crop((左, 上, 右, 下)) 裁剪，注意是坐标不是宽高
4. 滤镜：NEAREST 快有锯齿、BILINEAR 平滑、LANCZOS 高质量（默认）
5. 批量缩略图：iterdir 遍历 -> open -> thumbnail -> save，jpg 先 convert('RGB')
""")