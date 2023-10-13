from imapclient import IMAPClient

username = 'canrad7@163.com'
pwd = 'ZWUXENDBVAWOHIZI'

# context manager ensures the session is cleaned up
with IMAPClient(host="imap.163.com") as client:
    client.login(username, pwd)
    client.select_folder('INBOX')

    # search criteria are passed in a straightforward way
    # (nesting is supported)
    messages = client.search(['NOT', 'DELETED'])

    # fetch selectors are passed as a simple list of strings.
    response = client.fetch(messages, ['FLAGS', 'RFC822.SIZE'])

    # `response` is keyed by message id and contains parsed,
    # converted response items.
    for message_id, data in response.items():
        print('{id}: {size} bytes, flags={flags}'.format(
            id=message_id,
            size=data[b'RFC822.SIZE'],
            flags=data[b'FLAGS']))
