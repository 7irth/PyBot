import collections

__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import os
from windows import *
import numpy as np
from PIL import Image, ImageGrab, ImageOps
import solver

start, middle, end = 0, 0, 0  # for timing


class Timer:
    def __init__(self, label=''):
        self.label = label

    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
        log = ''
        if self.label:
            log += '\"{}\" '.format(self.label)
        else:
            log += 'Block '
        log += 'took ' + str(round(self.interval, 5)) + ' seconds'
        print(log)


def screen_grab(x=0, y=0, x_size=1920, y_size=1080):
    image = ImageGrab.grab((x, y, x + x_size, y + y_size))
    return image


def print_img(image, description=str(int(time.time()))):
    image.save(os.getcwd() + '\\' + description + '.png', 'PNG')


def grab(x=0, y=0, x_size=1920, y_size=1080):
    image = ImageOps.grayscale(ImageGrab.grab((x, y, x + x_size, y + y_size)))
    colours = image.getcolors()

    return colours


def get_signature(image):
    print(image.getpixel((0, 0)))
    print(image.tostring())
    values = ImageOps.grayscale(image).getcolors()
    return sum(values)


def find_target(target_in, sample_in=screen_grab(), debug=False):
    global start, middle, end

    start = time.clock()
    answer = 0

    sample = np.array(sample_in.getdata())
    s_width, s_height = sample_in.size

    target = np.array(target_in.getdata())
    t_width, t_height = target_in.size

    middle = time.clock()

    # go through all pixels in sample image
    for current_pix in range(0, sample.shape[0]):

        if np.all(sample[current_pix] == target[0]):  # first pixel match
            for column in range(t_width):
                sample_loc = column + current_pix
                target_loc = column
                if not (np.all(sample[sample_loc] == target[target_loc])):
                    break

            else:  # top row match

                for row in range(t_height):
                    sample_loc = row * s_width + current_pix
                    target_loc = row * t_width

                    if not (np.all(sample[sample_loc] == target[target_loc])):
                        break

                else:  # first column match

                    # TODO: make this work
                    for row in range(1, t_height):
                        for column in range(1, t_width):
                            sample_loc = row * s_width + column + current_pix
                            target_loc = row * t_width + column

                            if not (np.all(sample[sample_loc]
                                               == target[target_loc])):
                                break

                    else:  # full match
                        answer = current_pix
                        break

    start_pos = (answer % s_width, answer // s_width)

    end = time.clock()

    if debug:
        print(answer)
        print(start_pos)
        print_img(target_in, "target")
        print_img(sample_in, "input")
        print_img(
            sample_in.crop((start_pos[0], start_pos[1], start_pos[0] + t_width,
                            start_pos[1] + t_height)), "found")

    return start_pos


def get_puzzle(sudoku):
    a = sudoku.crop((2, 2, 34, 34))
    loaded = sudoku.load()
    # print(loaded[22, 12] != (255, 255, 255))
    # print(loaded[55, 12] != (255, 255, 255))
    # print(loaded[88, 12] != (255, 255, 255))
    # print(loaded[122, 12] != (255, 255, 255))
    # print(loaded[22, 78] != (255, 255, 255))

    # sample = np.array(sudoku.getdata())
    # s_width, s_height = sudoku.size
    #
    # print(s_width, s_height)
    # print(len(sample))

    other_got = collections.OrderedDict()
    other_got[(9, 22, 12)] = []
    other_got[(6, 12, 17)] = []
    other_got[(4, 12, 19)] = []
    other_got[(8, 13, 20)] = []
    other_got[(5, 14, 14)] = []
    other_got[(7, 22, 9)] = []
    other_got[(2, 12, 13)] = []
    other_got[(3, 13, 11)] = []
    other_got[(1, 15, 10)] = []

    bah = []

    for row in range(9):
        for col in range(9):
            for number in other_got:
                x = number[1] + 33 * col
                y = number[2] + 33 * row

                if col > 2:
                    x += 1

                if col > 5:
                    x += 1

                if (row, col) not in bah and (loaded[x, y] != (255, 255, 255)):
                    other_got[number].append((row, col))
                    bah.append((row, col))

    for thing in other_got:
        print(thing[0], other_got[thing])
    print(len(bah))

    # loaded[x, y] = (50, 0, 0)
    # sudoku.save(os.getcwd() + '\\' + "sudokut" + '.png', 'PNG')


if __name__ == '__main__':
    # test_sudoku = '003105060' \
    #               '000004008' \
    #               '060000507' \
    #               '056000000' \
    #               '094602150' \
    #               '000000620' \
    #               '509000040' \
    #               '600400000' \
    #               '040203900'

    # sudoku = solver.Sudoku()
    # sudoku.get_input(test_sudoku)
    # sudoku.solve()
    # print(sudoku.sudoku)

    target_img = Image.open("images/sudoku.png")
    get_puzzle(target_img)

    # random_target = screen_grab(np.random.randint(10, 1500),
    #                             np.random.randint(10, 800),
    #                             np.random.randint(5, 200),
    #                             np.random.randint(5, 200))

    # with Timer("search"):
    #     move(find_target(target_img))
    #     print("data prep", str(round(middle - start, 5)))
    #     print("actual search", str(round(end - middle, 5)))

    # type_something()

    # left_click()

    # print_img(screen_grab(1441, 411, 302, 299), "sudoku")
    # print(current_position())