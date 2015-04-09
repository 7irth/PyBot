__author__ = 'Tirth Patel <complaints@tirthpatel.com>'
version = "0.0.2"

import sudoku_stuff
from imaging import *

debug = False
functions = ["sudoku", "kill all humans"]
tom_delay = 1


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


if __name__ == '__main__':
    # choice = greeting()

    # if choice == "sudoku":
        sudoku_stuff.go()