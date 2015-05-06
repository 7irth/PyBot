import os

__author__ = 'Tirth'

import requests
import bs4
import re
import json
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


def get_messages(session, fb_dtsg, my_id, friend_id, friend_name, group=False):
    offset = 0
    num_messages = 0

    output = open(friend_name + '.txt', 'w')

    while True:

        url = friend_url(my_id, friend_id, offset, fb_dtsg)
        data = session.get(url, headers=headers, verify=False).text

        messages = json.loads(data[9:])['payload']['actions']
        num_messages += len(messages)

        for message in messages:
            date = message['timestamp_datetime']
            author = 'me' if int(
                message['author'].split(':')[1]) == my_id else friend_name
            body = message['body'].encode('utf8')
            source = 'mobile' if 'mobile' in ' '.join(
                message['source_tags']) else 'web'

            output.write(
                ' | '.join([date, author, str(body)[2:-1], source]) + '\n')

        if len(messages) < json_limit:
            print('Got', num_messages, 'in total with', friend_name)
            break
        else:
            offset += json_limit
            print(num_messages, 'so far')

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
    return session.post("https://www.facebook.com/login.php?login_attempt=1",
                        data=login_data, verify=False)


def go():
    sesh = requests.Session()

    username = input('FB account email: ')
    password = input('Password (you can trust me *shifty eyes*): ')

    fb = login(sesh, username, password).content.decode()

    try:
        print('Logging in...', end=' ')

        access_token = \
            re.search(r'fb_dtsg\" value=\"(.*)\"', fb).group(1).split('\"')[0]

        print('successful!')

        m_id = int(input('Your FB ID: '))
        f_id = int(input('Your friend\'s FB ID: '))
        f_name = input('Your friend\'s name: ')

        get_messages(sesh, access_token, m_id, f_id, f_name)

    except AttributeError:
        print('failed :(')


if __name__ == '__main__':
    go()