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

target_image = Image.open("match.png")


def screen_grab(x=0, y=0, x_size=1920, y_size=1080):
    image = ImageGrab.grab((x, y, x + x_size, y + y_size))
    image.save(os.getcwd() + '\\screenshot_' +
               str(int(time.time())) + '.png', 'PNG')
    return image


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
    colours = ImageOps.grayscale(image).getcolors()
    return sum(colours)


if __name__ == '__main__':
    # print(get_signature(target_image))
    t_sig = get_signature(target_image)
    print(t_sig)
    print(get_signature(Image.open("Capture1.PNG")))
    print(get_signature(screen_grab(1114, 373, 960, 24)))