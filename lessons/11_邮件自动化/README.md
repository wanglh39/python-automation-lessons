# 模块 11：邮件自动化

> 用 Python 程序化地构造、发送邮件：纯文本、HTML、附件、内嵌图片一次讲清。本模块只演示 API 用法与邮件对象构造，不真连 SMTP 服务器、不真发邮件，确保可独立安全运行。

## 核心库一览

| 库 | 类型 | 作用 | 是否需安装 |
| --- | --- | --- | --- |
| `smtplib` | 标准库 | 连接 SMTP 服务器、发送邮件 | 否（Python 自带） |
| `email` | 标准库 | 构造邮件对象（正文、附件、HTML、图片） | 否（Python 自带） |
| `yagmail` | 第三方 | 封装 smtplib + email，三行代码发邮件 | 是（`uv add yagmail` 或 `pip install yagmail`） |

> 关键认知：`smtplib` 只管"把邮件对象送到服务器"，邮件长什么样由 `email` 库决定。两者分工明确。

## smtplib vs yagmail

| 维度 | smtplib + email | yagmail |
| --- | --- | --- |
| 代码行数（发一封纯文本） | 约 15~30 行 | 3 行 |
| 构造邮件对象 | 手动 `MIMEText` / `MIMEMultipart` | 自动，传字符串即可 |
| 添加附件 | `MIMEBase` + `add_header` + 读文件 | `contents=[正文, "附件路径"]` |
| HTML 正文 | `MIMEText(html, "html")` | `contents=["<h1>hi</h1>"]` 自动识别 |
| 内嵌图片 | `MIMEMultipart("related")` + CID | `contents=[正文, "图片路径"]` |
| 登录 | `smtp.login(user, 授权码)` | 构造函数里直接传 |
| 学习成本 | 高（要懂 MIME 结构） | 低（几乎零配置） |
| 适用场景 | 需要精细控制、批量定制、教学 | 日常自动化、脚本通知 |

> 结论：生产脚本用 yagmail 省心；要理解原理、做定制化（如自定义邮件头、DKIM 签名）用 smtplib + email。

## 核心 API 速查

```python
# ===== smtplib + email（标准库）=====
import smtplib
from email.mime.text import MIMEText            # 纯文本/HTML 正文
from email.mime.multipart import MIMEMultipart  # 多部分（正文+附件）
from email.mime.base import MIMEBase            # 任意二进制附件
from email.utils import formataddr             # 格式化 "昵称 <addr>"

# 构造纯文本邮件
msg = MIMEText("正文内容", "plain", "utf-8")
msg["Subject"] = "主题"
msg["From"] = "me@example.com"
msg["To"] = "you@example.com"

# 构造 HTML 邮件
msg = MIMEText("<h1>你好</h1>", "html", "utf-8")

# 带附件：用 MIMEMultipart 包一层
msg = MIMEMultipart()
msg.attach(MIMEText("正文", "plain", "utf-8"))
part = MIMEBase("application", "octet-stream")
part.set_payload(文件字节)
part.add_header("Content-Disposition", "attachment", filename="x.txt")
msg.attach(part)

# 发送（需真实 SMTP 服务器，本模块不执行）
with smtplib.SMTP_SSL("smtp.qq.com", 465) as s:
    s.login("user@qq.com", "授权码")
    s.sendmail(from_addr, [to_addr], msg.as_string())

# ===== yagmail（第三方）=====
import yagmail
yag = yagmail.SMTP(user="user@qq.com", password="授权码", host="smtp.qq.com")
yag.send(to="to@example.com", subject="主题", contents="正文")
# 带附件：contents 列表里放路径即可
yag.send(to="to@example.com", subject="主题",
         contents=["正文", "report.pdf", "logo.png"])
```

## 本模块示例

| 文件 | 主题 | 关键点 |
| --- | --- | --- |
| `01_smtplib发邮件.py` | 用标准库构造并发送邮件 | `MIMEText`、`as_string()`、SMTP 连接流程、授权码说明 |
| `02_yagmail简化.py` | 用 yagmail 三行发邮件 | `yagmail.SMTP`、`send`、与 smtplib 对比 |
| `03_带附件与HTML.py` | HTML 正文、附件、内嵌图片 | `MIMEMultipart`、`MIMEBase`、CID 内嵌图片、yagmail 附件 |

运行方式：

```bash
cd "C:\Users\wlh19\Desktop\python自动化"
uv run python lessons/11_邮件自动化/01_smtplib发邮件.py
uv run python lessons/11_邮件自动化/02_yagmail简化.py
uv run python lessons/11_邮件自动化/03_带附件与HTML.py
```

> 三个脚本均不连接 SMTP 服务器、不真发邮件，只构造邮件对象并打印其文本内容，安全可独立运行。

## 底层原理

### 1. SMTP 协议

SMTP（Simple Mail Transfer Protocol）是"发邮件"的协议，默认端口 25；加密版本 SMTP-SSL 用 465；STARTTLS 升级用 587。Python `smtplib.SMTP(host, port)` 建立连接后，流程是：

```
连接服务器 -> EHLO 握手 -> (STARTTLS) -> LOGIN(账号, 授权码) -> sendmail -> quit
```

收邮件用另一套协议（IMAP/POP3），不在本模块范围。

### 2. email.mime 构造多部分邮件

一封邮件本质上是一段符合 RFC 2822 的文本。`email.mime` 提供分层对象：

- `MIMEText`：一段文本正文（`plain` 或 `html`）
- `MIMEMultipart`：容器，把多个子部分拼成一封邮件（`mixed` 带附件 / `alternative` 纯文本+HTML 双份 / `related` 内嵌图片）
- `MIMEBase`：任意二进制数据，附件用 `application/octet-stream`
- `MIMEImage`：图片，可内嵌正文（用 `Content-ID` 引用）

`msg.as_string()` 把对象序列化成可发送的完整邮件文本，`smtplib.sendmail` 就是把这段文本送到服务器。

### 3. 授权码不是密码

QQ 邮箱、163 邮箱等出于安全，禁止用登录密码直接 SMTP 发信。需要在邮箱网页端"设置 → 账号 → SMTP 服务"开启服务并生成"授权码"（一个 16 位字符串），代码里 `smtp.login(账号, 授权码)` 用它代替密码。授权码可独立关闭、按设备生成，泄露风险远小于主密码。

常见 SMTP 服务器：

| 邮箱 | host | 端口（SSL） |
| --- | --- | --- |
| QQ | smtp.qq.com | 465 |
| 163 | smtp.163.com | 465 |
| Gmail | smtp.gmail.com | 465 |
| Outlook | smtp.office365.com | 587（STARTTLS） |