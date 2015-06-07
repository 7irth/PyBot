__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import datetime as dt
import xlsxwriter
import nltk

SEPR = ' | '
contacts = {}


class ConvoIter:
    def __init__(self, name, convo):
        self.name = name
        self.convo = convo
        self.size = len(self.convo)
        self.idx = 0

    def next_ts(self):
        return (int(self.convo[self.idx].split(SEPR)[0])
                if self.idx < self.size else 2000000000000)

    def current(self):
        return self.convo[self.idx]

    def next(self):
        if self.idx < self.size:
            n = self.convo[self.idx]
            self.idx += 1
            return n

    def __str__(self):
        return str(self.convo)


def merge_conversations(*convos):
    files = {}
    total_size = 0
    merged = []
    outfile = ''

    for convo in convos:
        sort_by_time(convo)  # quicker to check if sorted first?

        with open(convo + '.txt') as conv:
            files[convo] = ConvoIter(convo, list(conv))
            total_size += files[convo].size
        outfile += convo.split('\\')[1] + '-'

    oldest = None
    while len(merged) < total_size:

        smallest_ts = 2000000000000
        for file in files.values():
            if file.next_ts() < smallest_ts:
                smallest_ts = file.next_ts()
                oldest = file

        merged.append(oldest.next())

    with open(outfile[:-1] + '.txt', 'w') as merged_convos:
        for m in merged:
            merged_convos.write(m)


def sort_by_time(convo):
    with open(convo + '.txt') as conv:
        messages = list(conv)

    with open(convo + '.txt', 'w') as s:
        s.writelines(sorted(messages, key=lambda m: m.split(SEPR)[0]))


def conversation_frequency(convo_name, graph=False, by_len=True,
                           from_date=None, to_date=None):
    messages = open(convo_name + '.txt', 'r')
    people = []
    freq = {}

    # count up messages per day
    for message in messages:
        sent, sender, msg = message.split(SEPR)[:3]
        date = dt.datetime.fromtimestamp(int(sent[:-3])).strftime('%Y-%m-%d')

        if sender not in people:
            people.append(sender)

        if date not in freq.keys():
            freq[date] = {}

        if sender not in freq[date]:
            freq[date][sender] = 0

        freq[date][sender] += len(msg) if by_len else 1

    # fill in empty days
    total_freq = {}

    days = sorted(freq.keys())

    if from_date:
        first_day = dt.date(from_date[0], from_date[1], from_date[2])
    else:
        first = [int(d) for d in days[0].split('-')]
        first_day = dt.date(first[0], first[1], first[2])

    if to_date:
        last_day = (dt.date(to_date[0], to_date[1], to_date[2])
                    if to_date != 'today' else dt.date.today())
    else:
        last = [int(d) for d in days[len(days) - 1].split('-')]
        last_day = dt.date(last[0], last[1], last[2])

    uno = dt.timedelta(days=1)
    total_days = (last_day - first_day).days

    # go through all elapsed days, filling in data if present
    curr = first_day
    for _ in range(total_days + 1):
        total_freq[str(curr)] = freq[str(curr)] if str(curr) in days else {}
        curr += uno

    # fill in zeros
    for day in total_freq.values():
        for person in people:
            if person not in day:
                day[person] = 0

    if graph:
        graph_frequency(total_freq, people, convo_name.split('\\')[-1])

    return total_freq, people


def daily_frequency(convo_name, graph=False, by_len=True):
    messages = open(convo_name + '.txt', 'r')
    people = []
    freq = {'Monday': {},
            'Tuesday': {},
            'Wednesday': {},
            'Thursday': {},
            'Friday': {},
            'Saturday': {},
            'Sunday': {}}

    # count up messages per day
    for message in messages:
        sent, sender, msg = message.split(SEPR)[:3]
        day = dt.datetime.fromtimestamp(int(sent[:-3])).strftime('%A')

        if sender not in people:
            people.append(sender)

        if sender not in freq[day]:
            freq[day][sender] = 0

        freq[day][sender] += len(msg) if by_len else 1

    return freq


def hourly_frequency(convo_name, graph=False, by_len=True):
    messages = open(convo_name + '.txt', 'r')
    people = []
    freq = {'{:02}'.format(h): {} for h in range(24)}

    # count up messages per hour
    for message in messages:
        sent, sender, msg = message.split(SEPR)[:3]
        hour = dt.datetime.fromtimestamp(int(sent[:-3])).strftime('%H')

        if sender not in people:
            people.append(sender)

        if sender not in freq[hour]:
            freq[hour][sender] = 0

        freq[hour][sender] += len(msg) if by_len else 1

    return freq


def word_frequency(convo_name):
    bodies = ''

    with open(convo_name + '.txt', 'r') as msgs:
        for msg in msgs:
            sent, sender, body = msg.split(SEPR)[:3]
            bodies += body.lower() + ' '

    text = nltk.Text(nltk.word_tokenize(bodies))
    nltk.FreqDist(text).plot(100)


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

    chart.set_title({'name': 'Message Frequency for ' + convo_name})
    chart.set_y_axis({'name': 'Messages'})

    chart.set_style(2)
    chart.set_size({'x_scale': 5, 'y_scale': 3})

    worksheet.insert_chart('B5', chart)

    workbook.close()

    for person in sorted(peeps, key=peeps.get, reverse=True):
        print('{amount:<7} {name}'.format(name=person, amount=peeps[person]))


if __name__ == '__main__':
    pass
