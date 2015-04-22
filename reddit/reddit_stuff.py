__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import praw

if __name__ == '__main__':
    r = praw.Reddit('thing for testing')
    for entry in r.get_subreddit('mildlyinteresting').get_top(limit=10):
        print(entry)