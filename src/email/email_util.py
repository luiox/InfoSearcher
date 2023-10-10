#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import email
import poplib
import re
from email import parser
from email.header import decode_header

# 对邮件字符串根据不同编码来解码
def email_string_decode(str):
    decode_str = ''
    for part, charset in decode_header(subject):
        if charset:
            decode_str += part.decode(charset)
        else:
            decode_str += part
    return decode_str


# 通过邮件的message对象找到转发邮件的原始邮件，返回message对象
def find_original_email(message):
    original_email = None

    # 遍历邮件的所有部分
    for part in message.walk():
        # 判断是否为文本类型的部分
        if part.get_content_type() == 'text/plain':
            # 获取文本内容
            content = part.get_payload(decode=True).decode('utf-8')
            print(content)
            # 在文本内容中查找原始邮件的引用符号
            index = content.find('-----Original Message-----')
            if index != -1:
                # 截取引用符号之前的部分作为原始邮件内容
                original_content = content[:index].strip()
                print(original_content)
                # 创建原始邮件的message对象
                original_message = email.message_from_string(original_content)

                # 设置原始邮件
                original_email = original_message
                break

    return original_email


# 传入一个message对象，判断是否是转发的邮件
def is_forwarded_email(message):
    subject = message.get('Subject', '')
    decoded_subject = email_string_decode(subject)
    # print("subject:" + decoded_subject)
    body = ''

    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                body += part.get_payload(decode=True).decode('utf-8')
    else:
        body = message.get_payload(decode=True).decode('utf-8')

    # 判断标题和正文中是否包含转发关键词
    keywords = ['Fw:', 'FW:', 'Fwd:', '转发：']
    for keyword in keywords:
        if keyword in decoded_subject or keyword in body:
            return True

    return False


class EmailUtil:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.email_dict = {}
        self.boundary_dict = {}
        self.raw_email_dict = {}

    def login(self):
        try:
            pop_server = poplib.POP3_SSL('pop.163.com')
            pop_server.user(self.username)
            pop_server.pass_(self.password)
            print('登录成功')
            return pop_server
        except poplib.error_proto as e:
            print('登录失败:', e)
            raise Exception('登录失败')

    # 获取所有邮件的原始数据
    def get_raw_emails(self):
        pop_server = self.login()
        if not pop_server:
            return

        try:
            num_messages = len(pop_server.list()[1])
            for i in range(num_messages):
                msg_lines = pop_server.top(i + 1, 0)[1]
                raw_email = b'\r\n'.join(msg_lines).decode('utf-8')
                msg = email.message_from_string(raw_email)
                for line in msg_lines:
                    if line.startswith(b'Subject:'):
                        subject = line.decode('utf-8')
                        subject = base64.b64decode(subject.replace('Subject: =?UTF-8?B?', '')).decode('utf-8')
                        self.raw_email_dict[subject] = raw_email  # 将邮件主题和原始内容存入字典
            for subject, message in self.raw_email_dict.items():
                print(subject)
                print(message)
        except poplib.error_proto as e:
            print('获取邮件失败:', e)

        pop_server.quit()

    def get_email_subjects(self):
        pop_server = self.login()
        if not pop_server:
            return

        try:
            num_messages = len(pop_server.list()[1])
            for i in range(num_messages):
                msg_lines = pop_server.top(i + 1, 0)[1]
                subject = ''
                content = ''
                for line in msg_lines:
                    if line.startswith(b'Subject:'):
                        subject = line.decode('utf-8')
                        subject = base64.b64decode(subject.replace('Subject: =?UTF-8?B?', '')).decode('utf-8')
                    elif line.strip() != b'':  # 这里假设非空行即为内容
                        content += line.decode('utf-8')
                self.email_dict[subject] = content
                print(f"邮件{i + 1}的主题：{subject}")

        except poplib.error_proto as e:
            print('获取邮件主题失败:', e)

        pop_server.quit()

    def get_email_message_object(self):
        pop_server = self.login()
        if not pop_server:
            return

        try:
            num_messages = len(pop_server.list()[1])
            for i in range(num_messages):
                msg_lines = pop_server.top(i + 1, 0)[1]
                msg_content = b'\r\n'.join(msg_lines).decode('utf-8')
                msg = email.message_from_string(msg_content)
                for line in msg_lines:
                    if line.startswith(b'Subject:'):
                        subject = line.decode('utf-8')
                        subject = base64.b64decode(subject.replace('Subject: =?UTF-8?B?', '')).decode('utf-8')
                # subject = msg.get('Subject')
                content = ''
                boundary = None  # 初始化边界变量
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        content += part.get_payload(decode=True).decode('utf-8')
                    elif part.get_content_type().startswith('multipart/'):
                        # 获取边界标识符
                        boundary = part.get_boundary()

                self.email_dict[subject] = msg
                self.boundary_dict[boundary] = content  # 将边界标识符和内容存入字典
                print(f"邮件{i + 1}的主题：{subject}")
                print(f"邮件{i + 1}的边界标识符：{content}")

        except poplib.error_proto as e:
            print('获取邮件主题失败:', e)

        pop_server.quit()

    def get_content_by_subject(self, subject):
        if subject in self.email_dict:
            return self.email_dict[subject]
        else:
            return None

    def filter_message_by_subjects(self, keyword):
        if not self.email_dict:
            raise Exception('还未获取邮件主题')

        try:
            filtered_dict = {}
            for subject, message in self.email_dict.items():
                if keyword in subject:
                    filtered_dict[subject] = message
            return filtered_dict
        except re.error:
            raise Exception('正则表达式错误')


if __name__ == '__main__':
    # 授权码 ZWUXENDBVAWOHIZI
    e = EmailUtil('canrad7@163.com', 'ZWUXENDBVAWOHIZI')
    e.get_raw_emails()
    e.get_email_message_object()
    filtered_dict = e.filter_message_by_subjects('账单')
    # 遍历获取的字典
    for subject, message in filtered_dict.items():
        print("主题:", subject)
        # print("内容:", message.email_dict[subject])
        if is_forwarded_email(message):
            print("转发")
            original_message = find_original_email(message)
            print("找到原邮件")
            original_content = ''

            print(original_content)
        else:
            print("不是转发")
