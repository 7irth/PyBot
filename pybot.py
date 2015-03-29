__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import os
from windows import *
import numpy as np
from PIL import Image, ImageGrab, ImageOps, ImageChops
import solver
from collections import OrderedDict

start, middle, end = 0, 0, 0  # for timing
runs = 3


# EMBEDDED IMAGE FILES

# import base64
#
# encoded_puzzle = ''
# puzzle_target = base64.b64decode(encoded_puzzle)
# target_img = Image.frombytes('RGB', (302, 299), puzzle_target)
target_img = Image.open("images/sudoku.png")

# encoded_bring = ''
# bring_target = base64.b64decode(encoded_bring)
# target_bring_button = Image.frombytes('RGB', (80, 20), bring_target)
target_bring_button = Image.open("images/bring_button.png")

# encoded_how = ''
# how_target = base64.b64decode(encoded_how)
# target_how_button = Image.frombytes('RGB', (50, 15), how_target)
# target_how_button = Image.open('images/how_button.png')


def screen_grab(x=0, y=0, x_size=screen_size()[0], y_size=screen_size()[1]):
    return ImageGrab.grab((x, y, x + x_size, y + y_size))


def print_img(image, description=str(int(time.time()))):
    image.save(os.getcwd() + '\\' + description + '.png', 'PNG')


def print_img_jpg(image, description=str(int(time.time()))):
    image.save(os.getcwd() + '\\' + description + '.jpg', 'JPEG')


def grab(x=0, y=0, x_size=1920, y_size=1080):
    image = ImageOps.grayscale(ImageGrab.grab((x, y, x + x_size, y + y_size)))
    colours = image.getcolors()

    return colours


def equal_images(uno, dos):
    return ImageChops.difference(uno, dos).getbbox() is None


def get_signature(image):
    print(image.getpixel((0, 0)))
    print(image.tostring())
    values = ImageOps.grayscale(image).getcolors()
    return sum(values)


def open_chrome():
    time.sleep(1)

    press("winkey")

    time.sleep(1)

    enter_phrase("chrome")
    press("enter")

    time.sleep(1)

    press_hold_release("ctrl", "t")
    enter_phrase("websudoku.com")
    press("enter")
    # press_hold_release("winkey", "up_arrow")

    time.sleep(5)


# takes ~1.7 seconds to turn target and sample into searchable arrays,
#       ~12 seconds to search the whole thing unsuccessfully
def find_target(target_in, sample_in=screen_grab(), debug=False):
    # print_img(sample_in, "current")
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


# takes ~1 second for full search
def find_target_redux(target_in, sample_in=screen_grab()):
    global start, middle, end
    start = time.time()

    t_width, t_height = target_in.size

    l_target = target_in.load()
    l_sample = sample_in.load()

    middle = time.time()

    for y in range(sample_in.size[1]):
        for x in range(sample_in.size[0]):
            if l_sample[x, y] == l_target[0, 0]:  # first pixel match

                for column in range(t_width):
                    if not (l_sample[x + column, y] == l_target[column, 0]):
                        break

                else:  # top row match

                    for row in range(t_height):
                        if not (l_sample[x, y + row] == l_target[0, row]):
                            break

                    else:  # first column match

                        return x, y

    end = time.time()
    return None


def get_puzzle(sudoku):
    loaded = sudoku.load()

    # magic numbers for character recognition
    numbers = OrderedDict()
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
        # refresh and try again
        raise Exception("Couldn't solve!")


def submit_puzzle(solved):
    for number in solved:
        press(str(number), 'tab', delay=0.005)

    press_hold_release('shift', 'tab')
    press('enter')


def next_puzzle(puzzle_pos):
    global runs
    runs -= 1

    time.sleep(1)

    # print(puzzle_pos)

    # sample from left of puzzle and down for "How am I doing?"
    # sample = screen_grab(puzzle_pos[0] - 100,
    # puzzle_pos[1] + 300, 210, 125)
    # print_img(sample, "test_images/how_search")
    #
    # how_pos = find_target_redux(target_how_button, sample)
    #
    # if how_pos == (0, 0):
    #     raise Exception("Couldn't find next button")
    #
    # move(how_pos[0] + puzzle_pos[0] - 100, how_pos[1] + puzzle_pos[1] + 300)
    # left_click()  # next puzzle
    #
    # time.sleep(1.5)

    # check for "Bring on another"
    sample = screen_grab(puzzle_pos[0], puzzle_pos[1] + 50, 300, 300)
    # print_img(sample, "test_images/bring_search")

    bring_another = find_target_redux(target_bring_button, sample)
    if bring_another != (0, 0):
        # found bring
        move(bring_another[0] + puzzle_pos[0],
             bring_another[1] + puzzle_pos[1] + 50)
        left_click()
        time.sleep(1)

    sample = screen_grab(puzzle_pos[0] - 100, puzzle_pos[1] - 100, 450, 500)
    # print_img(sample, "test_images/next_sudoku")
    next_pos = find_target_redux(target_img, sample)
    # print(next_pos)
    current = (next_pos[0] + puzzle_pos[0] - 100,
               next_pos[1] + puzzle_pos[1] - 100)
    move(current[0] + 5, current[1] + 5)
    left_click()
    solve_puzzle(get_puzzle(screen_grab(current[0], current[1], 302, 299)))

    if runs > 0:
        print(runs, "runs" if runs > 1 else "run", "left")
        next_puzzle(current)
    else:
        print("You get the point")


if __name__ == '__main__':
    open_chrome()

    found = find_target_redux(target_img, screen_grab())

    if found is None:
        raise Exception("Couldn't find puzzle!")

    else:
        print("Found puzzle! Going to try", runs, "runs")

        move(found[0] + 5, found[1] + 5)
        left_click()

        solve_puzzle(get_puzzle(screen_grab(found[0], found[1], 302, 299)))

        next_puzzle(found)

        input()