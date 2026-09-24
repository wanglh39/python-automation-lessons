# 模块 2：Excel / CSV 数据处理

> 办公场景最常见的需求：读写表格、汇总统计、多表合并。Python 有三把刀——`csv` 标准库够用就别引第三方；`openpyxl` 处理 `.xlsx` 格式和样式；`pandas` 做数据分析最强大。

## 核心库一览

| 库 | 来源 | 用途 | 推荐度 |
|---|:---:|---|:---:|
| `csv` | 标准库 | 读写 `.csv` 纯文本表格，**零依赖首选** | ★★★★ |
| `openpyxl` | 第三方 | 读写 `.xlsx`，能保留格式/样式/公式 | ★★★★ |
| `pandas` | 第三方 | 数据分析全家桶：筛选/分组/汇总/合并 | ★★★★★ |

## 为什么选 pandas / 什么时候用 openpyxl

**简单读写用 csv 或 openpyxl**，轻量、可控、不引入大依赖：
- `.csv` 是纯文本，用标准库 `csv` 就行，连安装都不用
- `.xlsx` 要保留字体、列宽、公式 → 用 `openpyxl`，它能逐格操作
- 只是把表格读出来处理一下再写回 → `openpyxl` 足够

**数据分析用 pandas**，一行顶十行：
```python
# openpyxl 写法：循环遍历算总分
for row in ws.iter_rows(min_row=2):
    total = row[1].value + row[2].value + row[3].value
    row[4].value = total

# pandas 写法：向量化，一行搞定
df['总分'] = df['语文'] + df['数学'] + df['英语']
```

> **经验法则**：要筛选/分组/排序/统计/合并多表 → pandas；要逐格写样式/公式/合并单元格 → openpyxl；纯文本表格 → csv 标准库。

## 核心 API 速查

```python
# --- csv 标准库（不用安装）---
import csv
with open('a.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['姓名', '分数'])
    w.writerows([['张三', 90], ['李四', 80]])

with open('a.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)      # 按列名读，返回字典
    for row in reader:
        print(row['姓名'], row['分数'])
```

```python
# --- openpyxl（处理 .xlsx）---
from openpyxl import Workbook, load_workbook
wb = Workbook()                     # 新建工作簿
ws = wb.active                      # 活动工作表
ws['A1'] = '标题'                   # 单格写
ws.append(['张三', 90])             # 追加一行
wb.save('a.xlsx')                   # 保存

wb = load_workbook('a.xlsx')        # 读取
ws = wb.active
ws['A1'].value                      # 单格读
list(ws.iter_rows(values_only=True))  # 遍历所有行
```

```python
# --- pandas（数据分析）---
import pandas as pd
df = pd.read_csv('a.csv', encoding='utf-8')   # 读 CSV
df = pd.read_excel('a.xlsx')                  # 读 Excel（底层调 openpyxl）

df.head()                  # 看前 5 行
df.info()                  # 看列名/类型/非空数
df.describe()              # 数值列统计摘要
df['总分'] = df['语文'] + df['数学']   # 加计算列
df[df['总分'] > 200]       # 筛选
df.sort_values('总分', ascending=False)  # 排序
df.groupby('班级')['总分'].mean()       # 分组求均值

df.to_csv('out.csv', index=False, encoding='utf-8')  # 导出
```

## 本模块示例

| 脚本 | 演示 |
|---|---|
| [01_csv标准库.py](01_csv标准库.py) | csv.writer / reader / DictReader / DictWriter，零依赖读写 CSV |
| [02_openpyxl读写.py](02_openpyxl读写.py) | 创建/保存 .xlsx，逐格读写，批量 append，设置字体和列宽 |
| [03_pandas汇总.py](03_pandas汇总.py) | read_csv/read_excel，加计算列、筛选、排序、分组、导出 |

运行方式：
```bash
uv run python lessons/02_表格数据/01_csv标准库.py
uv run python lessons/02_表格数据/02_openpyxl读写.py
uv run python lessons/02_表格数据/03_pandas汇总.py
```

每个脚本会自动在 `sample/` 目录生成测试数据，不碰你真实文件，可反复运行。

## 底层原理（简单了解）

1. **CSV 本质是纯文本**：每行一条记录，逗号分隔字段。`csv` 模块只是帮你处理"字段里有逗号要加引号"这类边界情况，不解析格式。所以读 CSV 用 `open(encoding='utf-8')` 打开文本文件，再交给 `csv.reader`。
2. **xlsx 本质是 ZIP 压缩包**：一个 `.xlsx` 文件改后缀为 `.zip` 解压，里面是一堆 XML 文件。`openpyxl` 的工作就是把这些 XML 解析成 Python 对象，保存时再序列化回 XML 打包。所以读写大 Excel 会比较慢——XML 解析开销大。
3. **pandas 的 DataFrame 是列存储**：每一列是一个 NumPy 数组，所以 `df['语文'] + df['数学']` 是整个数组相加（向量化），比 Python for 循环快几十倍。这也是 pandas 适合大数据量的原因。
4. **pandas 读 Excel 底层调 openpyxl**：`pd.read_excel()` 默认用 openpyxl 解析 xlsx，转成 DataFrame。所以"读 Excel 做分析"用 pandas，"写 Excel 带格式"用 openpyxl，两者互补。