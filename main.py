import imaplib
from bs4 import BeautifulSoup


class Gmail:

    def __init__(self, username: str, password: str, imap: str = 'imap.gmail.com',
                 port: int = 993, timeout: int = 5, look_pretty: bool = True):
        self.username = username
        self.password = password
        self.imap = imap
        self.port = port
        self.timeout = timeout
        self.look_pretty = look_pretty
        self.connection = imaplib.IMAP4_SSL(self.imap, self.port)
        self.login()

    def login(self):
        self.connection.login(self.username, self.password)

    def get_body(self, data):
        result = []
        for messages in data[::-1]:
            for message in messages:
                if type(message) is tuple:
                    if self.look_pretty:
                        result.append(BeautifulSoup(message[1], 'lxml').getText()
                                      .replace('=E2=80=A2', '-').replace('=E2=80=99', '\''))
                    else:
                        result.append(message[1])
        return result

    def set_label(self, label: str):
        return self.connection.select(label)

    def get_messages(self, search: str = '(UNSEEN)'):
        _, result = self.connection.search(None, search)
        data = []
        for num in result[0].split():
            _, msg = self.connection.fetch(num, '(RFC822)')
            data.append(msg)
        return self.get_body(data)


def main():
    # Must generate app key OR enable less secure apps in your google settings.
    username, password = 'username', 'password'
    gmail = Gmail(username, password)
    gmail.set_label('Inbox')
    for message in gmail.get_messages():
        updated = '\n'.join([m.rstrip('=') for m in message.split('\r\n')])
        print(updated)


if __name__ == '__main__':
    main()
