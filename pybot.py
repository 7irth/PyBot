__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import os
from windows import *
import numpy as np
from PIL import Image, ImageGrab, ImageOps


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
    answer = 0

    sample = np.array(sample_in.getdata())
    s_width, s_height = sample_in.size

    target = np.array(target_in.getdata())
    t_width, t_height = target_in.size

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

                    for row in range(1, t_height):
                        for column in range(1, t_width):
                            sample_loc = row * s_width + column + current_pix
                            target_loc = row * t_width + column

                            if not (
                                    np.all(sample[sample_loc] == target[
                                        target_loc])):
                                break

                    else:  # full match
                        answer = current_pix
                        break

    start_pos = (answer % s_width, answer // s_width)
                        
    if debug:
        print(answer)
        print(start_pos)
        print_img(target_in, "target")
        print_img(sample_in, "input")
        print_img(
            sample_in.crop((start_pos[0], start_pos[1], start_pos[0] + t_width,
                            start_pos[1] + t_height)), "found")

    return start_pos


if __name__ == '__main__':
    # time.sleep(3)
    target_img = Image.open("home.png")

    random_target = screen_grab(np.random.randint(10, 1500),
                                np.random.randint(10, 800),
                                np.random.randint(5, 200),
                                np.random.randint(5, 200))

    move(find_target(target_img))
    left_click()