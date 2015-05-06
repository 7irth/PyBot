__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import requests
import bs4
import re
import json
import os
from datetime import datetime
import xlsxwriter

os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.getcwd(), "cacert.pem")

json_limit = 5000

headers = {'Host': 'www.facebook.com',
           'Origin': 'http://www.facebook.com',
           'Referer': 'http://www.facebook.com/',
           'User-Agent': '"user-agent": "NCSA_Mosaic/2.0 (Windows 3.1)'}


# ajax for friend messages
def friend_url(my_id, friend_id, offset, fb_dtsg):
    return ('https://www.facebook.com/ajax/mercury/thread_info.php?&messages'
            '[user_ids][%d][limit]=%d&messages[user_ids][%d][offset]=%d'
            '&client=web_messenger&__user=%d&__a=1&fb_dtsg=%s' %
            (friend_id, json_limit, friend_id, offset, my_id, fb_dtsg))


# ajax for group messages
def group_url(my_id, friend_id, offset, fb_dtsg):
    return ('https://www.facebook.com/ajax/mercury/thread_info.php?&messages'
            '[thread_fbids][%d][limit]=%d&messages[thread_fbids][%d][offset]'
            '=%d&client=web_messenger&__user=%d&__a=1&fb_dtsg=%s' %
            (friend_id, json_limit, friend_id, offset, my_id, fb_dtsg))


def get_messages(session, fb_dtsg, my_id, friend_id, convo_name, group=False):
    offset = 0
    num_messages = 0

    output = open(convo_name + '.txt', 'w')

    while True:

        url = friend_url(my_id, friend_id, offset, fb_dtsg)
        data = session.get(url, headers=headers, verify=False).text

        messages = json.loads(data[9:])['payload']['actions']
        num_messages += len(messages)

        for message in messages:

            # print(str(message).encode('utf-8'))

            date = str(message['timestamp'])
            author = ('me' if int(message['author'].split(':')[1])
                              == my_id else convo_name)
            source = ('mobile' if 'mobile' in ' '.join(message['source_tags'])
                      else 'web')

            try:
                body = message['body'].encode('utf8')  # TODO: encode properly
                output.write(' | '.join(
                    [date, author, str(body)[2:-1], source]) + '\n')
            except KeyError:
                pass  # not a text message

        if len(messages) < json_limit:
            print('Got', num_messages, 'messages with', convo_name)
            break
        else:
            offset += json_limit
            print(num_messages, 'so far, getting more')

    output.close()


def login(session, username, password):
    login_page = session.get("https://www.facebook.com/").text
    login_soup = bs4.BeautifulSoup(login_page)

    lsd = str(login_soup.find_all('input', attrs={"name": "lsd"})[0]['value'])

    # assemble data for login POST
    login_data = {
        'locale': 'en_US',
        'non_com_login': '',
        'email': username,
        'pass': password,
        'lsd': lsd
    }

    # log in and return the response
    return session.post('https://www.facebook.com/login.php?login_attempt=1',
                        data=login_data, verify=False)


def conversation_frequency(convo_name):
    messages = open(convo_name + '.txt', 'r')
    freq = {}

    # count up messages per day
    for message in messages:
        sent, sender = message.split(' | ')[:2]
        date = datetime.fromtimestamp(int(sent) // 1000).strftime('%Y-%m-%d')

        if date not in freq.keys():
            freq[date] = {convo_name: 0, 'me': 0}

        freq[date][sender] += 1

    csv = open(convo_name + '.csv', 'w')
    csv.write('Day,me,' + convo_name + '\n')

    received, sent = 0, 0

    for day in freq:
        received += freq[day][convo_name]
        sent += freq[day]['me']

        csv.write(day + ',' + str(freq[day]['me']) + ',' +
                  str(freq[day][convo_name]) + '\n')

    csv.close()

    print(received, sent)


def go():
    sesh = requests.Session()

    # TODO: embed certs
    # with open('certs', 'w') as certs:
    #     r = requests.get('http://curl.haxx.se/ca/cacert.pem')
    #     print(r.content.decode('utf-8'))

    username = input('FB account email: ')
    password = input('Password (you can trust me *shifty eyes*): ')

    fb = login(sesh, username, password).content.decode()

    print('Logging in...', end=' ')

    try:
        access_token = \
            re.search(r'fb_dtsg\" value=\"(.*)\"', fb).group(1).split('\"')[0]
        m_id = int(re.findall(r'id="profile_pic_header_(\d+?)"', fb)[0])

        print('successful!')

        f_id = input('Your friend\'s FB ID: ')

        # get friend's name from ID
        data = sesh.get('https://www.facebook.com/' + f_id, headers=headers,
                        verify=False).content.decode('utf-8')
        f_name = re.findall(r'pageTitle">(.*?)</title>', data)[0].split(' ')[0]

        get_messages(sesh, access_token, m_id, int(f_id), f_name)
        conversation_frequency(f_name)

    except AttributeError:
        print('failed :(')


if __name__ == '__main__':
    go()