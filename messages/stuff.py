__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

from datetime import datetime
import xlsxwriter


def conversation_frequency(convo_name, delimiter=' | ', graph=False):
    messages = open(convo_name + '.txt', 'r')
    people = []
    freq = {}

    # count up messages per day
    for message in messages:
        sent, sender = message.split(delimiter)[:2]
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

    chart.set_title({'name': 'Message Frequency'})
    chart.set_y_axis({'name': 'Messages sent'})

    chart.set_style(2)
    chart.set_size({'x_scale': 4, 'y_scale': 2})

    worksheet.insert_chart('B5', chart)

    workbook.close()

    for person in sorted(peeps, key=peeps.get, reverse=True):
        print('{amount:<5} {name}'.format(name=person, amount=peeps[person]))
