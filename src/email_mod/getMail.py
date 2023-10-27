# coding=utf8

"""
python 2.7
"""

import re
import os
import sys
import time
import json
import email
import logging

from imapclient import IMAPClient

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] [%(filename)s] [%(lineno)d] - %(message)s',
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class NeteaseMail(object):

    def __init__(self):
        self.host = None
        self.username = None
        self.password = None
        self.server = None

    def client(self):
        try:
            self.server = IMAPClient(self.host)
            return 1
        except BaseException as e:
            logging.error('--- client error: %s' % e)
            return 0

    def login(self):
        try:
            resp = self.server.login(self.username, self.password)
            logging.info('--- login success: %s' % resp)
            return 1
        except BaseException as e:
            logging.error('--- login error: %s' % e)
            return 0

    def get_email_message(self, uid):
        # 获取邮件主体内容
        msgdict = self.server.fetch(uid, ['BODY[]'])
        mailbody = msgdict[uid][b'BODY[]']
        message = email.message_from_string(mailbody)

        return message

    def get_email_content(self, message):
        # 获取邮件的所有文本内容
        contents = []
        maintype = message.get_content_maintype()

        msgs = message.get_payload()
        if maintype == 'multipart':
            for msg in msgs:
                msg_type = msg.get_content_maintype()
                if msg_type == 'text':
                    msg_con_type = msg.get('Content-Type')
                    # 并不是所有的文本信息都在text/plain中，所以这里取text/html
                    if msg_con_type and 'text/html' in msg_con_type:
                        con1 = msg.get_payload(decode=True).strip()
                        contents.append(con1)
                elif msg_type == 'multipart':
                    for item in msg.get_payload():
                        item_tyep = item.get_content_maintype()
                        if item_tyep == 'text':
                            item_con_type = item.get('Content-Type')
                            if item_con_type and 'text/html' in item_con_type:
                                con2 = item.get_payload(decode=True).strip()
                                contents.append(con2)
                        else:
                            logging.error('wrong main type: %s' % item_tyep)
                else:
                    logging.error('--- get maintype error1')
        elif maintype == 'text':
            m_type = message.get('Content-Type')
            if m_type and 'text/html' in m_type:
                con3 = message.get_payload(decode=True).strip()
                contents.append(con3)
        else:
            logging.error('--- get maintype error2')

        # try:
        #     mail_content = mail_content.decode('utf8')
        # except:
        #     mail_content = mail_content.decode('gbk')

        conts = '\n'.join(contents)

        return conts

    def get_emails(self, search_condition):
        # 获取所有符合search_condition的邮件id，按时间升序排列
        self.server.select_folder('INBOX', readonly=True)  # readonly=True表明只读并不修改任何信息
        results = self.server.search(search_condition)

        return results

    def quit(self):
        try:
            self.server.logout()
        except Exception as e:
            logging.error('--- quit error: %s' % e)
            sys.exit(1)


def test():
    user = NeteaseMail()
    user.host = "imap.163.com"
    user.username = "canrad7@163.com"  # 邮箱账号
    user.password = "ZWUXENDBVAWOHIZI"  # 邮箱密码

    client_status = user.client()
    if not client_status:
        user.quit()
        return
    login_status = user.login()
    if not login_status:
        user.quit()
        return

    # 筛选条件
    search_condition = ['SINCE', '05-Dec-2018']
    emails = user.get_emails(search_condition)
    print('emails: ', emails)

    message = user.get_email_message(1543874740)
    print('message: ', message)
    # 得到的message对象可以使用类似于字典的方法进行访问
    print('eamil from: ', message['from'])

    contents = user.get_email_content(message)
    print('contents: ', contents)

    user.quit()


if __name__ == '__main__':
    test()
