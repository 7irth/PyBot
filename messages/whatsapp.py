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


def extract_messages(database, outfile='wa_messages', sort=False):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    formatted = open(outfile + '.txt', 'w')

    msgs = c.execute('SELECT timestamp, key_from_me, key_remote_jid, '
                     'remote_resource, data, media_mime_type '
                     'FROM messages WHERE timestamp IS NOT 0').fetchall()

    for msg in msgs:
        ts, from_me, j_id, group, message, media = msg

        if from_me:
            if group is not None:
                continue  # renamed conversation
            sender = 'me@' + j_id.split('@')[0]
        else:
            if group is None or group == '':  # single chat
                sender = j_id.split('@')[0] + '@me'

            else:  # group chat
                sender = group.split('@')[0] + '@' + j_id.split('@')[0]

        # figure out message
        if message is not None:
            body = str(message.encode())[2:-1]
        elif media is not None:
            body = media
        else:
            continue  # calls and images

        if sort:
            make_threads(ts, sender, body)

        formatted.write(str(ts) + ' | ' + sender + ' | ' + body + '\n')
    formatted.close()


def search_for_message(c, ts):
    return c.execute('SELECT * from messages '
                     'WHERE timestamp=?', (ts,)).fetchall()


# TODO: increase efficiency
def make_threads(sent, sender, msg):
    makedirs('convos', exist_ok=True)

    try:
        info = sender.split('@')
        sndr = phonebook[info[0]]
        receiver = phonebook[info[1]]

        file_name = (receiver['name'] if receiver['type'] == 'group' or
                                         sndr['name'] == 'me'
                     else sndr['name'])

        with open('convos\\' + file_name + '.txt', 'a') as chat:
            chat.write(str(sent) + ' | ' + sndr['name'] + ' | ' + msg + '\n')

    except KeyError:
        print(sender, 'not found in phonebook')


def go():
    wa_db = input('wa.db: ')
    msgstore = input('msgstore.db: ')

    read_contacts(wa_db)
    extract_messages(msgstore, sort=True)

    convo = input('Conversation to analyze: ')
    conversation_frequency(convo, graph=True, today=True)


if __name__ == '__main__':
    go()