__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

from PIL import Image, ImageGrab, ImageOps
import os
import time
import win32api as windows
import win32con
import numpy as np

# magic numbers for running itself
box = (613, 55, 120, 24)
target_cords = (box[0] + 108, box[1] + 13)


def screen_grab(x=0, y=0, x_size=1920, y_size=1080):
    image = ImageGrab.grab((x, y, x + x_size, y + y_size))
    return image


def print_img(image, description=str(int(time.time()))):
    image.save(os.getcwd() + '\\' + description + '.png', 'PNG')


def grab(x=0, y=0, x_size=1920, y_size=1080):
    image = ImageOps.grayscale(ImageGrab.grab((x, y, x + x_size, y + y_size)))
    colours = image.getcolors()

    return colours


def scroll_up(amount):
    windows.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, amount)


def scroll_down(amount):
    windows.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -amount)


def left_click(delay=0.1):
    left_down()
    time.sleep(delay)
    left_up()


def right_click(delay=0.1):
    left_down()
    time.sleep(delay)
    right_up()


def left_down(x=0, y=0, delay=0.1):
    windows.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
    time.sleep(delay)


def left_up(x=0, y=0, delay=0.1):
    windows.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y)
    time.sleep(delay)


def right_down(x=0, y=0, delay=0.1):
    windows.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y)
    time.sleep(delay)


def right_up(x=0, y=0, delay=0.1):
    windows.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y)
    time.sleep(delay)


def move(coordinates):
    windows.SetCursorPos(coordinates)


def current_position():
    return windows.GetCursorPos()


def start(delay=5):
    move(target_cords)
    left_click()
    time.sleep(delay)


def find_target(target_in, sample_in=screen_grab()):
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
                # print("top row match at", current_pix)

                for row in range(t_height):
                    sample_loc = row * s_width + current_pix
                    target_loc = row * t_width

                    if not (np.all(sample[sample_loc] == target[target_loc])):
                        break

                else:  # first column match
                    # print("first column match at", current_pix)

                    for row in range(1, t_height):
                        for column in range(1, t_width):
                            sample_loc = row * s_width + column + current_pix
                            target_loc = row * t_width + column

                            if not (
                                    np.all(sample[sample_loc] == target[
                                        target_loc])):
                                break

                    else:  # full match
                        # print("full match at", current_pix)
                        answer = current_pix
                        break

    print(answer)
    answer = (answer % s_width, answer // s_width)
    print(answer)

    print_img(target_in, "tar")
    print_img(sample_in, "input")
    print_img(sample_in.crop((answer[0], answer[1], answer[0] + t_width,
                              answer[1] + t_height)), "input_c")


def get_signature(image):
    print(image.getpixel((0, 0)))
    print(image.tostring())
    values = ImageOps.grayscale(image).getcolors()
    return sum(values)


if __name__ == '__main__':
    # time.sleep(3)
    target_img = Image.open("run_match.png")
    sample_img = Image.open("runner.png")

    # runner = screen_grab(600, 50, 150, 50)
    # got = screen_grab(632, 364, 960, 24)

    random_target = screen_grab(np.random.randint(10, 1500),
                                np.random.randint(10, 800),
                                np.random.randint(5, 200),
                                np.random.randint(5, 200))

    find_target(random_target)