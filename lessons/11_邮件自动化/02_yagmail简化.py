"""模块11 示例02：用 yagmail 简化发邮件

运行命令：
    uv run python lessons/11_邮件自动化/02_yagmail简化.py

说明：
    yagmail 是第三方库，封装 smtplib + email，三行代码发邮件。
    安装：uv add yagmail  或  pip install yagmail
    本脚本只演示 API 用法，不连接 SMTP 服务器、不真发邮件。
"""

# yagmail 是第三方库，导入失败时给出友好提示
try:
    import yagmail
    YAGMAIL_AVAILABLE = True
except ImportError:
    YAGMAIL_AVAILABLE = False


# ============================================================
# 第一部分：yagmail 基本用法
# ============================================================
print("=" * 55)
print("第一部分：yagmail 基本用法（仅说明，不真发）")
print("=" * 55)

print("""
yagmail 发一封邮件只需三步：

    import yagmail

    # 1. 初始化 SMTP 连接（账号 + 授权码 + 服务器）
    yag = yagmail.SMTP(
        user="你的邮箱@qq.com",
        password="你的授权码",
        host="smtp.qq.com"
    )

    # 2. 发送
    yag.send(
        to="收件人@example.com",
        subject="邮件主题",
        contents="邮件正文"
    )

    # 3. 自动关闭（也可用 with 语句）

对比 smtplib：同样的功能 smtplib 要 15~30 行，yagmail 只要 3 行。
""")


# ============================================================
# 第二部分：yagmail 进阶用法
# ============================================================
print("=" * 55)
print("第二部分：yagmail 进阶用法")
print("=" * 55)

print("""
1. 群发：to 传列表
    yag.send(to=["a@example.com", "b@example.com"],
             subject="群发", contents="大家好")

2. HTML 正文：contents 直接传 HTML 字符串
    yag.send(to="to@example.com", subject="HTML邮件",
             contents="<h1>你好</h1><p>这是 HTML 正文</p>")

3. 带附件：contents 传列表，路径自动作为附件
    yag.send(to="to@example.com", subject="带附件",
             contents=["正文内容", "report.pdf", "data.xlsx"])

4. 内嵌图片：正文用 html，图片路径放 contents
    yag.send(to="to@example.com", subject="带图片",
             contents=['<img src="logo.png">你好</img>', "logo.png"])

5. with 语句自动管理连接
    with yagmail.SMTP(user, password, host) as yag:
        yag.send(to=to, subject=subject, contents=contents)
""")


# ============================================================
# 第三部分：smtplib vs yagmail 代码对比
# ============================================================
print("=" * 55)
print("第三部分：smtplib vs yagmail 代码对比")
print("=" * 55)

print("""
任务：发一封纯文本邮件

--- smtplib 写法（约 15 行）---
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText("正文", "plain", "utf-8")
    msg["Subject"] = "主题"
    msg["From"] = "sender@qq.com"
    msg["To"] = "to@example.com"

    with smtplib.SMTP_SSL("smtp.qq.com", 465) as smtp:
        smtp.login("sender@qq.com", "授权码")
        smtp.sendmail("sender@qq.com",
                      ["to@example.com"],
                      msg.as_string())

--- yagmail 写法（3 行）---
    import yagmail
    yag = yagmail.SMTP("sender@qq.com", "授权码", "smtp.qq.com")
    yag.send("to@example.com", "主题", "正文")

yagmail 自动处理：编码、邮件头、MIME 构造、连接、登录、发送、关闭。
""")


# ============================================================
# 第四部分：yagmail 是否安装检测
# ============================================================
print("=" * 55)
print("第四部分：yagmail 安装状态检测")
print("=" * 55)

if YAGMAIL_AVAILABLE:
    print("\nyagmail 已安装，版本相关属性：")
    print("  模块路径：", yagmail.__file__)
    print("  可直接调用 yagmail.SMTP(...) 初始化连接")
else:
    print("\nyagmail 未安装。")
    print("安装命令：")
    print("    uv add yagmail")
    print("  或")
    print("    pip install yagmail")
    print("\n本脚本仅演示 API，未安装也能看懂用法。")


# ============================================================
# 第五部分：yagmail 源码层面做了什么
# ============================================================
print()
print("=" * 55)
print("第五部分：yagmail 背后做了什么")
print("=" * 55)

print("""
yagmail 本质上是对 smtplib + email 的封装：

1. SMTP(user, password, host)
   -> 内部创建 smtplib.SMTP_SSL(host)
   -> 调用 login(user, password)

2. send(to, subject, contents)
   -> 根据 contents 类型自动构造 MIMEText / MIMEMultipart
   -> 字符串当正文，路径当附件，HTML 自动识别
   -> 设置 Subject/From/To 头
   -> 调用 sendmail 发送

所以 yagmail 能做的事 smtplib + email 都能做，只是代码更长。
理解了 smtplib 原理，再用 yagmail 就是"语法糖"。
""")


# ============================================================
# 完成
# ============================================================
print("=" * 55)
print("完成!")
print("=" * 55)
print("""
要点:
1. yagmail.SMTP(user, password, host) 初始化连接
2. yag.send(to, subject, contents) 发送，contents 可字符串或列表
3. contents 列表中：字符串是正文，路径是附件，自动识别
4. with 语句可自动关闭连接
5. yagmail 是 smtplib + email 的封装，原理相同
6. 本脚本不真发邮件，只演示 API
""")