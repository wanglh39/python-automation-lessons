"""模块12 示例01：图像基本信息与打开

演示用 Pillow (PIL) 创建测试图片、打开图片、读取基本信息、模式转换。
Pillow 是 Python 事实上的图像处理标准库（导入名是 PIL，历史遗留）。

运行命令：
    uv run python lessons/12_图像批处理/01_基本信息与打开.py
"""

from pathlib import Path
from PIL import Image


# 定位 sample 目录
SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)


# ============================================================
# 第一部分：用 Image.new 创建测试图片
# ============================================================
print("=" * 55)
print("第一部分：用 Image.new 创建测试图片")
print("=" * 55)

# Image.new(mode, size, color)
#   mode:  "RGB" 真彩色 / "RGBA" 带透明 / "L" 灰度
#   size:  (宽, 高) 像素，注意宽在前
#   color: 填充色，RGB 用 (R,G,B)，RGBA 用 (R,G,B,A)，L 用单个整数
img_red = Image.new("RGB", (200, 100), (220, 60, 60))
red_path = SAMPLE_DIR / "纯色_red.png"
img_red.save(red_path)
print(f"  创建纯红图: mode={img_red.mode}, size={img_red.size}, 已存 {red_path.name}")

# 创建渐变图：逐像素填色（putpixel）。小图演示原理，大图太慢用 numpy
width, height = 128, 80
img_grad = Image.new("RGB", (width, height))
for x in range(width):
    for y in range(height):
        r = int(x / width * 255)   # 横向红渐变
        g = int(y / height * 255)  # 纵向绿渐变
        b = 128                    # 蓝色固定
        img_grad.putpixel((x, y), (r, g, b))
grad_path = SAMPLE_DIR / "渐变.png"
img_grad.save(grad_path)
print(f"  创建渐变图: {width}x{height}, 已存 {grad_path.name}")
print("  -> putpixel 逐像素填色，直观但慢；大图用 numpy 向量化快几百倍")

# 创建带透明通道的 RGBA 图片
img_alpha = Image.new("RGBA", (100, 100), (60, 120, 200, 128))
alpha_path = SAMPLE_DIR / "半透明.png"
img_alpha.save(alpha_path)
print(f"  创建半透明图: mode={img_alpha.mode}, alpha=128, 已存 {alpha_path.name}")
print("  -> RGBA 第 4 通道是 alpha：0 全透明、255 不透明，128 约 50%")

# 创建灰度图（模式 L，单通道）
img_gray = Image.new("L", (120, 80), 128)
gray_path = SAMPLE_DIR / "灰度.png"
img_gray.save(gray_path)
print(f"  创建灰度图: mode={img_gray.mode}, 已存 {gray_path.name}")
print("  -> 模式 L 每像素 1 字节，0 黑 255 白，存 png 文件比 RGB 小")


# ============================================================
# 第二部分：Image.open 打开图片并读取基本属性
# ============================================================
print("\n" + "=" * 55)
print("第二部分：Image.open 打开图片")
print("=" * 55)

img = Image.open(red_path)
print(f"  打开: {red_path.name}")
print(f"  类型: {type(img).__name__}")
print(f"  img.size   = {img.size}        # (宽, 高) 元组")
print(f"  img.mode   = {img.mode!r}        # 像素模式")
print(f"  img.format = {img.format!r}       # 文件格式（由内容识别，不看后缀）")
print("  -> size 是 (宽, 高)，宽在前高在后，和 numpy 数组 (高, 宽) 相反")
print("  -> Image.open 只读文件头部，不立刻解码全图，所以很快")
print("     第一次访问像素数据（如 resize、getpixel）才真正解码")


# ============================================================
# 第三部分：img.info 元信息
# ============================================================
print("\n" + "=" * 55)
print("第三部分：img.info 元信息")
print("=" * 55)

for name in ["纯色_red.png", "渐变.png", "半透明.png", "灰度.png"]:
    p = SAMPLE_DIR / name
    with Image.open(p) as im:
        print(f"\n  {name}:")
        print(f"    size={im.size}  mode={im.mode}  format={im.format}")
        print(f"    info={dict(im.info)}")
print("""
  -> info 是字典，内容因格式而异：
     PNG 可能有 dpi、icc_profile
     JPEG 可能有 quality、progression、jfif
     它只存"保存时指定的"元信息，不是 EXIF（EXIF 要用 img.getexif()）""")


# ============================================================
# 第四部分：模式转换 convert
# ============================================================
print("=" * 55)
print("第四部分：模式转换 img.convert()")
print("=" * 55)

img_rgb = Image.open(SAMPLE_DIR / "渐变.png")
print(f"  原图: mode={img_rgb.mode}, size={img_rgb.size}")

# RGB -> 灰度
img_l = img_rgb.convert("L")
img_l.save(SAMPLE_DIR / "渐变_灰度.png")
print(f"  convert('L'):  mode={img_l.mode}  # 转灰度，按 0.299R+0.587G+0.114B 加权")

# RGB -> RGBA（加透明通道，alpha 默认 255 即不透明）
img_rgba = img_rgb.convert("RGBA")
print(f"  convert('RGBA'): mode={img_rgba.mode}  # 加 alpha 通道（默认 255）")

# RGBA -> RGB（丢掉 alpha，用白色填充透明区）
img_back = img_rgba.convert("RGB")
print(f"  convert('RGB'):  mode={img_back.mode}  # 去透明通道")
print("  -> convert 常用于：彩色转灰度、加/去透明通道、二值化 convert('1')")
print("  -> 重要：jpg 不支持 RGBA，存 jpg 前必须 convert('RGB')")


# ============================================================
# 第五部分：with 上下文管理器
# ============================================================
print("\n" + "=" * 55)
print("第五部分：with 语句自动关闭文件句柄")
print("=" * 55)

print("""
  Image.open 返回的对象持有文件句柄，推荐用 with 自动关闭：

      with Image.open('x.png') as img:
          print(img.size)

  不用 with 时，img 在被垃圾回收前文件一直开着，批量处理几百张图
  可能耗尽系统文件句柄。with 语句保证用完即关。

  另一个细节：open 后只读了头部，with 块内访问 img.size 没问题，
  但 with 块外再访问已关闭图片的像素数据会报错。要长期持有像素，
  在 with 块内 img.load() 强制解码到内存，之后就不依赖文件了。
""")


# ============================================================
# 完成
# ============================================================
print("=" * 55)
print("完成!")
print("=" * 55)
print("""
要点:
1. Image.new(mode, size, color) 创建图片，mode 选 RGB/RGBA/L
2. Image.open(path) 打开图片，img.size/mode/format 是三个基本属性
3. img.info 字典存 DPI、quality 等附加元信息
4. img.convert('L'/'RGBA'/'RGB'/'1') 转换像素模式
5. 推荐用 with Image.open(...) as img 自动关闭文件句柄
6. putpixel 逐像素填色只适合小图演示，大图用 numpy 向量化
""")