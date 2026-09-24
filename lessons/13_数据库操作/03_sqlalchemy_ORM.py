"""模块13 示例03：SQLAlchemy ORM 基础

演示用 SQLAlchemy ORM 操作数据库：定义模型类、create_engine 连接、
session 增删改查、query + filter 查询。ORM 把表映射成类、行映射成对象，
不用写 SQL，但多一层抽象。后端用 SQLite，无需服务端。

运行命令：
    uv run python lessons/13_数据库操作/03_sqlalchemy_ORM.py
"""

from pathlib import Path

from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# 定位 sample 目录
SAMPLE_DIR = Path(__file__).parent / "sample"
SAMPLE_DIR.mkdir(exist_ok=True)
DB_PATH = SAMPLE_DIR / "school_orm.db"

# 每次运行都从干净状态开始
if DB_PATH.exists():
    DB_PATH.unlink()


# ============================================================
# 第一部分：定义模型类（ORM 核心）
# ============================================================
print("=" * 55)
print("第一部分：定义模型类（继承 Base）")
print("=" * 55)

# declarative_base() 返回所有模型类的共同基类
# 继承它的类会被 SQLAlchemy 识别为一张表
Base = declarative_base()


class Student(Base):
    # __tablename__ 指定表名
    __tablename__ = "students"

    # Column(类型, 主键/约束) 定义列
    id = Column(Integer, primary_key=True)        # 主键，自动自增
    name = Column(String(20), nullable=False)     # 姓名，非空
    age = Column(Integer)                         # 年龄
    score = Column(Float)                         # 分数

    # __repr__ 让打印对象时显示有用信息，调试方便
    def __repr__(self):
        return f"Student(id={self.id}, name={self.name!r}, age={self.age}, score={self.score})"


print(f"  模型类: {Student.__name__}")
print(f"  表名:   {Student.__tablename__}")
print(f"  列:     {[c.name for c in Student.__table__.columns]}")
print("  -> 类属性 = 表的列，类实例 = 表的一行")
print("  -> declarative_base() 是所有模型的基类，继承它才被识别为表")


# ============================================================
# 第二部分：create_engine 连接数据库
# ============================================================
print("\n" + "=" * 55)
print("第二部分：create_engine 连接数据库")
print("=" * 55)

# create_engine(连接字符串) 创建引擎
#   sqlite:///路径  是 SQLite 连接字符串，三个斜线后跟文件路径
#   echo=True 会打印执行的 SQL，调试用；生产关掉
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
print(f"  已创建引擎: {engine.url}")
print("  -> 连接字符串格式: sqlite:///路径  (三个斜线 + 文件路径)")
print("  -> echo=True 可打印执行的 SQL，调试时打开，生产关掉")

# Base.metadata.create_all(engine) 根据所有模型类自动建表
Base.metadata.create_all(engine)
print("  已根据模型类自动建表 students")

# sessionmaker 工厂创建会话类，会话是 ORM 操作的入口
Session = sessionmaker(bind=engine)
print("  已创建 Session 工厂 (sessionmaker(bind=engine))")


# ============================================================
# 第三部分：session 增删改查
# ============================================================
print("\n" + "=" * 55)
print("第三部分：用 session 增删改查")
print("=" * 55)

# 创建一个 session 实例，所有 ORM 操作通过它进行
session = Session()

# --- 新增：构造对象 + session.add + commit ---
students_obj = [
    Student(name="张三", age=18, score=88.5),
    Student(name="李四", age=19, score=92.0),
    Student(name="王五", age=18, score=76.5),
    Student(name="赵六", age=20, score=85.0),
    Student(name="钱七", age=19, score=91.5),
    Student(name="孙八", age=18, score=65.0),
]
session.add_all(students_obj)
session.commit()
print(f"  新增: add_all {len(students_obj)} 个对象后 commit")
for s in students_obj:
    print(f"    {s}  # commit 后 id 自动填回")
print("  -> 构造对象 = 在内存造一行，add 加入会话，commit 才真正写入")
print("  -> commit 后自增主键 id 会自动填回对象")


# ============================================================
# 第四部分：query 查询
# ============================================================
print("\n" + "=" * 55)
print("第四部分：query() 查询")
print("=" * 55)

# 查全部：session.query(模型类).all()
all_students = session.query(Student).all()
print(f"  query(Student).all(): 共 {len(all_students)} 个对象")
for s in all_students:
    print(f"    {s}")

# 按主键查一个：session.get(模型类, 主键)
one = session.get(Student, 1)
print(f"\n  session.get(Student, 1): {one}")
print("  -> get() 按主键查，最直接；query().all() 查全部")

# filter 过滤：相当于 WHERE
high = session.query(Student).filter(Student.score >= 85).all()
print(f"\n  filter(Student.score >= 85): 共 {len(high)} 个")
for s in high:
    print(f"    {s}")

# 多条件过滤：filter().filter() 链式，相当于 AND
result = session.query(Student).filter(Student.age >= 19).filter(Student.score > 85).all()
print(f"\n  filter(age >= 19).filter(score > 85): 共 {len(result)} 个")
for s in result:
    print(f"    {s}")
print("  -> Student.score 是类属性，filter 里用它代表列，ORM 翻译成 SQL")


# ============================================================
# 第五部分：排序、聚合、更新、删除
# ============================================================
print("\n" + "=" * 55)
print("第五部分：排序、聚合、更新、删除")
print("=" * 55)

# order_by 排序
ordered = session.query(Student).order_by(Student.score.desc()).all()
print("  order_by(Student.score.desc()) 分数降序:")
for s in ordered:
    print(f"    {s.name:6s}  {s.score}")

# 聚合：func.count / func.avg
from sqlalchemy import func

cnt = session.query(func.count(Student.id)).scalar()
avg_score = session.query(func.avg(Student.score)).scalar()
print(f"\n  func.count: 共 {cnt} 人")
print(f"  func.avg:   平均分 {avg_score:.2f}")
print("  -> .scalar() 取单值（聚合查询常用），.all() 取列表")

# 更新：查出对象，改属性，commit
target = session.query(Student).filter(Student.name == "孙八").one()
print(f"\n  更新前: {target}")
target.score = 82.0
session.commit()
print(f"  更新后: {target}")
print("  -> ORM 更新就是改对象属性再 commit，不用写 UPDATE SQL")

# 删除：查出对象，session.delete，commit
to_delete = session.query(Student).filter(Student.score < 70).all()
for s in to_delete:
    session.delete(s)
session.commit()
print(f"\n  删除 score < 70: 删了 {len(to_delete)} 个")
remaining = session.query(Student).count()
print(f"  剩余 {remaining} 条")
print("  -> ORM 删除就是 session.delete(对象) 再 commit")


# ============================================================
# 第六部分：ORM vs 原生 SQL 对比
# ============================================================
print("\n" + "=" * 55)
print("第六部分：ORM vs 原生 SQL 对比")
print("=" * 55)

print("""
  同一个"查年龄>=19且分数>85的学生"：

  原生 SQL (sqlite3):
      cursor.execute(
          "SELECT * FROM students WHERE age >= ? AND score > ?",
          (19, 85)
      )
      rows = cursor.fetchall()

  ORM (SQLAlchemy):
      students = session.query(Student)\\
          .filter(Student.age >= 19)\\
          .filter(Student.score > 85)\\
          .all()

  对比:
  - ORM 不写 SQL，用类属性表达条件，IDE 能自动补全列名
  - ORM 返回的是对象，访问 s.name 而非 row[1]，可读性好
  - ORM 多一层抽象，有性能开销，复杂查询可能要退回原生 SQL
  - ORM 屏蔽数据库差异，换 MySQL/PostgreSQL 只改连接字符串
  - 简单 CRUD 用 ORM 省心，复杂报表/高性能批量操作用原生 SQL
""")


# ============================================================
# 完成
# ============================================================
session.close()
print("=" * 55)
print("完成!")
print("=" * 55)
print(f"""
要点:
1. declarative_base() 创建模型基类，继承它定义表，类属性 = 列
2. create_engine('sqlite:///路径') 连接，Base.metadata.create_all 自动建表
3. sessionmaker(bind=engine) 造会话工厂，Session() 造会话，所有操作通过会话
4. 新增: 构造对象 + add/add_all + commit，commit 后自增主键自动填回
5. 查询: query(模型).all() 全部、get(模型, 主键) 单个、filter(条件) 过滤
6. 排序 order_by、聚合 func.count/avg + scalar()、更新改属性、delete 删对象
7. ORM 不写 SQL 用类属性表达条件，可读性好但多一层抽象有性能开销
8. 简单 CRUD 用 ORM 省心，复杂报表/高性能批量用原生 SQL
9. 屏蔽数据库差异，换 MySQL/PostgreSQL 只改 create_engine 连接字符串
""")