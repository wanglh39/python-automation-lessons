"""python-docx 操作 Word 文档

演示 python-docx：创建文档、加标题/段落/表格、设字体样式、保存后读取、批量替换关键词。

运行: uv run python lessons/06_办公自动化/01_python_docx.py
"""
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn


# 定位 sample 目录
SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)
DOC_PATH = SAMPLE_DIR / "报告.docx"


print("=" * 55)
print("1. 创建文档：加标题、段落、表格")
print("=" * 55)
doc = Document()
# 加标题（level 0 是 Title，1 是 Heading 1，依此类推）
doc.add_heading("2025 年度工作总结", level=0)
doc.add_heading("一、项目概述", level=1)
doc.add_paragraph("本年度共完成 3 个自动化项目，提升效率约 40%。")
doc.add_paragraph("其中办公自动化模块覆盖 Word、PPT、PDF 三类文档处理。")

# 加表格并填数据
doc.add_heading("二、项目数据", level=1)
table = doc.add_table(rows=4, cols=3, style="Light Grid Accent 1")
# 表头
table.cell(0, 0).text = "项目"
table.cell(0, 1).text = "耗时(天)"
table.cell(0, 2).text = "状态"
# 数据行
data = [
    ("文件批处理", "5", "已完成"),
    ("网络请求", "3", "已完成"),
    ("办公自动化", "7", "进行中"),
]
for i, row in enumerate(data, start=1):
    for j, val in enumerate(row):
        table.cell(i, j).text = val
print(f"  已创建文档，包含 {len(doc.paragraphs)} 个段落、{len(doc.tables)} 个表格")
print("  -> add_heading 加标题，add_paragraph 加段落，add_table 加表格")
print("  -> style='Light Grid Accent 1' 给表格加内置样式")

print("\n" + "=" * 55)
print("2. 设置字体样式：字号、加粗、颜色、中文字体")
print("=" * 55)
doc.add_heading("三、样式演示", level=1)
p = doc.add_paragraph()
# 一个段落里可以有多段 run，每段 run 可以有不同样式
run1 = p.add_run("普通文字 ")
run2 = p.add_run("加粗 14 号 ")
run2.bold = True
run2.font.size = Pt(14)
run3 = p.add_run("红色文字 ")
run3.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
run4 = p.add_run("大号蓝色")
run4.font.size = Pt(18)
run4.font.color.rgb = RGBColor(0x00, 0x00, 0xFF)
run4.bold = True
print("  段落里用 add_run 分段，每段 run 单独设 bold / font.size / font.color.rgb")
print("  -> python-docx 的最小样式单位是 run，一个段落可由多个 run 拼成")

# 中文字体要额外设置（python-docx 默认对中文可能不生效）
p_cn = doc.add_paragraph()
run_cn = p_cn.add_run("这是中文宋体演示")
run_cn.font.name = "SimSun"  # 设西文字体
run_cn._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")  # 设中文字体
print("  中文字体需额外设置 eastAsia 属性，否则可能不生效")

print("\n" + "=" * 55)
print("3. 保存文档")
print("=" * 55)
doc.save(DOC_PATH)
print(f"  已保存到: {DOC_PATH}")
print("  -> save() 覆盖写，路径用 Path 对象或字符串都行")

print("\n" + "=" * 55)
print("4. 读取文档：遍历段落和表格")
print("=" * 55)
doc2 = Document(DOC_PATH)
print(f"  读取到 {len(doc2.paragraphs)} 个段落、{len(doc2.tables)} 个表格")
print("\n  段落内容:")
for i, p in enumerate(doc2.paragraphs):
    if p.text.strip():
        style = p.style.name
        print(f"    [{style}] {p.text}")

print("\n  表格内容:")
for t_idx, t in enumerate(doc2.tables):
    print(f"    表格 {t_idx + 1}（{len(t.rows)} 行 x {len(t.columns)} 列）:")
    for row in t.rows:
        cells = [cell.text for cell in row.cells]
        print(f"      {cells}")
print("  -> paragraphs 是段落列表，tables 是表格列表，cell.text 取单元格文字")

print("\n" + "=" * 55)
print("5. 批量替换文档中的关键词")
print("=" * 55)
# 模板替换场景：把文档里的占位符换成实际值
replacements = {
    "2025": "2026",
    "自动化": "智能",
}
doc3 = Document(DOC_PATH)
replace_count = 0
for p in doc3.paragraphs:
    for run in p.runs:
        for old, new in replacements.items():
            if old in run.text:
                count = run.text.count(old)
                run.text = run.text.replace(old, new)
                replace_count += count
# 表格里也替换
for t in doc3.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    for old, new in replacements.items():
                        if old in run.text:
                            count = run.text.count(old)
                            run.text = run.text.replace(old, new)
                            replace_count += count
replaced_path = SAMPLE_DIR / "报告_替换后.docx"
doc3.save(replaced_path)
print(f"  替换规则: {replacements}")
print(f"  共替换 {replace_count} 处，保存到: {replaced_path.name}")
print("  -> 替换要遍历每个 run，因为文字可能被拆到多个 run 里")
print("  -> 段落和表格都要遍历，表格里每个单元格也是段落结构")

print("\n" + "=" * 55)
print("6. 注意：python-docx 只能处理 .docx，不能处理 .doc")
print("=" * 55)
print("  .docx 是 Office 2007+ 的 XML 压缩格式，python-docx 专门读写它")
print("  .doc 是老的二进制格式，python-docx 不支持，打开会报错")
print("  -> 遇到 .doc 先用 Word 另存为 .docx，再用 python-docx 处理")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. Document() 新建、Document(path) 读取，add_heading/add_paragraph/add_table 加内容")
print("  2. 样式最小单位是 run，一个段落可由多个 run 拼成，各自设字体/加粗/颜色")
print("  3. 读取用 doc.paragraphs 遍历段落、doc.tables 遍历表格，cell.text 取单元格")
print("  4. 替换文字要遍历每个 run 的 text，段落和表格都要处理；只支持 .docx 不支持 .doc")