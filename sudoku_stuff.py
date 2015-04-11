__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import solver
from collections import OrderedDict
from pybot import *

runs = 3


def open_sudoku_on_chrome():
    chill_out_for_a_bit()

    press("winkey")

    chill_out_for_a_bit()

    enter_phrase("google chrome")
    press("enter")

    chill_out_for_a_bit()

    press_hold_release("ctrl", "t")

    chill_out_for_a_bit()

    enter_phrase("websudoku.com")
    press("enter")
    # press_hold_release("winkey", "up_arrow")


def switch_to_evil():
    pass


# size of ? shaped box with a top left corner at (x, y)
def get_box_size(puzzle, x, y):
    first_x, first_y = int(x), int(y)

    while close_enough(puzzle[x, y], puzzle[x + 1, y]):  # check row
        x += 1

    while close_enough(puzzle[x, y], puzzle[x, y + 1]):  # check col
        y += 1

    return x - first_x + 1, y - first_y + 1  # x_size, y_size ?


# returns coordinates and size of puzzle
def find_puzzle(sample_in=screen_grab()):
    columns, rows = sample_in.size

    min_x_size, min_y_size = 250, 250
    init_pixel = (102, 102, 153)  # from target image

    sample = sample_in.load()

    x, y = -1, -1

    while y + 1 < rows:
        y += 1  # next row
        x = -1  # reset column

        while x + 1 < columns:
            x += 1  # next column

            if close_enough(sample[x, y], init_pixel, 3):  # first pixel match
                size = get_box_size(sample, x, y)

                if size > (min_x_size, min_y_size):
                    return x, y, size[0], size[1]

    return None, None, None, None


# returns array of given values in puzzle
def get_puzzle(sudoku_img):
    puzzle = sudoku_img.load()
    puzzle_size = 9

    # initialize new puzzle
    sudoku = [0 for _ in range(81)]

    border = puzzle[0, 0]

    # find top left cell
    for i in range(puzzle_size):
        if puzzle[i, i] != border:
            x, y = i, i

            x_size, y_size = get_box_size(puzzle, x, y)

            for row in range(puzzle_size):
                for col in range(puzzle_size):

                    # correct box size
                    x_size, y_size = get_box_size(puzzle, x, y)

                    cell = sudoku_img.crop((x, y, x + x_size, y + y_size))

                    if debug:
                        print_img(cell, 'all/' + str(row * puzzle_size + col))

                    # retrieve value from OCR and fill in puzzle
                    try:
                        sudoku[row * puzzle_size + col] = \
                            int(tesser(cell, '10', 'digits'))
                    except ValueError:
                        pass

                    # compensate for thicker column breaks
                    x += x_size + (2 if col in [2, 5] else 1)

                # compensate for row breaks
                y += y_size + (2 if row in [2, 5] else 1)
                x -= x_size * puzzle_size + 11  # reset to start

            return sudoku
    return sudoku


# returns array of given values in puzzle using magic numbers
def get_puzzle_hack(sudoku):
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
def solve_puzzle(sudoku_img):
    sudoku = solver.Sudoku()
    found = False

    with Timer('getting numbers the easy way'):
        if sudoku.get_input(get_puzzle_hack(sudoku_img)):
            found = True

    if not found:
        with Timer('getting numbers the hard way'):
            if sudoku.get_input(get_puzzle(sudoku_img)):
                found = True

    if found:
        with Timer('solving the puzzle'):
            sudoku.solve()
        submit_puzzle([number for row in sudoku.sudoku for number in row])
    else:
        # TODO: refresh and try again
        raise SudokuException


class SudokuException(Exception):
    pass


def submit_puzzle(solved):
    for number in solved:
        press(str(number), 'tab', delay=0.005)

    press_hold_release('shift', 'tab')
    press('enter')


def next_puzzle(old_x, old_y, old_x_size, old_y_size):
    global runs

    if runs > 0:
        chill_out_for_a_bit()

        bring_search = screen_grab(old_x, old_y, old_x_size, old_y_size)
        with Timer("finding the button for next puzzle"):
            buttons = find_buttons(bring_search)

        try:
            bring_x, bring_y, bring_x_size, bring_y_size = \
                buttons['Bring on a new puzzle!']

            bring_x += bring_x_size // 2 + old_x
            bring_y += bring_y_size // 2 + old_y

            move(bring_x, bring_y)
            left_click()
            chill_out_for_a_bit(1)

            # increased search area for next puzzle
            old_x -= 50
            old_y -= 50

            next_search = screen_grab(old_x, old_y,
                                      old_x_size + 100, old_y_size + 100)

            print_img(next_search, "send_to_tirth/next_sudoku")

            with Timer('finding the next puzzle'):
                next_x, next_y, x_size, y_size = find_puzzle(next_search)

            if next_x is None:
                if debug:
                    print_img(next_search, "send_to_tirth/next_sudoku")
                print("Couldn't find puzzle this time :(")

            else:
                next_x += old_x
                next_y += old_y

                move(next_x + 5, next_y + 5)
                left_click()

                solve_puzzle((screen_grab(next_x, next_y, x_size, y_size)))

                runs -= 1
                print(runs, "runs" if runs != 1 else "run", "left")
                next_puzzle(next_x, next_y, x_size, y_size)

        except KeyError:
            if debug:
                print_img(bring_search, "send_to_tirth/bring_search")
            print("Couldn't find button for next puzzle")

    else:
        # press_hold_release("winkey", "down_arrow")
        # press_hold_release("winkey", "down_arrow")
        print("You get the point")


def go():
    global runs
    runs = int(float(input("Runs through the puzzle (try at least 2): ")))

    print("Please don't move and/or breathe while the bot is working,\n"
          "and keep your arms and legs inside the ride at all times\n")

    open_sudoku_on_chrome()
    chill_out_for_a_bit(2)

    initial_search = screen_grab()

    with Timer('finding the puzzle'):
        img_x, img_y, x_size, y_size = find_puzzle(initial_search)

    if img_x is None:
        if debug:
            print_img(initial_search, "send_to_tirth/no_joy")
        input("Couldn't find puzzle! Press the any key (it's enter) to exit")

    else:
        print("Found puzzle! Going to try", runs, "runs")
        puzzle = screen_grab(img_x, img_y, x_size, y_size)

        move(img_x + 5, img_y + 5)
        left_click()

        if debug:
            print_img(puzzle, "send_to_tirth/initial_found_puzzle")

        try:
            solve_puzzle(puzzle)
            next_puzzle(img_x, img_y, x_size, y_size)
        except SudokuException:
            print("Couldn't solve puzzle :(")

        input("\nIronically, press enter to exit")  # to keep prompt open