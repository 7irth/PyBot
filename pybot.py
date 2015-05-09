__author__ = 'Tirth Patel <complaints@tirthpatel.com>'
version = '0.0.5'

from time import time, sleep

import sudoku
import crossword
import messages
# import reddit
import rss


debug = True
timings = True
functions = ['sudoku', 'crossword', 'facebook', 'whatsapp', 'reddit',
             'rss', 'kill all humans']
tom_delay = 1


def choose():
    picked = input('Pick a function - ' + str(functions) + ': ')

    while picked not in functions:
        picked = input("Invalid choice, try again foo': ")
        if picked == 'exit':
            exit()

    if picked == 'sudoku':
        sudoku.stuff.go()
    elif picked == 'crossword':
        crossword.stuff.go()
    elif picked == 'facebook':
        messages.fb.go()
    elif picked == 'whatsapp':
        messages.whatsapp.go()
    # elif picked == 'reddit':
    #     reddit.stuff.go()
    elif picked == 'rss':
        rss.stuff.go()


def chill_out_for_a_bit(extra_delay=0):
    delay = tom_delay + extra_delay
    if timings:
        print('sleeping for', delay, 'seconds' if delay != 1 else 'second')
    sleep(delay)


class Timer:
    def __init__(self, label):
        self.label = label

    def __enter__(self):
        if timings:
            print(self.label, end=' ')
        self.start = time()
        return self

    def __exit__(self, *args):
        self.time = time() - self.start
        if timings:
            print('took', str(round(self.time, 5)), 'seconds')


if __name__ == '__main__':
    # debug = timings = True if input('Debug? (y/n) ') == 'y' else False

    print('PyBot! v' + version + ('-debug' if debug else ''))

    # print("Enter time delay between steps -")
    # tom_delay = float(input((
    #     "(1 second works for me, might need more for slower computers): ")))

    choose()

    input("\nIronically, press enter to exit")