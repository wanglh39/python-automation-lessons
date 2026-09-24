"""模块11 示例03：带附件与 HTML 的邮件

运行命令：
    uv run python lessons/11_邮件自动化/03_带附件与HTML.py

说明：
    演示用 email.mime 构造 HTML 正文、带附件、内嵌图片的邮件对象。
    构造完成后用 as_string() 打印邮件文本，不连接 SMTP、不真发。
    附件用内存中的字节构造，不读真实文件，确保可独立运行。
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders


# ============================================================
# 第一部分：HTML 正文邮件
# ============================================================
print("=" * 55)
print("第一部分：HTML 正文邮件")
print("=" * 55)

html_body = """
<div style="font-family:sans-serif;">
    <h2 style="color:#2c7;">每日报告</h2>
    <p>尊敬的用户：</p>
    <p>今日任务已全部完成，统计如下：</p>
    <table border="1" cellpadding="6" cellspacing="0">
        <tr><th>项目</th><th>数量</th></tr>
        <tr><td>成功</td><td>98</td></tr>
        <tr><td>失败</td><td>2</td></tr>
    </table>
    <p style="color:gray;font-size:12px;">本邮件由 Python 自动发送</p>
</div>
"""
msg_html = MIMEText(html_body, "html", "utf-8")
msg_html["Subject"] = "HTML 正文邮件示例"
msg_html["From"] = "sender@qq.com"
msg_html["To"] = "receiver@example.com"

print("\n--- HTML 邮件文本（前 400 字符）---")
print(msg_html.as_string()[:400])
print("... (省略)")
print("--- 结束 ---\n")


# ============================================================
# 第二部分：带附件的邮件
# ============================================================
print("=" * 55)
print("第二部分：带附件的邮件")
print("=" * 55)

# MIMEMultipart("mixed") 表示多部分混合（正文+附件）
msg_attach = MIMEMultipart("mixed")
msg_attach["Subject"] = "带附件的邮件示例"
msg_attach["From"] = "sender@qq.com"
msg_attach["To"] = "receiver@example.com"

# 1) 正文部分
text_part = MIMEText("详见附件中的报告。", "plain", "utf-8")
msg_attach.attach(text_part)

# 2) 附件部分：用内存字节构造，不读真实文件
#    实际场景：open("report.txt", "rb").read()
fake_report = "任务名称,状态\n爬取首页,成功\n解析数据,成功\n入库,失败\n".encode("utf-8")
part = MIMEBase("application", "octet-stream")
part.set_payload(fake_report)
encoders.encode_base64(part)  # 附件用 base64 编码传输
part.add_header(
    "Content-Disposition",
    "attachment",
    filename=("utf-8", "", "report.csv")  # 中文文件名用三元组
)
msg_attach.attach(part)

print("\n--- 带附件邮件文本（前 500 字符）---")
print(msg_attach.as_string()[:500])
print("... (省略 base64 附件内容)")
print("--- 结束 ---\n")


# ============================================================
# 第三部分：内嵌图片的邮件
# ============================================================
print("=" * 55)
print("第三部分：内嵌图片的邮件")
print("=" * 55)

# 内嵌图片结构：MIMEMultipart("related") 包住 (HTML正文 + 图片)
# HTML 里用 <img src="cid:图片ID"> 引用图片
msg_img = MIMEMultipart("related")
msg_img["Subject"] = "内嵌图片邮件示例"
msg_img["From"] = "sender@qq.com"
msg_img["To"] = "receiver@example.com"

# 1) HTML 正文，用 cid:logo 引用图片
html_with_img = """
<h2>欢迎</h2>
<p><img src="cid:logo" alt="logo"></p>
<p>图片内嵌在邮件中，无需外链。</p>
"""
img_text_part = MIMEText(html_with_img, "html", "utf-8")
msg_img.attach(img_text_part)

# 2) 构造一个极小的 PNG 图片（1x1 红点）作为内嵌图片
#    实际场景：MIMEImage(open("logo.png", "rb").read())
#    这里用固定字节构造，避免依赖外部文件
tiny_png = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000"
    "0108060000001f15c4890000000d49444154789c63f8cf"
    "0000000901010000001f0000000049454e44ae426082"
)
img_part = MIMEImage(tiny_png)
img_part.add_header("Content-ID", "<logo>")  # 对应 HTML 里的 cid:logo
img_part.add_header("Content-Disposition", "inline", filename="logo.png")
msg_img.attach(img_part)

print("\n--- 内嵌图片邮件文本（前 500 字符）---")
print(msg_img.as_string()[:500])
print("... (省略 base64 图片内容)")
print("--- 结束 ---\n")


# ============================================================
# 第四部分：完整邮件结构说明
# ============================================================
print("=" * 55)
print("第四部分：邮件 MIME 结构说明")
print("=" * 55)

print("""
常见邮件结构：

1. 纯文本邮件
   MIMEText("正文", "plain")

2. HTML 邮件
   MIMEText("<html>...", "html")

3. 正文 + 附件
   MIMEMultipart("mixed")
     ├── MIMEText(正文)
     └── MIMEBase(附件)

4. 纯文本 + HTML 双份（让客户端自选）
   MIMEMultipart("alternative")
     ├── MIMEText(纯文本)
     └── MIMEText(HTML)

5. HTML + 内嵌图片
   MIMEMultipart("related")
     ├── MIMEText(HTML, 引用 cid:xxx)
     └── MIMEImage(图片, Content-ID=xxx)

6. 最复杂：正文 + 附件 + 内嵌图片
   MIMEMultipart("mixed")
     ├── MIMEMultipart("alternative")
     │     ├── MIMEText(纯文本)
     │     └── MIMEMultipart("related")
     │           ├── MIMEText(HTML)
     │           └── MIMEImage(内嵌图片)
     └── MIMEBase(普通附件)
""")


# ============================================================
# 第五部分：yagmail 发附件更简单
# ============================================================
print("=" * 55)
print("第五部分：yagmail 发附件/HTML/图片更简单")
print("=" * 55)

print("""
同样的功能，yagmail 写法：

1. HTML 正文
    yag.send(to="to@example.com", subject="HTML邮件",
             contents="<h2>报告</h2><p>详情见附件</p>")

2. 带附件（contents 列表里放路径）
    yag.send(to="to@example.com", subject="带附件",
             contents=["正文内容", "report.csv", "data.xlsx"])

3. 内嵌图片（HTML 里引用文件名，路径放 contents）
    yag.send(to="to@example.com", subject="带图片",
             contents=['<h2>欢迎</h2><img src="logo.png">',
                       "logo.png"])

yagmail 自动判断：
    - 字符串 -> 正文
    - 以 .html 结尾或含 <tag> -> HTML
    - 路径存在 -> 附件
    - 图片路径在 HTML 中被引用 -> 内嵌

无需手动构造 MIMEMultipart / MIMEBase / Content-ID。
""")


# ============================================================
# 第六部分：发送说明（不真发）
# ============================================================
print("=" * 55)
print("第六部分：发送说明（不真发）")
print("=" * 55)

print("""
若要真发带附件的邮件，代码如下（本脚本不执行）：

    import smtplib

    with smtplib.SMTP_SSL("smtp.qq.com", 465) as smtp:
        smtp.login("sender@qq.com", "授权码")
        smtp.sendmail("sender@qq.com",
                      ["receiver@example.com"],
                      msg_attach.as_string())

yagmail 版本：

    import yagmail
    yag = yagmail.SMTP("sender@qq.com", "授权码", "smtp.qq.com")
    yag.send("receiver@example.com", "带附件",
             contents=["正文", "report.csv"])
""")


# ============================================================
# 完成
# ============================================================
print("=" * 55)
print("完成!")
print("=" * 55)
print("""
要点:
1. HTML 正文用 MIMEText(html, "html", "utf-8")
2. 带附件用 MIMEMultipart("mixed") + MIMEBase + encode_base64
3. 内嵌图片用 MIMEMultipart("related") + MIMEImage + Content-ID
4. HTML 里用 <img src="cid:图片ID"> 引用内嵌图片
5. 邮件结构可嵌套：mixed 包 alternative 包 related
6. yagmail 把这些全封装了，contents 列表搞定
7. 本脚本用内存字节构造附件和图片，不读真实文件，不真发
""")