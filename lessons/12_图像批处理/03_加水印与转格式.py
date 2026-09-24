"""模块12 示例03：加水印与转格式

演示用 ImageDraw 在图片上画文字水印、用 ImageFont 加载字体、
做半透明水印（RGBA + alpha 通道）、转格式与 quality 参数、
批量转格式、批量加水印。

运行命令：
    uv run python lessons/12_图像批处理/03_加水印与转格式.py
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)


def load_font(size):
    """加载 TrueType 字体：优先 Windows 黑体，失败回退默认字体"""
    for font_path in [
        "C:/Windows/Fonts/simhei.ttf",   # 黑体
        "C:/Windows/Fonts/msyh.ttc",     # 微软雅黑
        "C:/Windows/Fonts/arial.ttf",    # Arial
    ]:
        try:
            return ImageFont.truetype(font_path, size)
        except (OSError, IOError):
            continue
    print("  [提示] 未找到 TrueType 字体，用默认字体（可能不支持中文）")
    return ImageFont.load_default()


# ============================================================
# 第一部分：ImageDraw 画文字水印
# ============================================================
print("=" * 55)
print("第一部分：ImageDraw + text 加文字水印")
print("=" * 55)

# 创建一张底图，在它上面画文字
base = Image.new("RGB", (400, 200), (245, 245, 245))
draw = ImageDraw.Draw(base)   # 在 base 上创建绘图对象
print(f"  创建底图: {base.size}, 绘图对象类型: {type(draw).__name__}")

font = load_font(36)
# draw.text((x, y), 文字, fill=颜色, font=字体)
draw.text((20, 20), "图像批处理", fill=(60, 60, 60), font=font)

font_sm = load_font(20)
draw.text((20, 90), "Pillow 加水印演示", fill=(120, 120, 120), font=font_sm)
draw.text((20, 130), "2026-09-24", fill=(180, 180, 180), font=font_sm)

watermark_path = SAMPLE_DIR / "水印_不透明.png"
base.save(watermark_path)
print(f"  已保存: {watermark_path.name}")
print("  -> ImageDraw.Draw(img) 创建绘图对象，draw.text 画文字")
print("  -> fill 是文字颜色 (R,G,B)，font 不传则用默认小字体（不支持中文）")


# ============================================================
# 第二部分：半透明水印（RGBA + alpha 通道）
# ============================================================
print("\n" + "=" * 55)
print("第二部分：半透明水印（RGBA 模式 + alpha 通道）")
print("=" * 55)

# 做半透明水印的关键：图片要转成 RGBA 模式，文字颜色用 (R,G,B,A)
# A 是透明度：0 全透明（看不见），255 不透明
base2 = Image.new("RGB", (400, 200), (245, 245, 245))
d = ImageDraw.Draw(base2)
d.text((10, 10), "底图内容", fill=(80, 80, 80), font=load_font(28))

# 转 RGBA 才能用透明色画水印
base2 = base2.convert("RGBA")
draw2 = ImageDraw.Draw(base2)

# 加半透明水印：alpha=80 表示约 31% 不透明
font_wm = load_font(40)
draw2.text((120, 80), "CONFIDENTIAL", fill=(255, 0, 0, 80), font=font_wm)
# 底部加重复水印
for i in range(3):
    draw2.text((20 + i * 120, 150), "DRAFT", fill=(100, 100, 100, 60), font=load_font(24))

# 保存成 png（png 支持 RGBA，jpg 不支持透明通道）
wm_path = SAMPLE_DIR / "水印_半透明.png"
base2.save(wm_path)
print(f"  已保存: {wm_path.name}")
print("  -> 半透明水印套路：底图 convert('RGBA') -> fill 用 (R,G,B,A) -> 存 png")
print("  -> alpha 0~255：0 全透明、255 不透明，80 约 31% 可见")
print("  -> 注意：jpg 不支持透明通道，半透明水印图必须存 png")


# ============================================================
# 第三部分：转格式 + quality 参数
# ============================================================
print("\n" + "=" * 55)
print("第三部分：转格式与 quality 参数")
print("=" * 55)

# Pillow 根据 save 的后缀自动选格式
img = Image.open(SAMPLE_DIR / "水印_不透明.png")
print(f"  打开: 水印_不透明.png  format={img.format}  size={img.size}")

# png -> jpg，quality 控制压缩质量（1~95，默认 75）
for q in [95, 50, 20]:
    out = SAMPLE_DIR / f"转格式_quality{q}.jpg"
    img.convert("RGB").save(out, quality=q)
    print(f"    quality={q:2d}: {out.name}  {out.stat().st_size} 字节")
print("  -> quality 越高越清晰、文件越大；95 几乎无损，20 明显模糊")
print("  -> save 根据后缀定格式；png 转 jpg 要先 convert('RGB')，jpg 不支持 RGBA")


# ============================================================
# 第四部分：批量转格式——遍历目录 png -> jpg
# ============================================================
print("\n" + "=" * 55)
print("第四部分：批量转格式（遍历 sample 目录 png -> jpg）")
print("=" * 55)

converted_dir = SAMPLE_DIR / "converted"
converted_dir.mkdir(exist_ok=True)

count = 0
for p in sorted(SAMPLE_DIR.iterdir()):
    if p.suffix.lower() != ".png":
        continue  # 只转 png
    with Image.open(p) as im:
        im = im.convert("RGB")  # jpg 不支持 RGBA
        out = converted_dir / f"{p.stem}.jpg"
        im.save(out, quality=85)
        count += 1
print(f"  已把 {count} 张 png 转成 jpg（quality=85），存到 converted/")
print("  -> 批量转格式套路：iterdir 找源格式 -> open -> convert('RGB') -> save 新后缀")
print("  -> 反过来 jpg->png 同理，png 支持 RGBA 不用 convert")


# ============================================================
# 第五部分：批量加水印
# ============================================================
print("\n" + "=" * 55)
print("第五部分：批量加水印（右下角统一水印）")
print("=" * 55)

# 实战场景：给一堆图片统一加右下角半透明水印
wm_dir = SAMPLE_DIR / "watermarked"
wm_dir.mkdir(exist_ok=True)

EXTS = {".png", ".jpg", ".jpeg"}
font_batch = load_font(24)
wm_text = "Python自动化"
count = 0
for p in sorted(SAMPLE_DIR.iterdir()):
    if p.suffix.lower() not in EXTS:
        continue
    with Image.open(p) as im:
        im = im.convert("RGBA")
        draw = ImageDraw.Draw(im)
        # 右下角定位：用 textbbox 算文字宽高
        bbox = draw.textbbox((0, 0), wm_text, font=font_batch)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = im.width - tw - 10
        y = im.height - th - 10
        draw.text((x, y), wm_text, fill=(255, 255, 255, 120), font=font_batch)
        out = wm_dir / f"wm_{p.stem}.png"
        im.convert("RGB").save(out)  # 存回 RGB 避免兼容问题
        count += 1
print(f"  已给 {count} 张图片加右下角水印，存到 watermarked/")
print("  -> 批量加水印套路：open -> convert('RGBA') -> Draw -> text 定位 -> save")
print("  -> textbbox 返回 (左,上,右,下)，用来算文字尺寸做右下角定位")


# ============================================================
# 完成
# ============================================================
print("=" * 55)
print("完成!")
print("=" * 55)
print("""
要点:
1. ImageDraw.Draw(img) 创建绘图对象，draw.text((x,y), 文字, fill, font) 画文字
2. ImageFont.truetype(字体路径, 字号) 加载 TrueType 字体
3. 半透明水印：底图 convert('RGBA')，fill 用 (R,G,B,A)，存 png（jpg 不支持透明）
4. 转格式：save 根据后缀自动定格式，jpg 用 quality=1~95 控制质量
5. png 转 jpg 要先 convert('RGB')，因为 jpg 不支持 RGBA/P 模式
6. 批量套路：iterdir 遍历 -> open -> 处理 -> save 到子目录
""")