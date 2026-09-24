# 模块 6：办公自动化

> 办公三件套——Word、PPT、PDF，天天手动改累死人。Python 有一组专门读写这些格式的库：python-docx 管 Word、python-pptx 管 PPT、pdfplumber 提取 PDF。本模块演示"用代码生成报告、改 PPT、抽 PDF 内容"，把重复的办公活儿交给脚本。

## 核心库一览

| 库 | 来源 | 用途 | 推荐度 |
|---|:---:|---|:---:|
| `python-docx` | 第三方 | 读写 .docx 文档：标题、段落、表格、样式 | ★★★★ |
| `python-pptx` | 第三方 | 读写 .pptx 演示文稿：幻灯片、文本框、表格 | ★★★★ |
| `pdfplumber` | 第三方 | 提取 PDF 文字、表格、文字位置（只读不能写） | ★★★★ |
| `reportlab` | 第三方 | 从零生成 PDF（pdfplumber 的互补：一个读一个写） | ★★★ |

## 各库定位

- **python-docx**：能创建新 .docx、读取已有 .docx、改段落文字、加表格、设字体样式。常用于批量生成报告、替换模板里的关键词、从表格里抽数据。**不能处理老的 .doc 格式**（那是二进制格式，和 .docx 完全不同）。
- **python-pptx**：能创建/读取 .pptx，往幻灯片上加文本框、表格、图片，设置字号颜色。常用于批量生成汇报 PPT、往模板里填数据。坐标用 Inches/Cm，内部换算成 EMU。
- **pdfplumber**：专门**提取** PDF 内容——文字、表格、每个字符的坐标。适合做"从 PDF 报表里抽数据进 Excel"。**不能创建 PDF**（创建用 reportlab），**扫描版 PDF 没有文字层**，得先用 OCR（如 pytesseract）识别成文字。

> **一句话区分**：docx/pptx 是"既能读又能写"，pdfplumber 是"只能读"，reportlab 是"只能写 PDF"。

## 核心 API 速查

```python
# --- python-docx（Word 文档）---
from docx import Document
from docx.shared import Pt, RGBColor

doc = Document()                          # 新建空文档
doc.add_heading('标题', level=1)          # 加标题（level 0-9）
p = doc.add_paragraph('一段文字')          # 加段落
run = p.add_run('加粗红字')                # 段落里加一段 run
run.bold = True
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
table = doc.add_table(rows=3, cols=2)     # 加表格
table.cell(0, 0).text = '左上'             # 填单元格
doc.save('报告.docx')                      # 保存

doc = Document('报告.docx')               # 读取
for p in doc.paragraphs:                  # 遍历段落
    print(p.text)
for t in doc.tables:                      # 遍历表格
    print(t.cell(0, 0).text)
```

```python
# --- python-pptx（PPT 演示文稿）---
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()                      # 新建空演示文稿
slide = prs.slides.add_slide(prs.slide_layouts[0])   # 加一张幻灯片（用版式 0）
txBox = slide.shapes.add_textbox(          # 加文本框
    Inches(1), Inches(1), Inches(8), Inches(2)
)
tf = txBox.text_frame
tf.text = '第一段'                         # 设文本
p = tf.add_paragraph()                     # 加段落
p.text = '第二段'
p.font.size = Pt(24)                       # 设字号
table = slide.shapes.add_table(2, 3,       # 加表格
    Inches(1), Inches(4), Inches(6), Inches(1)
).table
prs.save('演示.pptx')                      # 保存

prs = Presentation('演示.pptx')           # 读取
for slide in prs.slides:                   # 遍历幻灯片
    for shape in slide.shapes:            # 遍历形状
        if shape.has_text_frame:
            print(shape.text_frame.text)
```

```python
# --- pdfplumber（提取 PDF 内容，只读）---
import pdfplumber

with pdfplumber.open('测试.pdf') as pdf:   # 打开 PDF
    for page in pdf.pages:                # 遍历每页
        text = page.extract_text()        # 提取该页全部文字
        tables = page.extract_tables()    # 提取该页表格（返回 list[list[list]])
        words = page.extract_words()      # 提取文字带位置坐标
        chars = page.chars                # 每个字符的详细位置
```

## 本模块示例

| 脚本 | 演示 |
|---|---|
| [01_python_docx.py](01_python_docx.py) | 创建 Word 文档、加标题/段落/表格、设字体样式、保存后读取、批量替换关键词 |
| [02_python_pptx.py](02_python_pptx.py) | 创建 PPT、加幻灯片/文本框/表格、设字号、保存后遍历读取内容、Inches 坐标 |
| [03_PDF处理.py](03_PDF处理.py) | 用 reportlab 生成测试 PDF、pdfplumber 提取文字/表格/带位置文字、汇总所有页 |

运行方式：
```bash
uv run python lessons/06_办公自动化/01_python_docx.py
uv run python lessons/06_办公自动化/02_python_pptx.py
uv run python lessons/06_办公自动化/03_PDF处理.py
```

## 底层原理（简单了解）

1. **docx/pptx 本质是 XML + ZIP**：.docx 和 .pptx 文件其实是一个 zip 压缩包，里面装着一堆 XML 文件（document.xml、slide1.xml 等）和图片资源。python-docx/python-pptx 就是帮你读写这些 XML，不用手动解压。把 .docx 改名成 .zip 解压就能看到内部结构。
2. **pdfplumber 底层是 pdfminer.six**：PDF 格式本身不是"文字流"而是"绘图指令"（把字画在某个坐标），pdfminer.six 负责把这些指令解析成文字和坐标，pdfplumber 在上面加了表格识别、文字提取等友好 API。
3. **PDF 分两类：文本版和扫描版**。文本版 PDF 里真的有文字字符，pdfplumber 能直接抽；扫描版 PDF 本质是图片（扫描仪拍的），里面没有文字层，pdfplumber 抽出来是空的，得先用 OCR 库（pytesseract + tesseract 引擎）把图片识别成文字。
4. **PPT 的坐标用 EMU（English Metric Unit）**：1 英寸 = 914400 EMU，python-pptx 用 Inches() / Cm() / Pt() 帮你换算，不用自己算 EMU。Word 里字号用 Pt（磅），1 磅 = 1/72 英寸。