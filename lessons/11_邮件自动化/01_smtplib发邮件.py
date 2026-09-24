"""模块11 示例01：用 smtplib + email 标准库构造并发送邮件

运行命令：
    uv run python lessons/11_邮件自动化/01_smtplib发邮件.py

说明：
    本脚本只演示 API 用法，构造邮件对象并打印其文本内容。
    不连接 SMTP 服务器、不真发邮件。
    末尾用 print 说明"如果真发，代码是..."。
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr


# ============================================================
# 第一部分：构造纯文本邮件
# ============================================================
print("=" * 55)
print("第一部分：用 MIMEText 构造纯文本邮件")
print("=" * 55)

# MIMEText(正文, 类型, 编码)
#   类型: "plain" 纯文本 / "html" 网页
#   编码: 中文用 "utf-8"
msg_text = MIMEText("你好，这是一封来自 Python 的测试邮件。", "plain", "utf-8")

# 设置邮件头：Subject 主题、From 发件人、To 收件人
msg_text["Subject"] = "Python 邮件测试-纯文本"
msg_text["From"] = formataddr(("Python自动化", "sender@qq.com"))
msg_text["To"] = formataddr(("学习者", "receiver@example.com"))

print("\n邮件对象类型：", type(msg_text).__name__)
print("\n--- 邮件完整文本（as_string）---")
print(msg_text.as_string())
print("--- 结束 ---\n")


# ============================================================
# 第二部分：构造 HTML 邮件
# ============================================================
print("=" * 55)
print("第二部分：用 MIMEText 构造 HTML 邮件")
print("=" * 55)

html_content = """
<h2>Python 自动化报告</h2>
<p>本次运行结果：</p>
<ul>
    <li>成功项：98</li>
    <li>失败项：2</li>
</ul>
<p style="color:gray;">此邮件由 Python 程序自动发送</p>
"""
msg_html = MIMEText(html_content, "html", "utf-8")
msg_html["Subject"] = "Python 邮件测试-HTML"
msg_html["From"] = "sender@qq.com"
msg_html["To"] = "receiver@example.com"

print("\n--- HTML 邮件文本 ---")
print(msg_html.as_string())
print("--- 结束 ---\n")


# ============================================================
# 第三部分：用 MIMEMultipart 构造"正文+一段说明"的多部分邮件
# ============================================================
print("=" * 55)
print("第三部分：MIMEMultipart 多部分邮件")
print("=" * 55)

msg_multi = MIMEMultipart()
msg_multi["Subject"] = "Python 邮件测试-多部分"
msg_multi["From"] = "sender@qq.com"
msg_multi["To"] = "receiver@example.com"

# 第一部分：正文
body = MIMEText("这是正文部分。", "plain", "utf-8")
msg_multi.attach(body)

# 第二部分：附加一段 HTML（演示 attach 用法）
extra = MIMEText("<b>这是附加的 HTML 片段。</b>", "html", "utf-8")
msg_multi.attach(extra)

print("\n--- 多部分邮件文本 ---")
print(msg_multi.as_string())
print("--- 结束 ---\n")


# ============================================================
# 第四部分：smtplib 发送流程说明（不真连）
# ============================================================
print("=" * 55)
print("第四部分：smtplib 发送流程（仅说明，不真连）")
print("=" * 55)

print("""
要真发邮件，需要三步：

1. 连接 SMTP 服务器（以 QQ 邮箱为例）
2. 登录（账号 + 授权码，不是登录密码）
3. 调用 sendmail 发送

代码如下（本脚本不执行）：

    import smtplib

    smtp_server = "smtp.qq.com"
    smtp_port = 465          # SSL 端口
    sender = "你的邮箱@qq.com"
    password = "你的授权码"   # 不是 QQ 密码！
    receiver = "收件人@example.com"

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, [receiver], msg_text.as_string())

    print("邮件已发送")

注意：
- SMTP_SSL 用 465 端口（SSL 加密）
- SMTP + starttls() 用 587 端口
- sendmail 的收件人是列表，可群发
- with 语句会自动 quit()
""")


# ============================================================
# 第五部分：授权码获取方式
# ============================================================
print("=" * 55)
print("第五部分：授权码获取方式")
print("=" * 55)

print("""
QQ 邮箱：
    1. 登录 mail.qq.com
    2. 设置 -> 账号 -> POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务
    3. 开启 "POP3/SMTP 服务"
    4. 按提示发短信获取 16 位授权码

163 邮箱：
    1. 登录 mail.163.com
    2. 设置 -> POP3/SMTP/IMAP
    3. 开启 "SMTP 服务"
    4. 设置客户端授权密码

Gmail：
    1. 账号 -> 安全 -> 两步验证
    2. 应用专用密码 -> 生成

授权码是 16 位字符串，在代码里代替密码使用。
授权码可单独关闭，比直接用主密码安全。
""")


# ============================================================
# 完成
# ============================================================
print("=" * 55)
print("完成!")
print("=" * 55)
print("""
要点:
1. MIMEText(正文, "plain"/"html", "utf-8") 构造邮件正文
2. msg["Subject"]/["From"]/["To"] 设置邮件头
3. MIMEMultipart 是容器，用 attach() 拼接多个部分
4. msg.as_string() 把邮件对象序列化成可发送的文本
5. smtplib.SMTP_SSL(host, 465) 连服务器，login 用授权码
6. 本脚本只构造对象并打印，不真发邮件
""")