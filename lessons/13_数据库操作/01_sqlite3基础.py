"""模块13 示例01：sqlite3 标准库基础

演示用 Python 内置的 sqlite3 模块连接 SQLite 数据库、建表、插入数据、
参数化查询防 SQL 注入。sqlite3 是标准库，无需安装，SQLite 是文件数据库，
无需启动服务端，整个数据库就是一个 .db 文件。

运行命令：
    uv run python lessons/13_数据库操作/01_sqlite3基础.py
"""

import sqlite3
from pathlib import Path


# 定位 sample 目录，存放自动生成的 .db 文件
SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)
DB_PATH = SAMPLE_DIR / "school.db"

# 每次运行都从干净状态开始，避免重复插入导致主键冲突
if DB_PATH.exists():
    DB_PATH.unlink()


# ============================================================
# 第一部分：连接数据库与创建游标
# ============================================================
print("=" * 55)
print("第一部分：连接数据库与创建游标")
print("=" * 55)

# sqlite3.connect(path) 连接数据库文件
#   - 文件不存在时自动创建
#   - 传 ":memory:" 可创建纯内存数据库（程序退出即消失，适合临时测试）
conn = sqlite3.connect(DB_PATH)
print(f"  已连接: {DB_PATH.name}")
print(f"  连接对象类型: {type(conn).__name__}")

# conn.cursor() 创建游标，所有 SQL 都通过游标执行
cursor = conn.cursor()
print(f"  游标对象类型: {type(cursor).__name__}")
print("  -> 一个连接可有多个游标，游标记住上次查询的位置和结果")


# ============================================================
# 第二部分：建表 CREATE TABLE
# ============================================================
print("\n" + "=" * 55)
print("第二部分：建表 CREATE TABLE")
print("=" * 55)

# execute(sql) 执行一条 SQL
# 建学生表：id 主键自增、name 姓名、age 年龄、score 分数
cursor.execute("""
    CREATE TABLE students (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT    NOT NULL,
        age   INTEGER,
        score REAL
    )
""")
print("  已创建表 students")
print("  -> INTEGER PRIMARY KEY AUTOINCREMENT 让 id 自动递增")
print("  -> REAL 是浮点数类型，INTEGER 是整数，TEXT 是字符串")


# ============================================================
# 第三部分：插入数据 INSERT INTO
# ============================================================
print("\n" + "=" * 55)
print("第三部分：插入数据 INSERT INTO")
print("=" * 55)

# 单条插入：用 ? 占位符，参数以元组传入
students_data = [
    ("张三", 18, 88.5),
    ("李四", 19, 92.0),
    ("王五", 18, 76.5),
    ("赵六", 20, 85.0),
    ("钱七", 19, 91.5),
    ("孙八", 18, 65.0),
    ("周九", 20, 78.5),
    ("吴十", 19, 88.0),
]

# executemany 一次插入多行，比循环 execute 快得多
cursor.executemany(
    "INSERT INTO students (name, age, score) VALUES (?, ?, ?)",
    students_data,
)
print(f"  已插入 {len(students_data)} 条学生记录")

# conn.commit() 提交事务
#   - sqlite3 默认开启事务，execute 后数据只在内存，commit 才真正写入文件
#   - 不 commit 直接关闭连接，数据会丢失
conn.commit()
print("  已 commit 提交事务，数据真正写入文件")
print("  -> executemany 一次插多行，比循环 execute 快")
print("  -> 不 commit 就关闭连接，数据会丢失")


# ============================================================
# 第四部分：参数化查询防 SQL 注入
# ============================================================
print("\n" + "=" * 55)
print("第四部分：参数化查询防 SQL 注入")
print("=" * 55)

# 正确做法：用 ? 占位符，参数单独传，sqlite3 会安全转义
target_name = "张三"
cursor.execute("SELECT * FROM students WHERE name = ?", (target_name,))
row = cursor.fetchone()
print(f"  参数化查询 name={target_name!r}: {row}")

# 错误做法（仅演示，不执行）：字符串拼接
#   cursor.execute(f"SELECT * FROM students WHERE name = '{target_name}'")
# 如果 target_name 来自用户输入，比如输入 "x' OR '1'='1"
# 拼接后 SQL 变成：... WHERE name = 'x' OR '1'='1'
# 会返回全表数据，这就是 SQL 注入
print("""
  -> 错误写法（字符串拼接，有 SQL 注入风险）：
     cursor.execute(f"SELECT * FROM students WHERE name = '{user_input}'")
     若 user_input = "x' OR '1'='1"，SQL 变成：
       SELECT * FROM students WHERE name = 'x' OR '1'='1'
     会返回全表数据，这就是 SQL 注入

  -> 正确写法（参数化，? 占位符）：
     cursor.execute("SELECT * FROM students WHERE name = ?", (user_input,))
     sqlite3 会把参数当纯数据，不会当成 SQL 代码执行
""")


# ============================================================
# 第五部分：再次插入演示单条 execute + commit
# ============================================================
print("=" * 55)
print("第五部分：单条 execute 插入并查看自增 id")
print("=" * 55)

cursor.execute(
    "INSERT INTO students (name, age, score) VALUES (?, ?, ?)",
    ("郑十一", 21, 95.0),
)
conn.commit()
# cursor.lastrowid 取得上次插入的自增主键
print(f"  插入 '郑十一'，自增 id = {cursor.lastrowid}")
print("  -> lastrowid 在 INSERT 后立刻取，可拿到新行的主键值")


# ============================================================
# 完成
# ============================================================
# 关闭游标与连接，释放文件锁
cursor.close()
conn.close()
print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print(f"""
要点:
1. sqlite3.connect(path) 连接文件数据库，文件不存在会自动创建
2. conn.cursor() 创建游标，所有 SQL 通过 cursor.execute() 执行
3. CREATE TABLE 建表，INTEGER PRIMARY KEY AUTOINCREMENT 自增主键
4. INSERT INTO 插数据，executemany 一次插多行比循环 execute 快
5. conn.commit() 提交事务，不 commit 就关闭连接数据会丢失
6. 永远用 ? 占位符做参数化查询，不要字符串拼接，防 SQL 注入
7. cursor.lastrowid 取得刚插入行的自增主键
8. SQLite 是文件数据库无需服务端，整个库就是一个 .db 文件
""")