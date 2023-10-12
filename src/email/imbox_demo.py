import email
import imaplib
import os
from imbox import Imbox  # pip install imbox
import traceback


# enable less secure apps on your google account
# https://myaccount.google.com/lesssecureapps

class MailBox:
    SMTP_SERVER = 'imap.163.com'
    SMTP_PORT = 993
    USER = 'canrad7@163.com'
    PASSWORD = 'ZWUXENDBVAWOHIZI'

    def __init__(self):
        self.imap = imaplib.IMAP4_SSL(host=self.SMTP_SERVER, port=self.SMTP_PORT)
        self.imap.login(self.USER, self.PASSWORD)

    def __enter__(self):
        self.emails = self._get_all_messages()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.imap.close()
        self.imap.logout()

    def fetch_message(self, num=-1):
        _, data = self.imap.fetch(self.emails[num], '(RFC822)')
        _, bytes_data = data[0]
        email_message = email.message_from_bytes(bytes_data)
        return email_message

    def get_attachment(self, num=-1):
        for part in self.fetch_message(num).walk():
            if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                continue
            if part.get_filename():
                return part.get_payload(decode=True).decode('utf-8').strip()

    def _get_all_messages(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        return data[0].split()


host = "imap.163.com"
username = "canrad7@163.com"
password = 'ZWUXENDBVAWOHIZI'
download_folder = "/path/to/download/folder"

if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)

mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)
messages = mail.messages()  # defaults to inbox

for (uid, message) in messages:
    mail.mark_seen(uid)  # optional, mark message as read

    for idx, attachment in enumerate(message.attachments):
        try:
            att_fn = attachment.get('filename')
            download_path = f"{download_folder}/{att_fn}"
            print(download_path)
            with open(download_path, "wb") as fp:
                fp.write(attachment.get('content').read())

        except:
            print(traceback.print_exc())

mail.logout()

"""
Available Message filters: 

# Gets all messages from the inbox
messages = mail.messages()

# Unread messages
messages = mail.messages(unread=True)

# Flagged messages
messages = mail.messages(flagged=True)

# Un-flagged messages
messages = mail.messages(unflagged=True)

# Messages sent FROM
messages = mail.messages(sent_from='sender@example.org')

# Messages sent TO
messages = mail.messages(sent_to='receiver@example.org')

# Messages received before specific date
messages = mail.messages(date__lt=datetime.date(2018, 7, 31))

# Messages received after specific date
messages = mail.messages(date__gt=datetime.date(2018, 7, 30))

# Messages received on a specific date
messages = mail.messages(date__on=datetime.date(2018, 7, 30))

# Messages whose subjects contain a string
messages = mail.messages(subject='Christmas')

# Messages from a specific folder
messages = mail.messages(folder='Social')
"""
