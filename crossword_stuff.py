__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import crossword_solver
import pybot
from windows import *
from imaging import *


# returns coordinates and size of puzzle
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

            if sample[x, y] == init_pixel:  # first pixel match
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

    initial_search = screen_grab()
    with pybot.Timer('finding the crossword'):
        x, y, x_size, y_size = find_puzzle()

    if x is None:
        if pybot.debug:
            print_img(initial_search, "send_to_tirth/no_joy")
        input("Couldn't find puzzle! Press the any key (it's enter) to exit")

    else:
        # getting crossword answers
        across, down = crossword_solver.read_guardian_puzzle('crossword.txt')
        crossword = crossword_solver.Crossword(cells, across, down,
                                               'answers.json')
        crossword.fill_answers()

        first = crossword.clues[0]

        move(x + first.col * cell_size + cell_size // 2,
             y + first.row * cell_size + cell_size // 2)
        left_click()
        left_click()

        submit_crossword(crossword.answers)


if __name__ == '__main__':
    go()