import poplib
import email
from email.parser import Parser
from email.header import decode_header
import urllib.request


def parse_msg(message):  # 解析邮件内容
    type = message.get_content_type()
    maintype = message.get_content_maintype()
    subtype = message.get_content_subtype()
    if subtype == 'html':
        return None
    if maintype != 'multipart':
        print('type:', type)
        print('maintype:', maintype)
        print('subtype:', subtype)

        boundary = message.get_boundary()
        print('boundary:', boundary)

    # 如果get_filename()返回非None,表示有附件
    filename = message.get_filename()
    if filename:
        print('********')
        print('找到1个附件，文件名：', filename)
        print('********')
        data = message.get_payload(decode=True)
        with open(filename, 'wb') as pf:
            pf.write(data)
        return filename

    # 如果主类型为text，根据编码方式解析
    content_charset = message.get_content_charset()
    print('content_charset:', content_charset)
    if maintype == 'text':
        mail_content = message.get_payload(decode=True).strip()
        try:
            print('mail_content:\n', mail_content.decode(content_charset))
        except:
            print('解码邮件错误')

            # 如果主类型为multipart，递归
    elif maintype == 'multipart':
        for message_part in message.get_payload():
            parse_msg(message_part)
    return


# 登录邮箱
pop3_server = 'pop3.163.com'
yremail = 'canrad7@163.com'
password = 'ZWUXENDBVAWOHIZI'

# 连接到POP3服务器
server = poplib.POP3(pop3_server)
# 调试信息
server.set_debuglevel(1)
# 进行身份验证
server.user(yremail)
server.pass_(password)

# 获取邮件数量和占用空间
print('Messages: %s. Size: %s' % server.stat())

# 获取邮件列表
mail_list = resp, mails, octets = server.list()
print(mail_list)
print('------------------------------')

for index, mail in enumerate(mails):
    resp, lines, octets = server.retr(index + 1)
    msg_content = b'\r'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)
    parse_msg(msg)
    print('--------------------')

# 解析每封邮件并下载附件


print()
