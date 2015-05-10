__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

from bs4 import BeautifulSoup


def extract_messages(file):
    with open(file + '.xml', 'rb') as sms:
        soup = BeautifulSoup(sms, from_encoding='utf8')
        print(soup.thread)


def go():
    extract_messages('sms')


if __name__ == '__main__':
    go()