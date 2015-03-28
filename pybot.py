import collections

__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import os
from windows import *
import numpy as np
from PIL import Image, ImageGrab, ImageOps
import solver

start, middle, end = 0, 0, 0  # for timing


def screen_grab(x=0, y=0, x_size=1920, y_size=1080):
    return ImageGrab.grab((x, y, x + x_size, y + y_size))


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
                s = column + current_pix
                t = column
                if not (np.all(sample[s] == target[t])):
                    break

            else:  # top row match

                for row in range(t_height):
                    s = row * s_width + current_pix
                    t = row * t_width

                    if not (np.all(sample[s] == target[t])):
                        break

                else:  # first column match

                    # TODO: make this work
                    for row in range(1, t_height):
                        for column in range(1, t_width):
                            s = row * s_width + column + current_pix
                            t = row * t_width + column

                            if not (np.all(sample[s] == target[t])):
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
    loaded = sudoku.load()

    # magic numbers for character recognition
    numbers = collections.OrderedDict()
    numbers[(9, 22, 15)] = []
    numbers[(6, 12, 17)] = []
    numbers[(4, 12, 19)] = []
    numbers[(8, 13, 20)] = []
    numbers[(5, 14, 14)] = []
    numbers[(7, 22, 9)] = []
    numbers[(2, 12, 13)] = []
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
        raise Exception("Couldn't solve!")


def submit_puzzle(solved):
    for number in solved:
        press(str(number), 'tab', delay=0.005)

    # move to and hit submit button
    press('tab', 'tab', 'tab', 'enter')


if __name__ == '__main__':
    target_img = Image.open("images/sudoku.png")
    # solve_puzzle(get_puzzle(target_img))

    curr = find_target(target_img)
    print("data prep", str(round(middle - start, 5)))
    print("actual search", str(round(end - middle, 5)))

    move(curr[0] + 5, curr[1] + 5)
    left_click()

    solve_puzzle(get_puzzle(screen_grab(curr[0], curr[1], 302, 299)))