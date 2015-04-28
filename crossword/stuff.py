__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import pybot
import crossword as c
from utils.windows import *
from utils.imaging import *
from os import path
from re import findall


def open_guardian_on_chrome(numb=None):
    press('winkey')
    pybot.chill_out_for_a_bit()

    enter_phrase('google chrome')
    press('enter')
    pybot.chill_out_for_a_bit()

    press_hold_release('ctrl', 't')
    pybot.chill_out_for_a_bit()

    enter_phrase('theguardian.com/crosswords/' +
                 (('quick/' + numb) if numb else 'series/quick'), delay=.01)
    press('enter')


# return coordinates and size of puzzle
def find_puzzle(sample_in=screen_grab()):
    columns, rows = sample_in.size

    min_x_size, min_y_size = 200, 200
    init_pixel = (17, 17, 17)
    other_pixel = (0, 0, 0)

    sample = sample_in.load()

    x, y = -1, -1

    while y + 1 < rows:
        y += 1  # next row
        x = -1  # reset column

        while x + 1 < columns:
            x += 1  # next column

            if sample[x, y] == init_pixel or sample[x, y] == other_pixel:
                first_x, first_y = int(x), int(y)

                while (sample[x + 1, y] == init_pixel or
                               sample[x + 1, y] == other_pixel):  # check row
                    x += 1

                while (sample[x, y + 1] == init_pixel or
                               sample[x, y + 1] == other_pixel):  # check col
                    y += 1

                size = x - first_x + 1, y - first_y + 1

                if size > (min_x_size, min_y_size):
                    return first_x, first_y, size[0], size[1]

    return None, None, None, None


def submit_crossword(solved):
    for answer in solved:
        for letter in answer:
            press(letter, delay=0.01)
        press('tab')


def go():
    cells = 13
    cell_size = 28

    # open_guardian_on_chrome()

    entered = input('Enter a Guardian Quick crossword No ')

    if entered == 'test':
        sample_puzzle = path.realpath('') + '\\crossword.txt'
        sample_answers = path.realpath('') + '\\answers.json'

        open_guardian_on_chrome('14022')
        pybot.chill_out_for_a_bit(2)

        across, down = c.solver.read_guardian_puzzle(sample_puzzle)
        puzzle = c.solver.Crossword(cells, across, down, sample_answers)
    else:
        found = False
        while not found:
            if len(findall(r'^\d+$', entered)) != 1:
                entered = input('Try again: ')
            else:
                try:
                    across, down = c.solver.get_guardian(entered)
                    puzzle = c.solver.Crossword(cells, across, down)
                    found = True
                except c.solver.PuzzleNotFound:
                    entered = input('Couldn\'t find that one, try again: ')

    with pybot.Timer('solving the crossword'):
        while not puzzle.fill_answers():
            puzzle.fill_clues(None, None, True)  # reset and shuffle

    if pybot.debug:
        print(puzzle.answers)

    with pybot.Timer('finding the crossword'):
        # press_hold_release('winkey', 'down_arrow')
        pybot.chill_out_for_a_bit(1)
        initial_search = screen_grab()
        # press_hold_release('alt', 'esc')
        # press_hold_release('winkey', 'up_arrow')

        x, y, x_size, y_size = find_puzzle(initial_search)

    if x is None:
        if pybot.debug:
            print_img(initial_search, 'send_to_tirth/no_joy')
        input("Couldn't find puzzle! Press the any key (it's enter) to exit")

    else:
        move(x + puzzle.first_clue.col * cell_size + cell_size // 2,
             y + puzzle.first_clue.row * cell_size + cell_size // 2)
        left_click(); sleep(0.01); left_click()  # select across

        submit_crossword(puzzle.answers)


if __name__ == '__main__':
    go()
    # print(find_buttons())
    # import math
    #
    # for x in range(10, 500):
    #     y = int(round((math.sin(x / 10) * 100 + 500), 0))
    #     move(x, y)
    #     sleep(0.015)