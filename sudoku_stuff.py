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


def find_puzzle(target_in, sample_in=screen_grab()):
    s_width, s_height = sample_in.size

    min_x_size, min_y_size = 250, 250

    target = target_in.load()
    sample = sample_in.load()

    init_pixel = target[0, 0]

    x, y = 0, 0
    first_x, first_y = 0, 0
    x_size, y_size = 0, 0

    found = False

    while y < s_height:
        while x < s_width:
            if close_enough(sample[x, y], init_pixel, 1):
                x_size, y_size = 1, 1
                first_x, first_y = x, y

                while close_enough(sample[x, y], sample[x + 1, y]):
                    x_size += 1
                    x += 1

                x = first_x
                while close_enough(sample[x, y], sample[x, y + 1]):
                    y_size += 1
                    y += 1

                if x_size > min_x_size and y_size > min_y_size:
                    found = True
                    break

            x += 1

        y += 1
        x = 0

        if found:
            return first_x, first_y, x_size, y_size

    return None, None, None, None


def get_puzzle(sudoku_img):
    puzzle = sudoku_img.load()
    puzzle_size = (9, 9)
    
    first = None

    # initialize new puzzle
    sudoku = [0 for _ in range(81)]

    border = puzzle[0, 0]

    # find top left cell
    for i in range(puzzle_size[0] + puzzle_size[1]):
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

        for row in range(puzzle_size[0]):
            for col in range(puzzle_size[1]):

                if row in [2, 5, 8]:  # irregular cell size TODO: make elegant
                    y_size -= 1

                cell = sudoku_img.crop((x, y, x + x_size, y + y_size))

                if row in [2, 5, 8]:
                    y_size += 1

                print_img(cell, 'all/' + str(row * 9 + col))

                # retrieve value from OCR
                # value = tesser(cell)
                #
                # # iterate through puzzle filling in found values
                # sudoku[row * 9 + col] = int(value) if value != '' else 0

                # compensate for thicker column breaks
                x += x_size + (2 if col in [2, 5] else 1)

            y += y_size + 1  # compensate for row breaks
            x = first[0]

    return sudoku


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
    for n in numbers:
        for thing in numbers[n]:
            puzzle[thing[0] * 9 + thing[1]] = n[0]

    return puzzle


def solve_puzzle(puzzle):
    sudoku = solver.Sudoku()

    if sudoku.get_input(puzzle) and sudoku.solve():
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

    time.sleep(tom_delay)

    # check for "Bring on another"
    sample = screen_grab(img_x, img_y + 50, 300, 300)
    if debug:
        print_img(sample, "send_to_tirth/bring_search")

    bring_x, bring_y = find_target_by_edges(target_bring_button, sample)
    if bring_x is not None:
        # found bring
        move(bring_x + img_x, bring_y + img_y + 50)
        left_click()
        time.sleep(tom_delay + 1)

    sample = screen_grab(img_x - 100, img_y - 100, 450, 500)
    if debug:
        print_img(sample, "send_to_tirth/next_sudoku")

    next_x, next_y, x_size, y_size = find_puzzle(target_img, sample)
    move(next_x + 5, next_y + 5)
    left_click()
    solve_puzzle(get_puzzle(screen_grab(next_x, next_y, x_size, y_size)))

    if runs > 0:
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

    img_x, img_y, x_size, y_size = find_puzzle(target_img, screen_grab())

    if img_x is None:
        if debug:
            print_img(screen_grab(), "send_to_tirth/no_joy")
        input("Couldn't find puzzle! Press the any key (it's enter) to exit")

    else:
        print("Found puzzle! Going to try", runs, "runs")

        # move(img_x + 5, img_y + 5)
        # left_click()

        if debug:
            print_img(screen_grab(img_x, img_y, x_size, y_size),
                      "send_to_tirth/initial_found_puzzle")

        get_puzzle(screen_grab(img_x, img_y, x_size, y_size))

        # next_puzzle(img_x, img_y)

        input("\nIronically, press enter to exit")  # to keep prompt open