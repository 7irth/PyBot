__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import sqlite3
from datetime import datetime
from os import makedirs
from bs4 import BeautifulSoup
import phonenumbers
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


def extract_messages_titanium(file, out_folder='t_sms'):
    makedirs(out_folder, exist_ok=True)

    with open(file + '.xml', 'rb') as sms:
        for thread in BeautifulSoup(sms)('thread'):
            convo = thread['address']

            try:
                number = str(phonenumbers.parse(convo, "CA").national_number)
            except phonenumbers.NumberParseException:
                # print([phonenumbers.parse(n, "CA").national_number for n in convo.split(';')])
                continue  # group message

            with open(out_folder + '/' + number + '.txt', 'w') as current:
                for msg in thread.find_all('sms'):
                    try:
                        date = msg['datesent']
                    except KeyError:
                        date = msg['date']

                    sent = '{0:0<13}'.format(str(datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()).replace('.', ''))
                    sender = 'me' if msg['msgbox'] == 'sent' else number
                    body = msg.string

                    if len(sent) < 2:
                        print(msg.attrs)
                        exit()

                    try:
                        current.write(sent + SEPR + sender + SEPR + body + '\n')
                    except UnicodeEncodeError:
                        print(str(msg.string).encode())

                current.close()


def go():
    # extract_messages_sqlite('mmssms.db')
    extract_messages_titanium('sms')

if __name__ == '__main__':
    go()
    conversation_frequency('', graph=True)