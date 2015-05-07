__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import requests
import re
import json
import os
from bs4 import BeautifulSoup
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
            '[user_ids][{friend_id}][limit]={json_limit}&messages[user_ids]'
            '[{friend_id}][offset]={offset}&client=web_messenger&__user='
            '{my_id}&__a=1&fb_dtsg={fb_dtsg}'
            .format(my_id=my_id, friend_id=friend_id, offset=offset,
                    json_limit=json_limit, fb_dtsg=fb_dtsg))


# ajax for group messages
def group_url(my_id, friend_id, offset, fb_dtsg):
    return ('https://www.facebook.com/ajax/mercury/thread_info.php?&messages'
            '[thread_fbids][{friend_id}][limit]={json_limit}&messages'
            '[thread_fbids][{friend_id}][offset]={offset}&client=web_messenger'
            '&__user={my_id}&__a=1&fb_dtsg={fb_dtsg}'
            .format(my_id=my_id, friend_id=friend_id, offset=offset,
                    json_limit=json_limit, fb_dtsg=fb_dtsg))


def get_messages(session, fb_dtsg, my_id, friend_id, convo_name, group=False):
    offset = 0
    num_messages = 0
    author_ids = {str(my_id): 'me'}

    output = open(convo_name + '.txt', 'w')

    while True:

        url = (group_url(my_id, friend_id, offset, fb_dtsg) if group
               else friend_url(my_id, friend_id, offset, fb_dtsg))

        f_page = session.get(url, headers=headers, verify=False).text

        messages = json.loads(f_page[9:])['payload']['actions']
        num_messages += len(messages)

        for message in messages:
            date = str(message['timestamp'])
            source = ('mobile' if 'mobile' in ' '.join(message['source_tags'])
                      else 'web')

            a_id = message['author'].split(':')[1]
            try:
                author = author_ids[a_id]
            except KeyError:

                # get author name from ID
                soup = BeautifulSoup(session.get(
                    'https://www.facebook.com/' + a_id,
                    headers=headers, verify=False).content.decode())

                author = soup.title.string
                author_ids[a_id] = author  # save name

            # TODO: encode properly
            body = str(message['body'].encode() if 'body' in message.keys()
                       else message['log_message_body'].encode())[2:-1]

            loc = ('No location' if message['coordinates'] is None else
                   str(message['coordinates']['latitude']) + ',' +
                   str(message['coordinates']['longitude']))

            try:
                if message['has_attachment']:
                    for attachment in message['attachments']:
                        if attachment['attach_type'] == 'sticker':
                            body += 'sticker'
                        else:
                            # print(attachment['attach_type'])
                            pass  # other kind of attachment
            except KeyError:
                pass  # log message

            output.write(' | '.join([date, author, body, source, loc]) + '\n')

        if len(messages) < json_limit:
            print('Got', num_messages, 'messages with', convo_name)
            break
        else:
            offset += json_limit
            print(num_messages, 'so far, getting more')

    output.close()


def login(session, username, password):
    login_page = session.get("https://www.facebook.com/").text
    login_soup = BeautifulSoup(login_page)

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


def conversation_frequency(convo_name, graph=False):
    messages = open(convo_name + '.txt', 'r')
    people = []
    freq = {}

    # count up messages per day
    for message in messages:
        sent, sender = message.split(' | ')[:2]
        date = datetime.fromtimestamp(int(sent) // 1000).strftime('%Y-%m-%d')

        if sender not in people:
            people.append(sender)

        if date not in freq.keys():
            freq[date] = {}

        if sender not in freq[date]:
            freq[date][sender] = 0

        freq[date][sender] += 1

    # fill in zeros
    for day in freq.values():
        for person in people:
            if person not in day:
                day[person] = 0

    if graph:
        graph_frequency(freq, people, convo_name)

    return freq, people


def graph_frequency(freq, people, convo_name):
    people.sort()

    chart_data = {n: [] for n in people}
    chart_data['day'] = []

    # total message counts
    peeps = {n: 0 for n in people}

    for day in sorted(freq):
        chart_data['day'].append(day)

        for person in freq[day]:
            peeps[person] += freq[day][person]
            chart_data[person].append(freq[day][person])

    # prepare chart
    workbook = xlsxwriter.Workbook(convo_name + '-freq.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})

    worksheet.write_row('A1', ['Day'] + people)
    worksheet.write_column('A2', chart_data['day'])

    # write data
    for idx, person in enumerate(people):
        worksheet.write_column(chr(ord('B') + idx) + '2', chart_data[person])

    chart = workbook.add_chart({'type': 'line'})
    data_size = len(chart_data['day'])

    for i in range(1, len(people) + 1):
        chart.add_series({
            'name': ['Sheet1', 0, i],
            'categories': ['Sheet1', 1, 0, data_size + 1, 0],
            'values': ['Sheet1', 1, i, data_size + 1, i]
        })

    chart.set_title({'name': 'FB Message Frequency'})
    chart.set_y_axis({'name': 'Messages sent'})

    chart.set_style(2)
    chart.set_size({'x_scale': 4, 'y_scale': 2})

    worksheet.insert_chart('B5', chart)

    workbook.close()

    for person in sorted(peeps, key=peeps.get, reverse=True):
        print('{amount:<5} {name}'.format(name=person, amount=peeps[person]))


# noinspection PyUnboundLocalVariable
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
    except AttributeError:
        print('failed :(')
        exit(1)

    kind = input('(F)riend or (G)roup messages? ')
    while kind not in ['f', 'g']:
        kind = input('Try again: ')

    f_id = input('Enter ID: ')
    while len(re.findall(r'^\d+$', f_id)) != 1:
        f_id = input('Try again: ')

    if kind.lower() == 'f':
        # get friend's name from ID
        c_name = BeautifulSoup(sesh.get('https://www.facebook.com/' + f_id,
                                        headers=headers, verify=False)
                               .text).title.string
        get_messages(sesh, access_token, m_id, int(f_id), c_name)
    else:
        # get group name from ID
        msgs = sesh.get(
            'https://www.facebook.com/messages/conversation-' + f_id,
            headers=headers, verify=False).text

        patter = '"thread_fbid":"' + f_id + '"(.*?)"snippet"'
        c_name = re.findall(r'"name":"(.*?)",', re.findall(patter, msgs)[0])[0]

        get_messages(sesh, access_token, m_id, int(f_id), c_name, True)

    # analyze and graph
    conversation_frequency(c_name, graph=True)


if __name__ == '__main__':
    go()