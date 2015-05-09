__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import sqlite3
from os import makedirs
from messages.stuff import *

phonebook = {'me': {'name': 'me', 'type': 'person'}}


def read_contacts(database):
    global phonebook

    conn = sqlite3.connect(database)
    c = conn.cursor()

    rows = c.execute('SELECT jid, display_name FROM wa_contacts').fetchall()

    for row in rows:
        sender = row[0].split('@')

        if sender[1] == 'g.us':
            phonebook[sender[0]] = {'name': row[1], 'type': 'group'}
        else:
            phonebook[sender[0]] = {'name': row[1] if row[1] is not None
            else "No name", 'type': 'person'}
            

class WhatsAppMessage:
    def __init__(self, ts, from_me, j_id, group, message, media):
        self.ts = ts
        self.sender = self.get_sender(from_me, j_id, group)
        self.body = self.get_body(message, media)

    @staticmethod
    def get_sender(from_me, j_id, group):
        if from_me:
            if group is not None:
                raise MessageError  # renamed conversation
            sender = 'me@' + j_id.split('@')[0]
        else:
            if group is None or group == '':  # single chat
                sender = j_id.split('@')[0] + '@me'

            else:  # group chat
                sender = group.split('@')[0] + '@' + j_id.split('@')[0]

        return sender

    @staticmethod
    def get_body(message, media):
        if message is not None:
            body = str(message.encode())[2:-1]
        elif media is not None:
            body = media
        else:
            raise MessageError  # calls and images

        return body
                

class MessageError(Exception):
    pass


def extract_messages(database, outfile='wa_all', sort_all=False, choice=None):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    formatted = open(outfile + '.txt', 'w')

    msgs = c.execute('SELECT timestamp, key_from_me, key_remote_jid, '
                     'remote_resource, data, media_mime_type '
                     'FROM messages WHERE timestamp IS NOT 0').fetchall()

    for msg in msgs:
        ts, from_me, j_id, group, message, media = msg

        try:
            m = WhatsAppMessage(ts, from_me, j_id, group, message, media)
        except MessageError:
            continue

        if choice:
            make_threads(m.ts, m.sender, m.body, choice)
        elif sort_all:
            make_threads(m.ts, m.sender, m.body)

        formatted.write(str(m.ts) + SEPR + m.sender + SEPR + m.body + '\n')
    formatted.close()


def get_db_entry(database, ts):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    return c.execute('SELECT * from messages '
                     'WHERE timestamp=?', (ts,)).fetchall()


# TODO: increase efficiency
def make_threads(sent, sender, msg, choice=None):
    makedirs('convos', exist_ok=True)

    try:
        info = sender.split('@')
        sndr = phonebook[info[0]]
        receiver = phonebook[info[1]]

        file_name = (receiver['name'] if receiver['type'] == 'group' or
                                         sndr['name'] == 'me'
                     else sndr['name'])

        if not choice or file_name == choice:
            with open('convos\\' + file_name + '.txt', 'a') as chat:
                chat.write(str(sent) + SEPR + sndr['name'] + SEPR + msg + '\n')

    except KeyError:
        print(sender, 'not found in phonebook')


def go():
    # wa_db = input('wa.db: ')
    # msgstore = input('msgstore.db: ')

    wa_db = 'wa.db'
    msgstore = 'msgstore.db'

    read_contacts(wa_db)

    choice = input('Extract (all) or (contact name): ')
    extract_messages(msgstore, choice=(choice if choice != 'all' else None))

    # print(get_db_entry(msgstore, input('search timestamp: ')))

    convo = input('Conversation to analyze: ')
    conversation_frequency(convo, graph=True, to_date='today')


if __name__ == '__main__':
    go()