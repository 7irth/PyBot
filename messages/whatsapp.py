__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

from messages.stuff import *


def read_contacts(contacts):
    pass


def format_whatsapp(file):
    formatted = open(file + '-f.txt', 'w')

    with open(file + '.txt', encoding='utf8') as msgs:
        for msg in msgs:
            try:
                ts, from_me, number, m = str(msg.encode())[2:-3].split('|')
            except ValueError:
                continue  # paragraph in message

            sender = 'me' if from_me == '1' \
                else number.split('@')[0]

            formatted.write(ts + ' | ' + sender + ' | ' + m + '\n')
    formatted.close()


if __name__ == '__main__':
    format_whatsapp('wa_messages')
