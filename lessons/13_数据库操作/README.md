# 模块 13：数据库操作

> 用 Python 操作数据库：标准库 sqlite3 直连 SQLite 文件数据库写原生 SQL，第三方 SQLAlchemy 用 ORM 把表映射成对象不用写 SQL。本模块每个脚本自动创建临时 .db 文件，不碰用户真实数据库，可独立安全运行。

## 核心库一览

| 库 | 导入名 | 来源 | 用途 | 是否需安装 |
| --- | --- | --- | --- | --- |
| sqlite3 | `import sqlite3` | 标准库 | 连接 SQLite、执行原生 SQL、事务管理 | 否（Python 自带） |
| SQLAlchemy | `from sqlalchemy import create_engine, Column, ...` | 第三方 | ORM 映射、屏蔽 SQL、跨数据库 | 是（`uv add sqlalchemy`） |

> 关键认知：sqlite3 是 Python 标准库，装 Python 就有；SQLAlchemy 是第三方，但本项目的 `pyproject.toml` 已声明依赖，`uv run` 会自动装好。SQLite 是文件数据库，无需启动服务端，整个库就是一个 `.db` 文件。

## sqlite3 vs sqlalchemy：什么时候用什么

| 维度 | sqlite3（原生 SQL） | SQLAlchemy（ORM） |
| --- | --- | --- |
| 写 SQL | 手写 `SELECT/INSERT/UPDATE/DELETE` | 不写 SQL，用类属性表达条件 |
| 返回形式 | 元组或 `sqlite3.Row`，`row[0]` 或 `row["name"]` | 模型对象，`s.name` 直接访问 |
| 学习成本 | 要懂 SQL | 要懂 ORM 概念（模型、会话、引擎） |
| IDE 补全 | 列名是字符串，无补全 | 类属性有补全，重构友好 |
| 性能 | 直接执行 SQL，最快 | 多一层抽象，有开销，复杂查询可能要退回原生 |
| 跨数据库 | 只连 SQLite | 换 MySQL/PostgreSQL 只改连接字符串 |
| 适用场景 | 简单脚本、教学、高性能批量、复杂报表 | 业务系统、CRUD 为主、想屏蔽 SQL |

> 结论：写一次性脚本、做数据分析、追求性能——用 sqlite3 写原生 SQL；做业务系统、模型多、想跨数据库——用 SQLAlchemy ORM。两者不互斥，SQLAlchemy 也能执行原生 SQL。

## 核心 API 速查

```python
# ===== sqlite3（标准库，原生 SQL）=====
import sqlite3

conn = sqlite3.connect("test.db")          # 连接文件数据库，不存在自动创建
conn = sqlite3.connect(":memory:")         # 纯内存数据库，退出即消失
conn.row_factory = sqlite3.Row             # 设后行可按列名访问 row["name"]

cur = conn.cursor()                        # 创建游标
cur.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("INSERT INTO t (name) VALUES (?)", ("张三",))   # ? 占位符防注入
cur.executemany("INSERT INTO t (name) VALUES (?)", [("a",), ("b",)])  # 批量插入
conn.commit()                              # 提交事务，不 commit 数据会丢

cur.execute("SELECT * FROM t WHERE id = ?", (1,))
row = cur.fetchone()                       # 取一行
rows = cur.fetchall()                      # 取全部
some = cur.fetchmany(10)                   # 取 10 行

cur.execute("UPDATE t SET name = ? WHERE id = ?", ("李四", 1))
cur.execute("DELETE FROM t WHERE id = ?", (1,))
print(cur.rowcount)                        # UPDATE/DELETE 影响的行数

with conn:                                 # 上下文管理事务，自动 commit/rollback
    conn.execute("INSERT INTO t (name) VALUES (?)", ("王五",))
conn.close()                               # 关闭连接

# ===== SQLAlchemy（ORM）=====
from sqlalchemy import Column, Integer, String, Float, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Student(Base):                       # 模型类 = 一张表
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    score = Column(Float)

engine = create_engine("sqlite:///test.db")   # 引擎，连接字符串
Base.metadata.create_all(engine)              # 根据模型自动建表
Session = sessionmaker(bind=engine)           # 会话工厂
session = Session()                           # 会话，所有操作通过它

# 增
session.add(Student(name="张三", score=88.5))
session.add_all([Student(name="李四"), Student(name="王五")])
session.commit()                              # commit 后自增主键自动填回

# 查
session.get(Student, 1)                       # 按主键查
session.query(Student).all()                  # 查全部
session.query(Student).filter(Student.score >= 85).all()   # 条件过滤
session.query(Student).order_by(Student.score.desc()).all()  # 排序
session.query(func.count(Student.id)).scalar()  # 聚合，scalar 取单值

# 改
s = session.query(Student).filter(Student.name == "张三").one()
s.score = 90.0
session.commit()

# 删
session.delete(s)
session.commit()
session.close()
```

## 本模块示例

| 脚本 | 演示 |
| --- | --- |
| [01_sqlite3基础.py](01_sqlite3基础.py) | `connect` 连接、`cursor` 游标、`CREATE TABLE` 建表、`INSERT` 插入、`commit` 事务、`?` 参数化防 SQL 注入、`lastrowid` |
| [02_sqlite3查询.py](02_sqlite3查询.py) | `fetchall/fetchone/fetchmany`、`WHERE`、`ORDER BY`、`GROUP BY` 聚合、`UPDATE`、`DELETE`、`row_factory` 按列名、`with conn` 事务 |
| [03_sqlalchemy_ORM.py](03_sqlalchemy_ORM.py) | `declarative_base` 定义模型、`create_engine` 连接、`session` 增删改查、`query/filter` 查询、与原生 SQL 对比 |

运行方式：

```bash
cd "C:\Users\wlh19\Desktop\python自动化"
uv run python lessons/13_数据库操作/01_sqlite3基础.py
uv run python lessons/13_数据库操作/02_sqlite3查询.py
uv run python lessons/13_数据库操作/03_sqlalchemy_ORM.py
```

> 三个脚本均自动在 `sample/` 子目录创建临时 `.db` 文件，不碰用户真实数据库，可独立运行。`01` 每次运行删除重建 `school.db`；`02` 复用 `01` 建的表，表不存在时自动初始化；`03` 单独用 `school_orm.db`。

## 底层原理

### 1. SQLite 是文件数据库，无需服务端

传统数据库（MySQL、PostgreSQL）是 C/S 架构：先启动一个数据库服务进程监听端口，客户端通过网络协议连接。SQLite 不一样——它是一个**嵌入式**数据库，整个引擎编译进一个库，数据库就是一个普通文件（`.db`）。`sqlite3.connect("test.db")` 直接读写这个文件，没有服务进程、没有网络、没有端口。

特点：

- **零配置**：装 Python 就有 sqlite3，拿来即用，适合教学、原型、小工具
- **单文件**：整个库就是一个 `.db` 文件，拷贝即备份
- **并发弱**：写操作锁整个文件，高并发写场景不适合，读多写少没问题
- **无服务端**：不需要 `mysqld` 这样的守护进程，脚本里 `connect` 就能用

Python 标准库的 `sqlite3` 模块其实是 SQLite C 引擎的薄封装，`import sqlite3` 时 Python 调用内置的 SQLite 动态库执行 SQL。

### 2. SQLAlchemy ORM：表映射成类、行映射成对象

ORM（Object-Relational Mapping，对象关系映射）的核心思想：

| 数据库概念 | Python 对象 |
| --- | --- |
| 表 | 类（继承 `Base`） |
| 列 | 类属性（`Column`） |
| 一行数据 | 类的一个实例 |
| 外键关联 | 属性访问（`s.department` 直接拿到关联对象） |

工作流程：

1. `declarative_base()` 创建模型基类
2. 定义模型类继承 `Base`，类属性用 `Column` 声明列
3. `create_engine(连接字符串)` 创建引擎（连接池的入口）
4. `Base.metadata.create_all(engine)` 根据模型类自动生成 `CREATE TABLE` 并执行
5. `sessionmaker(bind=engine)` 造会话工厂，`Session()` 造会话
6. 通过会话 `add/query/delete` 操作对象，`commit` 提交

ORM 把你写的 `Student.score >= 85` 翻译成 `WHERE score >= 85`，把 `order_by(Student.score.desc())` 翻译成 `ORDER BY score DESC`。你操作的是 Python 对象，ORM 在背后生成并执行 SQL。

代价：多一层抽象有性能开销，复杂查询（多表 JOIN、窗口函数、原生 SQL 优化）ORM 表达起来反而更绕，这时可用 `session.execute(text("原生SQL"))` 退回原生 SQL。

### 3. 连接池：create_engine 默认管理连接

`create_engine` 不是直接创建一个连接，而是创建一个**连接池**（默认 `QueuePool`）。每次 `Session()` 从池里借一个连接，`session.close()` 时连接不真关，而是还回池里复用。

为什么需要连接池：

- 建数据库连接很贵（TCP 握手、认证、分配会话），复用连接省时间
- 多线程并发时，池控制最大连接数，避免压垮数据库
- `sqlite3` 文件数据库连接很便宜，池的意义不大；但换成 MySQL/PostgreSQL 就很重要

连接字符串示例：

| 数据库 | 连接字符串 |
| --- | --- |
| SQLite 文件 | `sqlite:///test.db` |
| SQLite 内存 | `sqlite:///:memory:` |
| MySQL | `mysql+pymysql://user:pass@host:3306/dbname` |
| PostgreSQL | `postgresql+psycopg2://user:pass@host:5432/dbname` |

换数据库只改连接字符串，模型类和查询代码不用动——这是 ORM 跨数据库的核心价值。