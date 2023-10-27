import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


class Sender:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def send_email(sender_email, sender_password, receiver_email, subject, content):
    # SMTP服务器地址和端口号，一般来说只需要改服务器地址，这个是发送人邮箱的服务器地址。
    smtp_server = 'smtp.163.com'
    smtp_port = 25

    # 发件人和收件人
    sender = sender_email
    receiver = receiver_email

    # 构造邮件内容
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ";".join(receiver)
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText(content, 'plain', 'utf-8'))
    try:
        # 登录SMTP服务器
        smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
        smtp_obj.login(sender, sender_password)

        # 发送邮件
        smtp_obj.sendmail(sender, receiver, message.as_string())

        smtp_obj.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("邮件发送失败:", str(e))


sender_list = [
    Sender('@163.com', ''),
    Sender('@163.com', '')
]

if __name__ == '__main__':
    receiver_email = ['@qq.com']  # 收件人邮箱
    subject = '测试邮件'  # 邮件主题
    content = '这是一封测试邮件。'  # 邮件内容
    for sender in sender_list:
        send_email(sender.username, sender.password, receiver_email, subject, content)
