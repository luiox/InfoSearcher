#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import poplib
import re

class EmailUtil:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.email_dict = {}

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

    def get_content_by_subject(self, subject):
        if subject in self.email_dict:
            return self.email_dict[subject]
        else:
            return None

    def filter_subjects(self, keyword):
        if not self.email_dict:
            raise Exception('还未获取邮件主题')

        try:
            filtered_dict = {}
            for subject, content in self.email_dict.items():
                if keyword in subject:
                    filtered_dict[subject] = content
            return filtered_dict
        except re.error:
            raise Exception('正则表达式错误')


if __name__ == '__main__':
    # 授权码 ZWUXENDBVAWOHIZI
    e = EmailUtil('canrad7@163.com', 'ZWUXENDBVAWOHIZI')
    e.get_email_subjects()
    content = e.get_content_by_subject('test')
    print(content)
    filtered_dict = e.filter_subjects('账单')
    print(filtered_dict)
