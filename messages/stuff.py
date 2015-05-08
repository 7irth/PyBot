__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import datetime as dt
import xlsxwriter


def conversation_frequency(convo_name, graph=False, by_len=True, today=False):
    messages = open(convo_name + '.txt', 'r')
    people = []
    freq = {}

    # count up messages per day
    for message in messages:
        sent, sender, msg = message.split(' | ')[:3]
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

    first = [int(d) for d in days[0].split('-')]
    first_day = dt.date(first[0], first[1], first[2])

    last = [int(d) for d in days[len(days) - 1].split('-')]
    last_day = dt.date(last[0], last[1], last[2]) if today else dt.date.today()

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
