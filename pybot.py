__author__ = 'Tirth Patel <complaints@tirthpatel.com>'
version = "0.0.2"

import sudoku_stuff
from imaging import *

debug = True
functions = ["sudoku", "kill all humans"]
choice = ""
tom_delay = 1


def greeting():
    global tom_delay, choice

    print("PyBot! v" + version, end='')
    if debug:
        print("-debug")
        os.makedirs("send_to_tirth", exist_ok=True)
    else:
        print()
    print("Enter time delay between steps -")
    tom_delay = float(input((
        "(1 second works for me, might need more for slower computers): ")))

    choice = input("Pick a function! Options - " + str(functions) + ": ")

    while choice not in functions:
        choice = input("Invalid choice, try again foo': ")
        if choice == "exit":
            exit()


if __name__ == '__main__':
    greeting()

    if choice == "sudoku":
        sudoku_stuff.go()