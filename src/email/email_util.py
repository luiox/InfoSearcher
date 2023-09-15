#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import poplib


class EmailUtil:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        try:
            pop_server = poplib.POP3_SSL('pop.163.com')
            pop_server.user(self.username)
            pop_server.pass_(self.password)
            print('登录成功')
            return pop_server
        except poplib.error_proto as e:
            print('登录失败:', e)
            return None

    def get_email_subjects(self):
        pop_server = self.login()
        if not pop_server:
            return

        try:
            num_messages = len(pop_server.list()[1])
            for i in range(num_messages):
                msg_lines = pop_server.top(i + 1, 0)[1]
                subject = ''
                for line in msg_lines:
                    if line.startswith(b'Subject:'):
                        subject = line.decode('utf-8')
                        break
                print(f"邮件{i + 1}的主题：{subject}")
        except poplib.error_proto as e:
            print('获取邮件主题失败:', e)

        pop_server.quit()


if __name__ == '__main__':
    # 授权码 ZWUXENDBVAWOHIZI
    e = EmailUtil('canrad7@163.com', 'ZWUXENDBVAWOHIZI')
    e.login()
    e.get_email_subjects()
