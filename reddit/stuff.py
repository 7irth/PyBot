__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import praw


def top_entries(subreddit, limit=10):
    entries = []

    r = praw.Reddit('Testing things and other things by u/ctrlaltdemolish')
    for entry in r.get_subreddit(subreddit).get_top(limit=limit):
        entries.append(entry)

    return entries


def go():
    subreddit = input('Enter a subreddit: ')
    limit = int(float(input('How many top stories? ')))

    for e in top_entries(subreddit, limit):
        print(e)

if __name__ == '__main__':
    go()
