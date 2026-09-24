"""模块13 示例02：sqlite3 查询、更新、删除与进阶用法

演示 SELECT 查询（fetchall/fetchone/fetchmany）、WHERE 条件、
ORDER BY 排序、GROUP BY 聚合、UPDATE 更新、DELETE 删除、
with conn 上下文管理器、row_factory 按列名访问。

运行命令：
    uv run python lessons/13_数据库操作/02_sqlite3查询.py
"""

import sqlite3
from pathlib import Path


# 定位 sample 目录
SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)
DB_PATH = SAMPLE_DIR / "school.db"


# ============================================================
# 准备：建表并插入测试数据（若表不存在则重建）
# ============================================================
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 检查表是否存在，不存在则创建并填充数据
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='students'"
)
if cursor.fetchone() is None:
    cursor.execute("""
        CREATE TABLE students (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT    NOT NULL,
            age   INTEGER,
            score REAL
        )
    """)
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
    cursor.executemany(
        "INSERT INTO students (name, age, score) VALUES (?, ?, ?)",
        students_data,
    )
    conn.commit()
    print(f"  已初始化表 students，插入 {len(students_data)} 条数据\n")
else:
    print("  表 students 已存在，直接查询\n")


# ============================================================
# 第一部分：三种 fetch 方法
# ============================================================
print("=" * 55)
print("第一部分：fetchall / fetchone / fetchmany")
print("=" * 55)

# fetchall：取全部结果行，返回列表，每行是元组
cursor.execute("SELECT * FROM students")
all_rows = cursor.fetchall()
print(f"  fetchall 取全部: 共 {len(all_rows)} 行")
print(f"    前 2 行: {all_rows[:2]}")

# fetchone：取一行，再调取下一行，取完返回 None
cursor.execute("SELECT * FROM students")
first = cursor.fetchone()
second = cursor.fetchone()
print(f"\n  fetchone 第 1 次调用: {first}")
print(f"  fetchone 第 2 次调用: {second}")
print("  -> fetchone 适合结果集很大、想逐行处理不想一次全装进内存")

# fetchmany(n)：取 n 行
cursor.execute("SELECT * FROM students")
some = cursor.fetchmany(3)
print(f"\n  fetchmany(3): 共 {len(some)} 行")
print(f"    {some}")
print("  -> fetchmany(n) 一次取 n 行，介于 fetchall 和 fetchone 之间")


# ============================================================
# 第二部分：WHERE 条件查询
# ============================================================
print("\n" + "=" * 55)
print("第二部分：WHERE 条件查询")
print("=" * 55)

# 年龄 >= 19 且 分数 > 80
cursor.execute("SELECT name, age, score FROM students WHERE age >= ? AND score > ?", (19, 80))
rows = cursor.fetchall()
print("  条件: age >= 19 AND score > 80")
for name, age, score in rows:
    print(f"    {name}  年龄={age}  分数={score}")

# 模糊匹配 LIKE
cursor.execute("SELECT name FROM students WHERE name LIKE ?", ("张%",))
print("\n  条件: name LIKE '张%'  (姓张的)")
for (name,) in cursor.fetchall():
    print(f"    {name}")
print("  -> ? 占位符里也能放通配符，但通配符要写在参数里不是 SQL 里")


# ============================================================
# 第三部分：ORDER BY 排序
# ============================================================
print("\n" + "=" * 55)
print("第三部分：ORDER BY 排序")
print("=" * 55)

# 按分数降序
cursor.execute("SELECT name, score FROM students ORDER BY score DESC")
print("  ORDER BY score DESC (分数降序):")
for name, score in cursor.fetchall():
    print(f"    {name:6s}  {score}")

# 按年龄升序，年龄相同再按分数降序
cursor.execute("SELECT name, age, score FROM students ORDER BY age ASC, score DESC")
print("\n  ORDER BY age ASC, score DESC (年龄升序，同年龄分数降序):")
for name, age, score in cursor.fetchall():
    print(f"    {name:6s}  年龄={age}  分数={score}")


# ============================================================
# 第四部分：GROUP BY + 聚合函数
# ============================================================
print("\n" + "=" * 55)
print("第四部分：GROUP BY + 聚合函数")
print("=" * 55)

# 按年龄分组，统计每组的数量、平均分、最高分、总分
cursor.execute("""
    SELECT age,
           COUNT(*)   AS cnt,
           AVG(score) AS avg_score,
           MAX(score) AS max_score,
           SUM(score) AS sum_score
    FROM students
    GROUP BY age
    ORDER BY age
""")
print("  按年龄分组统计 (COUNT / AVG / MAX / SUM):")
print(f"    {'年龄':>4}  {'人数':>4}  {'平均分':>8}  {'最高分':>6}  {'总分':>6}")
for age, cnt, avg_s, max_s, sum_s in cursor.fetchall():
    print(f"    {age:>4}  {cnt:>4}  {avg_s:>8.2f}  {max_s:>6.1f}  {sum_s:>6.1f}")

# 全表聚合
cursor.execute("SELECT COUNT(*), AVG(score), MIN(score), MAX(score) FROM students")
cnt, avg_s, min_s, max_s = cursor.fetchone()
print(f"\n  全表统计: 共 {cnt} 人，平均 {avg_s:.2f}，最低 {min_s}，最高 {max_s}")


# ============================================================
# 第五部分：UPDATE 更新
# ============================================================
print("\n" + "=" * 55)
print("第五部分：UPDATE 更新数据")
print("=" * 55)

# 更新前先看孙八的分数
cursor.execute("SELECT score FROM students WHERE name = ?", ("孙八",))
before = cursor.fetchone()[0]
print(f"  更新前: 孙八 分数 = {before}")

# UPDATE 更新
cursor.execute("UPDATE students SET score = ? WHERE name = ?", (82.0, "孙八"))
conn.commit()

cursor.execute("SELECT score FROM students WHERE name = ?", ("孙八",))
after = cursor.fetchone()[0]
print(f"  更新后: 孙八 分数 = {after}")
print("  -> UPDATE ... SET 列=值 WHERE 条件，必须带 WHERE 否则更新全表")
print("  -> 更新后同样要 commit 才真正写入")


# ============================================================
# 第六部分：DELETE 删除
# ============================================================
print("\n" + "=" * 55)
print("第六部分：DELETE 删除数据")
print("=" * 55)

cursor.execute("SELECT COUNT(*) FROM students")
before_cnt = cursor.fetchone()[0]
print(f"  删除前: 共 {before_cnt} 条记录")

# 删除分数 < 70 的
cursor.execute("DELETE FROM students WHERE score < ?", (70,))
deleted = cursor.rowcount  # rowcount 取得上次操作影响的行数
conn.commit()

cursor.execute("SELECT COUNT(*) FROM students")
after_cnt = cursor.fetchone()[0]
print(f"  删除分数 < 70: 影响 {deleted} 行，删除后剩 {after_cnt} 条")
print("  -> DELETE FROM ... WHERE 条件，必须带 WHERE 否则清空全表")
print("  -> cursor.rowcount 取得 UPDATE/DELETE 影响的行数")


# ============================================================
# 第七部分：row_factory 按列名访问
# ============================================================
print("\n" + "=" * 55)
print("第七部分：row_factory = sqlite3.Row 按列名访问")
print("=" * 55)

# 默认情况下行是元组，只能用下标 row[0]、row[1] 访问
# 设 row_factory = sqlite3.Row 后，行对象支持按列名访问 row["name"]
conn.row_factory = sqlite3.Row
cursor2 = conn.cursor()  # 新游标继承 row_factory
cursor2.execute("SELECT * FROM students LIMIT 3")
print("  设 conn.row_factory = sqlite3.Row 后:")
for row in cursor2.fetchall():
    print(f"    row['id']={row['id']}  row['name']={row['name']}  row['score']={row['score']}")
print("  -> 默认行是元组只能 row[0]，设 Row 后可 row['列名']，代码可读性更好")
print("  -> row.keys() 返回列名列表，方便动态处理")


# ============================================================
# 第八部分：with conn 上下文管理器
# ============================================================
print("\n" + "=" * 55)
print("第八部分：with conn 上下文管理器")
print("=" * 55)

print("""
  with conn 上下文管理器管理事务：

      with conn:
          conn.execute("INSERT ...")
          conn.execute("UPDATE ...")
      # 退出 with 块时自动 commit；若块内抛异常则自动 rollback

  注意：with conn 管理的是事务提交/回滚，不是关闭连接。
  关闭连接仍需 conn.close()，或用 with sqlite3.connect(...) as conn
  （后者在退出时关闭连接，但不会自动 commit，需手动 commit）。

  推荐写法：
      conn = sqlite3.connect(DB_PATH)
      try:
          with conn:                 # 管理事务
              conn.execute("INSERT ...")
      finally:
          conn.close()              # 关闭连接
""")

# 演示 with conn 自动 commit
with conn:
    conn.execute("INSERT INTO students (name, age, score) VALUES (?, ?, ?)", ("测试员", 22, 77.0))
cursor2.execute("SELECT COUNT(*) FROM students")
print(f"  with conn 块内插入后查询: 共 {cursor2.fetchone()[0]} 条（已自动 commit）")


# ============================================================
# 完成
# ============================================================
cursor.close()
cursor2.close()
conn.close()
print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("""
要点:
1. fetchall 取全部、fetchone 取一行、fetchmany(n) 取 n 行
2. WHERE 条件查询，LIKE 做模糊匹配，通配符写在参数里
3. ORDER BY 列 ASC/DESC 排序，可多列组合排序
4. GROUP BY 分组，配合 COUNT/AVG/SUM/MAX/MIN 聚合函数
5. UPDATE ... SET ... WHERE 改数据，DELETE FROM ... WHERE 删数据，都必带 WHERE
6. cursor.rowcount 取 UPDATE/DELETE 影响的行数
7. conn.row_factory = sqlite3.Row 让行可按列名访问，比元组下标可读
8. with conn 自动 commit 或 rollback，但不管关闭连接，关闭仍需 close()
9. 所有改动都要 commit 才真正写入文件
""")