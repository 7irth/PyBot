__author__ = 'Tirth'

import solver
from collections import OrderedDict
from imaging import *
from pybot import tom_delay, debug

runs = 3


def open_sudoku_on_chrome():
    time.sleep(tom_delay)

    press("winkey")

    time.sleep(tom_delay)

    enter_phrase("google chrome")
    press("enter")

    time.sleep(tom_delay)

    press_hold_release("ctrl", "t")

    time.sleep(tom_delay)

    enter_phrase("websudoku.com")
    press("enter")
    # press_hold_release("winkey", "up_arrow")

    time.sleep(tom_delay + 3)


def switch_to_evil():
    pass


# returns coordinates and size of puzzle
def find_puzzle(sample_in=screen_grab()):
    columns, rows = sample_in.size

    min_x_size, min_y_size = 250, 250
    init_pixel = (102, 102, 153)  # from target image

    sample = sample_in.load()

    x, y = -1, -1
    first_x, first_y, x_size, y_size = 0, 0, 0, 0

    while y + 1 < rows:
        y += 1  # next row
        x = -1  # reset column

        while x + 1 < columns:
            x += 1  # next column

            if close_enough(sample[x, y], init_pixel, 1):
                first_x, first_y = x, y

                while close_enough(sample[x, y], sample[x + 1, y]):  # row
                    x += 1
                x_size = x - first_x + 1

                x = first_x  # reset x
                while close_enough(sample[x, y], sample[x, y + 1]):  # col
                    y += 1
                y_size = y - first_y + 1

                if x_size > min_x_size and y_size > min_y_size:
                    return first_x, first_y, x_size, y_size

    return None, None, None, None


# returns array of given values in puzzle
def get_puzzle(sudoku_img):
    puzzle = sudoku_img.load()
    puzzle_size = 9

    first = None

    # initialize new puzzle
    sudoku = [0 for _ in range(81)]

    border = puzzle[0, 0]

    # find top left cell
    for i in range(puzzle_size):
        if puzzle[i, i] != border:
            first = [i, i]
            break

    if first:
        x = first[0]
        y = first[1]

        x_size = 1
        while close_enough(puzzle[x, y], puzzle[x, y + 1]):  # check row
            y += 1
            x_size += 1

        y_size = 1
        while close_enough(puzzle[x, y], puzzle[x + 1, y]):  # check col
            x += 1
            y_size += 1

        x = first[0]  # reset
        y = first[1]  # current

        for row in range(puzzle_size):
            for col in range(puzzle_size):

                if row in [2, 5, 8]:  # irregular cell size TODO: make elegant
                    y_size -= 1

                cell = sudoku_img.crop((x, y, x + x_size, y + y_size))

                if row in [2, 5, 8]:
                    y_size += 1

                # print_img(cell, 'all/' + str(row * 9 + col))

                # retrieve value from OCR and fill in puzzle
                try:
                    sudoku[row * puzzle_size + col] = int(tesser(cell))
                except ValueError:
                    pass

                # compensate for thicker column breaks
                x += x_size + (2 if col in [2, 5] else 1)

            y += y_size + 1  # compensate for row breaks
            x = first[0]

    return sudoku


# returns array of given values in puzzle using magic numbers
def get_puzzle_old(sudoku):
    loaded = sudoku.load()

    # magic numbers for character recognition
    numbers = OrderedDict()
    numbers[(9, 22, 15)] = []
    numbers[(6, 12, 15)] = []
    numbers[(4, 12, 19)] = []
    numbers[(8, 13, 20)] = []
    numbers[(5, 14, 14)] = []
    numbers[(7, 22, 9)] = []
    numbers[(2, 21, 24)] = []
    numbers[(3, 13, 11)] = []
    numbers[(1, 15, 10)] = []

    got = []

    for row in range(9):
        for col in range(9):
            for number in numbers:
                x = number[1] + col * 33  # width of the box
                y = number[2] + row * 33  # height of the box

                if col > 2:
                    x += 1

                if col > 5:
                    x += 1

                if (row, col) not in got and (loaded[x, y] != (255, 255, 255)):
                    numbers[number].append((row, col))
                    got.append((row, col))

    # initialize new puzzle
    puzzle = [0 for _ in range(81)]

    # fill with given values
    for value in numbers:
        for coords in numbers[value]:
            puzzle[coords[0] * 9 + coords[1]] = value[0]

    return puzzle


# takes in picture of puzzle, then solves and submits it
def solve_puzzle(puzzle):
    sudoku = solver.Sudoku()

    # try fast, likely inaccurate hack read, and slow accurate OCR read
    if sudoku.get_input(get_puzzle_old(puzzle)) \
        or sudoku.get_input(get_puzzle(puzzle)) \
            and sudoku.solve():
        submit_puzzle([number for row in sudoku.sudoku for number in row])

    else:
        # TODO: refresh and try again
        print("Couldn't solve puzzle :(")


def submit_puzzle(solved):
    for number in solved:
        press(str(number), 'tab', delay=0.005)

    press_hold_release('shift', 'tab')
    press('enter')


def next_puzzle(img_x, img_y):
    global runs
    runs -= 1

    if runs > 0:
        time.sleep(tom_delay)

        # find button for next puzzle
        bring_x, bring_y = find_target_by_edges(
            target_bring_button, screen_grab(img_x, img_y + 50, 300, 300))

        if bring_x is None:
            if debug:
                print_img(screen_grab(img_x, img_y + 50, 300, 300),
                          "send_to_tirth/bring_search")
            print("Couldn't find button for next puzzle")

        else:
            move(bring_x + img_x, bring_y + img_y + 50)
            left_click()
            time.sleep(tom_delay + 1)

            # find and solve next puzzle
            next_x, next_y, x_size, y_size = find_puzzle()

            if next_x is None:
                if debug:
                    print_img(screen_grab(), "send_to_tirth/next_sudoku")
                print("Couldn't find puzzle this time :(")

            else:
                move(next_x + 5, next_y + 5)
                left_click()

                solve_puzzle((screen_grab(next_x, next_y, x_size, y_size)))

                print(runs, "runs" if runs > 1 else "run", "left")
                next_puzzle(next_x, next_y)

    else:
        # press_hold_release("winkey", "down_arrow")
        # press_hold_release("winkey", "down_arrow")
        print("You get the point")


def go():
    global runs
    # runs = int(float(input("Runs through the puzzle (try at least 2): ")))
    #
    # print("Please don't move the mouse while the bot is working\n")
    # time.sleep(tom_delay)

    # open_sudoku_on_chrome()

    img_x, img_y, x_size, y_size = find_puzzle()

    if img_x is None:
        if debug:
            print_img(screen_grab(), "send_to_tirth/no_joy")
        input("Couldn't find puzzle! Press the any key (it's enter) to exit")

    else:
        print("Found puzzle! Going to try", runs, "runs")
        puzzle = screen_grab(img_x, img_y, x_size, y_size)

        move(img_x + 5, img_y + 5)
        left_click()

        if debug:
            print_img(puzzle, "send_to_tirth/initial_found_puzzle")

        solve_puzzle(puzzle)

        # next_puzzle(img_x, img_y)

        input("\nIronically, press enter to exit")  # to keep prompt open