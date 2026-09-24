"""PDF 处理：用 reportlab 生成 + pdfplumber 提取

演示 pdfplumber 提取 PDF 文字/表格/带位置文字。先用 reportlab 生成一个测试 PDF，
再用 pdfplumber 读取它。pdfplumber 只能读不能写，写 PDF 用 reportlab。

运行: uv run python lessons/06_办公自动化/03_PDF处理.py
"""
from pathlib import Path

import pdfplumber
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体（reportlab 默认 Helvetica 不支持中文）
pdfmetrics.registerFont(TTFont("SimHei", "C:/Windows/Fonts/simhei.ttf"))


# 定位 sample 目录
SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)
PDF_PATH = SAMPLE_DIR / "测试.pdf"


print("=" * 55)
print("1. 先用 reportlab 生成一个测试 PDF")
print("=" * 55)
# reportlab 是"画图式"生成 PDF：在 canvas 上指定坐标画文字、线条
c = canvas.Canvas(str(PDF_PATH), pagesize=A4)
width, height = A4
print(f"  A4 页面尺寸: {width:.0f} x {height:.0f} 点（1 点 = 1/72 英寸）")

# 画标题（坐标原点在左下角，y 轴向上）。中文必须用中文字体
c.setFont("SimHei", 18)
c.drawString(2 * cm, height - 2 * cm, "PDF 提取测试报告")
# 画正文
c.setFont("SimHei", 12)
c.drawString(2 * cm, height - 3 * cm, "这是第一段文字，用于测试 pdfplumber 提取。")
c.drawString(2 * cm, height - 3.8 * cm, "这是第二段文字，包含数字 123 和字母 ABC。")
c.drawString(2 * cm, height - 4.6 * cm, "第三段：测试中文提取是否正常。")

# 画一个简单表格（用线条和文字拼）
c.drawString(2 * cm, height - 6 * cm, "表格示例:")
table_top = height - 6.8 * cm
row_h = 0.8 * cm
col_x = [2 * cm, 6 * cm, 10 * cm]
rows = [
    ["项目", "耗时", "状态"],
    ["批处理", "5 天", "完成"],
    ["PDF 处理", "3 天", "完成"],
]
# 画表格线（先画线，再画文字，避免重叠）
for i in range(len(rows) + 1):
    y = table_top - i * row_h
    c.line(2 * cm, y, 14 * cm, y)
for x in col_x + [14 * cm]:
    c.line(x, table_top, x, table_top - len(rows) * row_h)
# 填表格文字：文字基线放在行中间偏下，不和线重叠
for i, row in enumerate(rows):
    y = table_top - i * row_h - 0.55 * row_h
    for j, val in enumerate(row):
        c.drawString(col_x[j] + 0.1 * cm, y, val)

c.showPage()  # 结束当前页
# 加第二页
c.setFont("SimHei", 12)
c.drawString(2 * cm, height - 2 * cm, "这是第二页，测试多页 PDF 提取。")
c.drawString(2 * cm, height - 3 * cm, "第二页的内容也应该被 pdfplumber 读到。")
c.showPage()
c.save()
print(f"  已生成测试 PDF: {PDF_PATH}")
print("  -> reportlab 是画图式生成：在 canvas 上 drawString 画文字、line 画线")
print("  -> 坐标原点在左下角，y 轴向上（和 pdfplumber 提取的坐标一致）")

print("\n" + "=" * 55)
print("2. 用 pdfplumber 打开 PDF")
print("=" * 55)
with pdfplumber.open(PDF_PATH) as pdf:
    print(f"  打开成功，共 {len(pdf.pages)} 页")
    print(f"  第 1 页尺寸: {pdf.pages[0].width:.0f} x {pdf.pages[0].height:.0f} 点")
    print("  -> pdfplumber.open() 返回上下文管理器，with 自动关闭")

print("\n" + "=" * 55)
print("3. 提取每页文字：page.extract_text()")
print("=" * 55)
with pdfplumber.open(PDF_PATH) as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text()
        print(f"\n  --- 第 {i} 页文字 ---")
        print(text)
    print("\n  -> extract_text() 返回该页全部文字拼成的字符串")
    print("  -> 按阅读顺序排列，换行保留，适合整页文字提取")

print("\n" + "=" * 55)
print("4. 提取表格：page.extract_tables()")
print("=" * 55)
with pdfplumber.open(PDF_PATH) as pdf:
    page = pdf.pages[0]
    tables = page.extract_tables()
    print(f"  第 1 页检测到 {len(tables)} 个表格")
    for t_idx, table in enumerate(tables, start=1):
        print(f"\n  表格 {t_idx}（{len(table)} 行）:")
        for row in table:
            print(f"    {row}")
    print("\n  -> extract_tables() 返回 list[list[list]]，三层嵌套：表 -> 行 -> 单元格")
    print("  -> 靠线条检测表格边界，没有线的表格可用 table_settings 调")

print("\n" + "=" * 55)
print("5. 提取文字带位置：page.extract_words() / page.chars")
print("=" * 55)
with pdfplumber.open(PDF_PATH) as pdf:
    page = pdf.pages[0]
    words = page.extract_words()
    print(f"  第 1 页共 {len(words)} 个词")
    print(f"  前 5 个词（带坐标）:")
    for w in words[:5]:
        print(f"    文字='{w['text']}'  x0={w['x0']:.1f}  y0={w['top']:.1f}  x1={w['x1']:.1f}  y1={w['bottom']:.1f}")
    print(f"\n  第 1 页共 {len(page.chars)} 个字符")
    print(f"  前 3 个字符（带详细属性）:")
    for ch in page.chars[:3]:
        print(f"    字符='{ch['text']}'  x0={ch['x0']:.1f}  y0={ch['top']:.1f}  字体={ch.get('fontname', '?')}  字号={ch.get('size', '?'):.1f}")
    print("\n  -> extract_words() 按词返回，带 x0/y0/x1/y1 坐标")
    print("  -> page.chars 按字符返回，还带字体名、字号等详细属性")
    print("  -> 适合需要按位置筛选文字的场景（如只抽某区域的文字）")

print("\n" + "=" * 55)
print("6. 汇总所有页文字")
print("=" * 55)
all_text = []
with pdfplumber.open(PDF_PATH) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            all_text.append(text)
full = "\n".join(all_text)
print(f"  共 {len(all_text)} 页有文字，合计 {len(full)} 个字符")
print(f"  前 50 字: {full[:50]}...")
print("  -> 实战常把每页文字拼起来做全文搜索或关键词定位")

print("\n" + "=" * 55)
print("7. pdfplumber 的边界与互补")
print("=" * 55)
print("  pdfplumber 只能读 PDF，不能创建/修改 PDF（创建用 reportlab）")
print("  文本版 PDF（有文字层）能直接抽，扫描版 PDF（是图片）抽出来是空的")
print("  扫描版要先 OCR（如 pytesseract + tesseract 引擎）识别成文字")
print("  -> pdfplumber 适合：从 PDF 报表抽数据进 Excel、提取合同条款、全文搜索")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. pdfplumber.open() 打开 PDF，page.extract_text() 提取文字、extract_tables() 提取表格")
print("  2. page.chars / extract_words() 带坐标，适合按位置筛选文字")
print("  3. pdfplumber 只能读不能写，创建 PDF 用 reportlab（画图式 API）")
print("  4. 扫描版 PDF 没有文字层，pdfplumber 抽不出来，要先 OCR 识别")