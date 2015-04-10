__author__ = 'Tirth Patel <complaints@tirthpatel.com>'
version = "0.0.3"

import sudoku_stuff
from imaging import *

debug = True
timings = True
functions = ["sudoku", "kill all humans"]
tom_delay = 3


def greeting():
    global tom_delay

    print("PyBot! v" + version, end='')
    if debug:
        print("-debug")
        os.makedirs("send_to_tirth", exist_ok=True)
    else:
        print()
    print("Enter time delay between steps -")
    tom_delay = float(input((
        "(1 second works for me, might need more for slower computers): ")))

    picked = input("Pick a function - " + str(functions) + ": ")

    while picked not in functions:
        picked = input("Invalid choice, try again foo': ")
        if picked == "exit":
            exit()

    return picked


def chill_out_for_a_bit(extra=0):
    delay = tom_delay + extra
    if timings:
        print("sleeping for", delay, "seconds" if delay != 1 else "second")
    time.sleep(delay)


class Timer:
    def __init__(self, label):
        self.label = label

    def __enter__(self):
        if timings:
            print(self.label, end=' ')
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.time = time.clock() - self.start
        if timings:
            print('took', str(round(self.time, 5)), 'seconds')


if __name__ == '__main__':
    choice = greeting()

    if choice == "sudoku":
        sudoku_stuff.go()