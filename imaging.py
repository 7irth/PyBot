__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import os
from re import finditer
from PIL import Image, ImageOps, ImageGrab, ImageChops
from windows import *
from subprocess import Popen, PIPE

# location of tesseract command
tesseract = 'tesseract'


def screen_grab(x=0, y=0, x_size=screen_size()[0], y_size=screen_size()[1]):
    return ImageGrab.grab((x, y, x + x_size, y + y_size))


def print_img(image, description=str(int(time.time())), kind='PNG'):
    # make sure required folders exist
    folders = [-1] + [found.start() for found in finditer('/', description)]
    for i in range(len(folders) - 1):
        os.makedirs(description[folders[i] + 1:folders[i + 1]], exist_ok=True)

    image.save(os.getcwd() + '\\' + description + '.' + kind.lower(), kind)


# unstable
def signature(image):
    return sum([sum(pair) for pair in ImageOps.grayscale(image).getcolors()])


def equal_images(uno, dos):
    return ImageChops.difference(uno, dos).getbbox() is None


def close_enough(pix1, pix2, tolerance=2):
    if pix1 == pix2:
        return True

    elif tolerance != 0:
        for sub_pixel in range(len(pix1)):
            if not (abs(pix1[sub_pixel] - pix2[sub_pixel]) < tolerance):
                break
        else:
            return True

    return False


# default to single line of text without restrictions
def tesser(image, mode='7', restriction=''):
    print_img(image, 'temp_img')

    # assemble tesseract command
    command = [tesseract, 'temp_img.png', 'temp', '-psm', mode, restriction]

    # punch it
    tess = Popen(command, stdout=PIPE, stderr=PIPE)

    outs, errs = tess.communicate()

    # return results and clean up
    try:
        if tess.returncode == 0:
            with open('temp.txt', 'r') as f:
                result = f.read().strip()
            os.remove(f.name)
            return result
        else:
            print(errs)
    finally:
        os.remove('temp_img.png')


def find_buttons(sample_in=screen_grab()):
    buttons = {}

    min_width = 20
    max_height = 30

    s_width, s_height = sample_in.size
    sample = sample_in.load()

    # chrome button colours
    top_corner = (219, 219, 220)
    top_border = (163, 163, 163)
    bot_border = (148, 148, 148)  # gradient

    for y in range(s_height):
        for x in range(s_width):
            if close_enough(sample[x, y], top_corner, 2):  # corner pixel match
                width, height = 0, 0
                test_x, test_y = x + 1, y  # add one to compensate for colour

                # check width
                while close_enough(sample[test_x, y], top_border, 3):
                    width += 1
                    test_x += 1

                    # prevent cut off buttons from causing IndexError
                    if test_x == s_width:
                        return buttons

                if width > min_width:
                    # check height
                    while not close_enough(sample[x + 1, test_y], bot_border) \
                            and height < max_height:
                        height += 1
                        test_y += 1

                    if height < max_height:
                        read_button = (x + 1, y + 1, x + width, y + height)

                        # read button and add coordinates to dict
                        buttons[tesser(sample_in.crop(read_button))] = \
                            (x, y, width, height)
    return buttons


def find_target_by_edges(target_in, sample_in=screen_grab()):
    t_width, t_height = target_in.size
    s_width, s_height = sample_in.size

    target = target_in.load()
    sample = sample_in.load()

    for y in range(s_height):
        for x in range(s_width):
            if close_enough(sample[x, y], target[0, 0], 1):  # first pixel

                for column in range(t_width):
                    if not close_enough(sample[x + column, y],
                                        target[column, 0]):
                        break

                else:  # top row match

                    for row in range(t_height):
                        if not close_enough(sample[x, y + row],
                                            target[0, row]):
                            break

                    else:  # first column match

                        return x, y
    return None, None


if __name__ == "__main__":
    print(signature(Image.open('test_images/bring_search.png')))