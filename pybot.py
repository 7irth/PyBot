__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

from PIL import Image, ImageGrab, ImageOps
import os
import time
import win32api as windows
import win32con
from numpy import *

# magic numbers for running itself
box = (613, 55, 120, 24)
target_cords = (box[0] + 108, box[1] + 13)

target_image = Image.open("run_match.png")


def screen_grab(x=0, y=0, x_size=1920, y_size=1080):
    image = ImageGrab.grab((x, y, x + x_size, y + y_size))
    return image


def print_img(image):
    image.save(os.getcwd() + '\\screenshot_' +
               str(int(time.time())) + '.png', 'PNG')


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


def find_target(image):
    pass


def get_signature(image):
    print(image.getpixel((0, 0)))
    print(image.tostring())
    values = ImageOps.grayscale(image).getcolors()
    return sum(values)


if __name__ == '__main__':
    time.sleep(3)
    # got = screen_grab(632, 364, 960, 24)
    runner = screen_grab(600, 50, 150, 50)

    things = []
    r = runner.load()
    for x in range(150):
        for y in range(50):
            things.append(r[x, y])

    other_things = []
    q = target_image.load()
    for x in range(120):
        for y in range(24):
            other_things.append(q[x, y])

    print(things)
    print("FIND ME")
    print(other_things)