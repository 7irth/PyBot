__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import sqlite3
from bs4 import BeautifulSoup
from messages.stuff import *


def extract_messages_sqlite(database, outfile='sms_all'):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    msgs = c.execute('SELECT date_sent, date, person, address, body '
                     'FROM sms').fetchall()

    formatted = open(outfile + '.txt', 'w')

    for msg in msgs:
        ts, o_ts, sender, number, content = msg

        sent = str(ts) if ts != 0 else str(o_ts)
        sndr = 'me' if sender is None else number
        body = ' '.join(content.split('\n'))

        make_threads(sent, sndr, number, body)

        try:
            formatted.write(sent + SEPR + sndr + SEPR + body + '\n')
        except UnicodeEncodeError:
            print('skipping', ts)

    formatted.close()


def make_threads(sent, sender, number, msg):
    if number == '':
        with open('test.txt', 'a') as sms:
            sms.write(sent + SEPR + sender + SEPR + msg + '\n')


def get_db_entry(database, ts):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    return c.execute('SELECT * FROM sms WHERE date_sent=?', (ts,)).fetchall()


def extract_messages_titanium(file):
    with open(file + '.xml', 'rb') as sms:
        soup = BeautifulSoup(sms)
        print(soup.thread)


def go():
    extract_messages_sqlite('mmssms.db')


if __name__ == '__main__':
    go()
    # conversation_frequency('sms_all', graph=True)