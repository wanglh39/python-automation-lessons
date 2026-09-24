# 模块 12：图像批处理

> 用 Python 批量处理图片：读取信息、缩放裁剪、加水印、转格式。Pillow 是 Python 事实上的图像处理标准库，本模块演示它的"怎么用"——每个脚本自动生成测试图片，可独立运行，不依赖外部素材。

## 核心库一览

| 库 | 导入名 | 来源 | 用途 | 是否需安装 |
| --- | --- | --- | --- | --- |
| Pillow | `from PIL import Image` | 第三方 | 图像读写、缩放、裁剪、转格式 | 是（`uv add pillow`） |
| Pillow | `from PIL import ImageDraw` | 第三方 | 在图片上画文字/线条/矩形 | 同上（Pillow 自带） |
| Pillow | `from PIL import ImageFont` | 第三方 | 加载 TrueType 字体画文字 | 同上（Pillow 自带） |

> 关键认知：Pillow 的导入名是 `PIL`（历史遗留，见底层原理），不是 `pillow`。装的是 `pillow`，import 的是 `PIL`。

## Pillow 能做什么

- **读写**：打开 jpg/png/bmp/gif/webp/tiff 等，按后缀自动识别格式；`save` 按后缀自动选格式
- **基本信息**：`img.size` 尺寸、`img.mode` 像素模式、`img.format` 文件格式、`img.info` 元信息（DPI、quality 等）
- **几何变换**：`resize` 缩放、`thumbnail` 缩略图（保比例）、`crop` 裁剪、`rotate` 旋转、`transpose` 翻转
- **像素模式转换**：`convert('L')` 转灰度、`convert('RGBA')` 加透明通道、`convert('1')` 二值化
- **绘图**：`ImageDraw` 画文字、线条、矩形、椭圆；`ImageFont` 加载 ttf/ttc 字体
- **合成**：`Image.alpha_composite` 合并透明层、`paste` 粘贴图片、半透明水印靠 RGBA + alpha

## 常见场景

| 场景 | 关键 API |
| --- | --- |
| 批量生成缩略图 | `glob` 遍历 → `open` → `thumbnail((w,h))` → `save` |
| 给图片统一加水印 | `convert('RGBA')` → `ImageDraw.Draw` → `text` → `save` |
| 批量转格式 jpg↔png | `open` → `convert('RGB')` → `save('x.jpg', quality=85)` |
| 上传前压缩 | `save('x.jpg', quality=85, optimize=True)` |
| 提取图片尺寸做筛选 | `Image.open(p).size`，不用真解码（`Image.open` 只读头部） |
| 做半透明角标 | RGBA 模式 + `fill=(R,G,B,A)`，A 越小越透明 |

## 核心 API 速查

```python
from PIL import Image, ImageDraw, ImageFont

# --- 读写与信息 ---
img = Image.open('x.png')          # 打开（只读头部，访问像素才解码）
print(img.size, img.mode, img.format, img.info)
img.save('y.jpg', quality=85)      # 按后缀定格式，quality 仅 jpg 有效

# --- 创建图片 ---
img = Image.new('RGB', (宽, 高), (R, G, B))      # 纯色
img = Image.new('RGBA', (宽, 高), (R, G, B, A))  # 带透明

# --- 缩放与裁剪 ---
small = img.resize((w, h), resample=Image.LANCZOS)  # 返回新图，可放大
img.thumbnail((max_w, max_h))                        # 原地改、保比例、只缩不放
cropped = img.crop((左, 上, 右, 下))                 # 注意是坐标不是宽高

# --- 模式转换 ---
gray = img.convert('L')          # 转灰度
rgba = img.convert('RGBA')       # 加透明通道

# --- 绘图与水印 ---
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 36)
draw.text((x, y), '水印文字', fill=(255, 0, 0), font=font)        # 不透明
draw.text((x, y), '半透明', fill=(255, 0, 0, 80), font=font)      # alpha=80 约 31% 可见
bbox = draw.textbbox((0, 0), '文字', font=font)                   # 算文字宽高做定位

# --- 批量套路 ---
from pathlib import Path
for p in Path('imgs').glob('*.jpg'):
    with Image.open(p) as im:
        im.thumbnail((200, 200))
        im.save(f'thumbs/{p.stem}.png')
```

## 本模块示例

| 脚本 | 演示 |
| --- | --- |
| [01_基本信息与打开.py](01_基本信息与打开.py) | `Image.new` 创建测试图片、`Image.open` 打开、`size/mode/format/info` 读取、`convert` 模式转换 |
| [02_缩放与裁剪.py](02_缩放与裁剪.py) | `resize`、`thumbnail`、`crop`、LANCZOS/BILINEAR/NEAREST 滤镜对比、批量生成缩略图 |
| [03_加水印与转格式.py](03_加水印与转格式.py) | `ImageDraw.text` 加水印、`ImageFont.truetype` 加载字体、RGBA 半透明水印、转格式与 quality、批量加水印 |

运行方式：

```bash
cd "C:\Users\wlh19\Desktop\python自动化"
uv run python lessons/12_图像批处理/01_基本信息与打开.py
uv run python lessons/12_图像批处理/02_缩放与裁剪.py
uv run python lessons/12_图像批处理/03_加水印与转格式.py
```

> 三个脚本均自动在 `sample/` 子目录生成测试图片，不依赖外部素材，可独立运行。重复运行会覆盖同名文件。

## 底层原理

### 1. Pillow 是 PIL 的 fork

PIL（Python Imaging Library）是 1995 年的老库，2009 年后停止维护，不支持 Python 3。社区 fork 出 **Pillow** 继续维护，成为事实标准。为了向后兼容，Pillow 保留了 `PIL` 这个导入名——所以装 `pillow`、`import PIL`，这是历史遗留，不是笔误。

### 2. 图像模式：RGB / RGBA / L / 1 / P

`img.mode` 描述每个像素用几个通道、每通道几位：

| 模式 | 含义 | 每像素 | 典型用途 |
| --- | --- | --- | --- |
| `RGB` | 真彩色 | 3 字节 | 普通照片，jpg 只能存这个 |
| `RGBA` | 真彩色 + 透明 | 4 字节 | 带 alpha 通道，png/webp 支持，jpg 不支持 |
| `L` | 灰度 | 1 字节 | 黑白照片、灰度处理 |
| `1` | 二值 | 1 位 | 黑白线稿，每像素只有 0/1 |
| `P` | 调色板 | 1 字节 + 调色板 | gif 用，最多 256 色 |

关键坑：**jpg 不支持 RGBA/P/L 带 alpha**，存 jpg 前要 `convert('RGB')`，否则报错 `cannot write mode RGBA as JPEG`。

### 3. resize 的重采样滤镜

缩放本质是"在离散像素网格间插值"，不同滤镜用不同插值算法：

| 滤镜 | 算法 | 速度 | 质量 | 适用 |
| --- | --- | --- | --- | --- |
| `NEAREST` | 最近邻：直接取最近像素 | 最快 | 差，有锯齿 | 像素艺术、缩放整数倍 |
| `BILINEAR` | 双线性：2x2 邻域加权平均 | 中 | 中，较平滑 | 缩小、一般用途 |
| `BICUBIC` | 双三次：4x4 邻域三次多项式 | 慢 | 好 | 放大照片 |
| `LANCZOS` | Lanczos 重采样：sinc 函数加窗卷积 | 最慢 | 最好，边缘锐利 | 高质量缩放（resize 默认） |

`resize` 默认用 `LANCZOS`；`thumbnail` 默认也用 `LANCZOS`。放大时滤镜差异最明显——NEAREST 出锯齿、LANCZOS 保边缘。缩小差别小，速度敏感时用 `BILINEAR`。