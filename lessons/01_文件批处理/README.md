# 模块 1：文件 / 目录批处理

> 最常见的自动化需求：批量改文件名、按类型整理、清理空目录。Python 标准库就能搞定，不用装任何第三方库。

## 核心库一览

| 库 | 来源 | 用途 | 推荐度 |
|---|:---:|---|:---:|
| `pathlib` | 标准库 (3.4+) | 面向对象的路径操作，**现代写法首选** | ★★★★★ |
| `os` / `os.path` | 标准库 | 老牌路径操作，大量旧代码在用 | ★★★ |
| `shutil` | 标准库 | 文件移动/复制/删除目录树 | ★★★★ |
| `glob` | 标准库 | 通配符匹配文件名 | ★★★ |

## 为什么推荐 pathlib 而不是 os.path？

**os.path 是函数式**，字符串传来传去：
```python
import os
dir = os.path.dirname(path)
name = os.path.basename(path)
new = os.path.join(dir, "new.txt")
```

**pathlib 是面向对象**，Path 对象自带方法，链式调用更清晰：
```python
from pathlib import Path
p = Path(path)
new = p.parent / "new.txt"      # 用 / 拼接，跨平台
```

> **原理**：`pathlib.Path` 内部只存一个字符串（`_raw_paths`），所有操作都是对这个字符串的计算。`/` 运算符被重载为 `__truediv__`，内部调用 `os.path.join`。所以 pathlib 本质是 os.path 的面向对象封装，功能没多什么，但**可读性和安全性更好**（不会拼错分隔符）。

## pathlib 核心 API 速查

```python
from pathlib import Path

p = Path("sample") / "报告.docx"

# --- 取属性（不访问磁盘）---
p.name       # '报告.docx'   完整文件名
p.stem       # '报告'        去扩展名
p.suffix     # '.docx'       扩展名
p.parent     # Path('sample') 父目录
p.parts      # ('sample', '报告.docx') 拆成元组

# --- 判断（访问磁盘）---
p.exists()   # 是否存在
p.is_file()  # 是否文件
p.is_dir()   # 是否目录

# --- 遍历 ---
Path("sample").iterdir()       # 列出直接子项
Path("sample").glob("*.txt")   # 通配符匹配（仅当前层）
Path("sample").rglob("*.txt")  # 递归匹配所有子目录

# --- 读写小文件（不用 open）---
p.read_text(encoding="utf-8")
p.write_text("内容", encoding="utf-8")
p.read_bytes()                 # 读二进制

# --- 增删改 ---
p.mkdir(parents=True, exist_ok=True)  # 建目录
p.rename(p.with_name("新名.txt"))     # 重命名
p.unlink()                            # 删文件
p.rmdir()                             # 删空目录

# --- 路径变换 ---
p.resolve()           # 转绝对路径
p.relative_to(parent) # 算相对路径
p.with_suffix(".pdf") # 换扩展名
p.with_name("新名")   # 换文件名
```

## shutil 补充（pathlib 没有的操作）

```python
import shutil
shutil.copy(src, dst)            # 复制文件
shutil.copy2(src, dst)           # 复制 + 保留元数据(时间等)
shutil.copytree(src, dst)        # 复制整个目录树
shutil.rmtree(path)              # 删除目录树(含内容)
shutil.move(src, dst)            # 移动(跨磁盘也能用)
shutil.disk_usage(path)          # 查磁盘容量
```

## 本模块示例

| 脚本 | 演示 |
|---|---|
| [01_pathlib基础.py](01_pathlib基础.py) | Path 对象的创建、取属性、遍历、读写 |
| [02_批量重命名.py](02_批量重命名.py) | 给目录下所有文件加日期前缀 |
| [03_按类型整理.py](03_按类型整理.py) | 按扩展名把文件归类到子文件夹 |

运行方式：
```bash
uv run python lessons/01_文件批处理/01_pathlib基础.py
uv run python lessons/01_文件批处理/02_批量重命名.py
uv run python lessons/01_文件批处理/03_按类型整理.py
```

每个脚本会自动在 `sample/` 目录生成测试文件，不碰你真实文件，可反复运行。

## 底层原理（简单了解）

1. **Path 对象不访问磁盘**：`p.name`、`p.suffix` 这些只是字符串切分，不读硬盘。只有 `exists()`、`is_file()` 才真正访问文件系统。
2. **glob 的通配符**：`*` 匹配任意字符，`?` 匹配单个字符，`[abc]` 匹配字符集。底层用 `fnmatch` 模块实现。
3. **rglob 递归**：等价于 `glob("**/*.txt")`，`**` 表示任意层目录。底层用 `os.scandir()` 递归遍历，比 `os.listdir` 快（不构造完整列表）。
4. **跨平台分隔符**：Windows 用 `\`，macOS/Linux 用 `/`。`pathlib` 内部用 `os.sep`，所以用 `/` 运算符拼接的代码在所有平台都能跑。