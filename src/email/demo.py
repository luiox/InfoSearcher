import getpass
import imaplib

username = "canrad7@163.com"  # 邮箱账号
password = "ZWUXENDBVAWOHIZI"  # 邮箱密码
M = imaplib.IMAP4("imap.163.com")
M.login(username, password)
M.select()
typ, data = M.search(None, 'ALL')
for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    print('Message %s\n%s\n' % (num, data[0][1]))
M.close()
M.logout()

