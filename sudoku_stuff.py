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


def get_puzzle(sudoku):
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
                x = number[1] + 33 * col
                y = number[2] + 33 * row

                if col > 2:
                    x += 1

                if col > 5:
                    x += 1

                if (row, col) not in got and (loaded[x, y] != (255, 255, 255)):
                    numbers[number].append((row, col))
                    got.append((row, col))
    return numbers


def solve_puzzle(given):
    sudoku = solver.Sudoku()
    puzzle = [0 for _ in range(81)]

    for n in given:
        for thing in given[n]:
            puzzle[thing[0] * 9 + thing[1]] = n[0]

    if sudoku.get_input(puzzle) and sudoku.solve():
        submit_puzzle([number for row in sudoku.sudoku for number in row])
    else:
        # refresh and try again
        print("Couldn't solve puzzle :(")


def submit_puzzle(solved):
    for number in solved:
        press(str(number), 'tab', delay=0.005)

    press_hold_release('shift', 'tab')
    press('enter')


def next_puzzle(puzzle_pos):
    global runs
    runs -= 1

    time.sleep(tom_delay)

    # check for "Bring on another"
    sample = screen_grab(puzzle_pos[0], puzzle_pos[1] + 50, 300, 300)
    if debug:
        print_img(sample, "send_to_tirth/bring_search")

    bring_location = find_target_redux(target_bring_button, sample)
    if bring_location != (0, 0):
        # found bring
        move(bring_location[0] + puzzle_pos[0],
             bring_location[1] + puzzle_pos[1] + 50)
        left_click()
        time.sleep(tom_delay + 1)

    sample = screen_grab(puzzle_pos[0] - 100, puzzle_pos[1] - 100, 450, 500)
    if debug:
        print_img(sample, "send_to_tirth/next_sudoku")

    next_pos = find_target_redux(target_img, sample)
    current = (next_pos[0] + puzzle_pos[0] - 100,
               next_pos[1] + puzzle_pos[1] - 100)
    move(current[0] + 5, current[1] + 5)
    left_click()
    solve_puzzle(get_puzzle(screen_grab(current[0], current[1], 302, 299)))

    if runs > 0:
        print(runs, "runs" if runs > 1 else "run", "left")
        next_puzzle(current)
    else:
        # press_hold_release("winkey", "down_arrow")
        # press_hold_release("winkey", "down_arrow")
        print("You get the point")


def go():
    global runs
    runs = int(float(input("Runs through the puzzle (try at least 2): ")))

    print("Please don't move the mouse while the bot is working\n")
    time.sleep(tom_delay)

    # open_sudoku_on_chrome()

    img_loc = find_target_redux(target_img, screen_grab())

    if img_loc is None:
        if debug:
            print_img(screen_grab(), "send_to_tirth/no_joy")
        input("Couldn't find puzzle! Press the any key (it's enter) to exit")
    
    else:
        print("Found puzzle! Going to try", runs, "runs")
    
        move(img_loc[0] + 5, img_loc[1] + 5)
        left_click()
    
        if debug:
            print_img(screen_grab(img_loc[0], img_loc[1], 302, 299),
                      "send_to_tirth/initial_found_puzzle")
    
        solve_puzzle(get_puzzle(
            screen_grab(img_loc[0], img_loc[1], 302, 299)))
    
        next_puzzle(img_loc)
    
        input("\nIronically, press enter to exit")  # to keep prompt open