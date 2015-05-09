__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import feedparser


def go():
    a = feedparser.parse('http://feeds.arstechnica.com/arstechnica/index.xml')
    for entry in a.entries:
        print(entry.title)


if __name__ == '__main__':
    go()