import base64
import email
import poplib
import re
import os
from email import parser
from email.header import decode_header
from email.parser import Parser


def remove_invalid_chars(filename):
    # 定义需要去除的非法字符正则表达式模式
    pattern = r'[\/:*?"<>|]'

    # 使用 re.sub 函数替换非法字符为空字符串
    cleaned_filename = re.sub(pattern, '', filename)

    return cleaned_filename


def write_file_with_directory(path, content, way='w'):
    # 检查路径中的目录是否存在，如果不存在则创建
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 打开文件并写入内容
    with open(path, way) as file:
        file.write(content)


def parse_msg(subject, message):  # 解析邮件内容
    content_type = message.get_content_type()
    maintype = message.get_content_maintype()
    subtype = message.get_content_subtype()
    if subtype == 'html':
        return None
    if maintype != 'multipart':
        print('type:', content_type)
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
        filename = "download/" + filename
        write_file_with_directory(filename, data, 'wb')
        return filename

    # 如果主类型为text，根据编码方式解析
    content_charset = message.get_content_charset()
    print('content_charset:', content_charset)
    if maintype == 'text':
        mail_content = message.get_payload(decode=True).strip()
        try:
            content_str = mail_content.decode(content_charset)
            print('mail_content:\n', content_str)
            # print("subject:", subject)

            filename = remove_invalid_chars(f"{subject}.txt")
            full_filename = "email_context/" + filename
            write_file_with_directory(full_filename, content_str)

        except:
            print('解码邮件错误')

            # 如果主类型为multipart，递归
    elif maintype == 'multipart':
        for message_part in message.get_payload():
            parse_msg(subject, message_part)
    return


class EmailUtil:
    def __init__(self, username, password):
        self.pop_server = None
        self.username = username
        self.password = password
        self.email_dict = {}
        self.boundary_dict = {}
        self.raw_email_dict = {}

    def login(self):
        try:
            self.pop_server = poplib.POP3('pop.163.com')
            self.pop_server.user(self.username)
            self.pop_server.pass_(self.password)
            print('登录成功')
            return self.pop_server
        except poplib.error_proto as e:
            print('登录失败:', e)
            raise Exception('登录失败')

    def do(self):
        mail_list = resp, mails, octets = self.pop_server.list()
        print(mail_list)
        print('------------------------------')

        for index, mail in enumerate(mails):
            resp, lines, octets = self.pop_server.retr(index + 1)
            msg_content = b'\r'.join(lines).decode('utf-8')
            msg = Parser().parsestr(msg_content)
            # 获取主题
            subject = msg.get("Subject")
            if subject:
                # 解码主题
                decoded_subject = decode_header(subject)[0][0]
                if isinstance(decoded_subject, bytes):
                    decoded_subject = decoded_subject.decode("utf-8")
                print("主题:", decoded_subject)
                # 正则匹配是不是账单
                words = ["银行", "账单"]
                pattern = r"(?:" + "|".join(words) + r")"
                match = re.search(pattern, decoded_subject)
                if match:
                    print("是账单!")
                    parse_msg(decoded_subject, msg)
            print('--------------------')


if __name__ == '__main__':
    # 授权码 ZWUXENDBVAWOHIZI
    e = EmailUtil('canrad7@163.com', 'ZWUXENDBVAWOHIZI')
    e.login()
    e.do()
