import smtplib
from email.mime.text import MIMEText
from email.header import Header
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

# 邮件服务器地址和端口号
smtp_server = 'smtp.163.com'
smtp_port = 25

# 发件人邮箱地址和密码
sender_email = 'canrad7@163.com'  # 这里替换为您自己的发件人邮箱地址
sender_password = 'HAAFDDDDFDAABAF'  # 这里是你的授权码？ 非邮箱登录密码

# 收件人邮箱地址
recipient_email = '1111111@qq.com'

# 创建一封邮件，文本内容为 "Hello, World!"
message = MIMEText('This is test! Hello, World!', 'plain', 'utf-8')
message['From'] = Header('发件人昵称 <{}>'.format(sender_email), 'utf-8')  # 设置发件人昵称
message['To'] = Header('收件人昵称 <{}>'.format(recipient_email), 'utf-8')  # 设置收件人昵称
message['Subject'] = Header('邮件主题', 'utf-8')  # 设置邮件主题

try:
    # 连接邮件服务器并登录
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.login(sender_email, sender_password)

    # 发送邮件
    smtp_connection.sendmail(sender_email, recipient_email, message.as_string())

    # 关闭连接
    smtp_connection.quit()

    print("邮件发送成功！")

except Exception as e:
    print("邮件发送失败：", e)

# |邮箱 |SMTP服务器 |SSL协议端口 |非SSL协议端口|
#
# |:——:|:——:|:——:|:——:|
#
# |163 |smtp.163.com |465或者994| 25|
#
# |qq |smtp.qq.com |465或587 |25|

def send_email(from_addr, to_addr, subject, password):

    msg = MIMEText("邮件正文",'html','utf-8')

    msg['From'] = u'<%s>' % from_addr

    msg['To'] = u'<%s>' % to_addr

    msg['Subject'] = subject

    smtp = smtplib.SMTP_SSL('smtp.163.com', 465)

    smtp.set_debuglevel(1)

    smtp.ehlo("smtp.163.com")

    smtp.login(from_addr, password)

    smtp.sendmail(from_addr, [to_addr], msg.as_string())

if __name__ == "__main__":

    # 这里的密码是开启smtp服务时输入的客户端登录授权码，并不是邮箱密码

    # 现在很多邮箱都需要先开启smtp才能这样发送邮件

    send_email(u"from_addr",u"to_addr",u"主题",u"password")
