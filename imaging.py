__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

from PIL import Image, ImageOps, ImageGrab, ImageChops
import os
from windows import *
# import numpy as np
import time
from subprocess import Popen, PIPE

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


def print_img(image, description=str(int(time.time())), kind='PNG'):
    image.save(os.getcwd() + '\\' + description + '.' + kind.lower(), kind)


def grab(x=0, y=0, x_size=1920, y_size=1080):
    image = ImageOps.grayscale(ImageGrab.grab((x, y, x + x_size, y + y_size)))
    colours = image.getcolors()

    return colours


def equal_images(uno, dos):
    return ImageChops.difference(uno, dos).getbbox() is None


def close_enough(pix1, pix2, tolerance=2):
    if pix1 == pix2:
        return True

    elif tolerance != 0:
        for sub in range(3):
            if not (abs(pix1[sub] - pix2[sub]) < tolerance):
                break
        else:
            return True

    return False


def get_signature(image):
    print(image.getpixel((0, 0)))
    print(image.tostring())
    values = ImageOps.grayscale(image).getcolors()
    return sum(values)


def tesseract(image):
    print_img(image, 'temp_img')

    # run tesseract with given image
    tess = Popen([os.getcwd() + '\\libs\\tesseract',
                  'temp_img.png', 'temp'],
                 stdout=PIPE, stderr=PIPE)

    outs, errs = tess.communicate()

    # return results and clean up
    try:
        if tess.returncode == 0:
            with open('temp.txt', 'r') as f:
                result = f.read()
            os.remove(f.name)
            return result
        else:
            print(errs)
    finally:
        os.remove('temp_img.png')

# takes ~1.7 seconds to turn target and sample into searchable arrays,
#       ~12 seconds to search the whole thing unsuccessfully
# def find_target(target_in, sample_in=screen_grab(), debug=False):
#     answer = 0
#
#     sample = np.array(sample_in.getdata())
#     s_width, s_height = sample_in.size
#
#     target = np.array(target_in.getdata())
#     t_width, t_height = target_in.size
#
#     # go through all pixels in sample image
#     for current_pix in range(0, sample.shape[0]):
#
#         if np.all(sample[current_pix] == target[0]):  # first pixel match
#             for column in range(t_width):
#                 s = column + current_pix
#                 t = column
#                 if not (np.all(sample[s] == target[t])):
#                     break
#
#             else:  # top row match
#
#                 for row in range(t_height):
#                     s = row * s_width + current_pix
#                     t = row * t_width
#
#                     if not (np.all(sample[s] == target[t])):
#                         break
#
#                 else:  # first column match
#
#                     # TODO: make this work
#                     for row in range(1, t_height):
#                         for column in range(1, t_width):
#                             s = row * s_width + column + current_pix
#                             t = row * t_width + column
#
#                             if not (np.all(sample[s] == target[t])):
#                                 break
#
#                     else:  # full match
#                         answer = current_pix
#                         break
#
#     start_pos = (answer % s_width, answer // s_width)
#
#     if debug:
#         print(answer)
#         print(start_pos)
#         print_img(target_in, "target")
#         print_img(sample_in, "input")
#         print_img(
#             sample_in.crop((start_pos[0], start_pos[1],
#                             start_pos[0] + t_width,
#                             start_pos[1] + t_height)), "found")
#
#     return start_pos


# takes ~1 second for full search
def find_target_redux(target_in, sample_in=screen_grab()):
    t_width, t_height = target_in.size
    s_width, s_height = sample_in.size

    l_target = target_in.load()
    l_sample = sample_in.load()

    for y in range(s_height):
        for x in range(s_width):
            if close_enough(l_sample[x, y], l_target[0, 0], 1):  # first pixel

                for column in range(t_width):
                    if not close_enough(l_sample[x + column, y],
                                        l_target[column, 0]):
                        break

                else:  # top row match

                    for row in range(t_height):
                        if not close_enough(l_sample[x, y + row],
                                            l_target[0, row]):
                            break

                    else:  # first column match

                        return x, y
    return None


if __name__ == "__main__":
    a = Image.open('test_images\how_search.png')

    print(tesseract(a))