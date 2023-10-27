import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


def send_email(sender_email, sender_password, receiver_email, subject, content):
    # SMTP服务器地址和端口号
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


if __name__ == '__main__':
    # 填写登录信息和邮件内容
    sender_email = 'canrad7@163.com'  # 发件人邮箱
    sender_password = 'ZWUXENDBVAWOHIZI'  # 发件人邮箱授权码
    receiver_email = ['1517807724@qq.com']  # 收件人邮箱
    subject = '测试邮件'  # 邮件主题
    content = '这是一封测试邮件。'  # 邮件内容
    send_email(sender_email, sender_password, receiver_email, subject, content)
