__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

from PIL import ImageGrab
import os
import time
import win32api as windows
import win32con


def screen_grab(x=0, y=0, x_size=1920, y_size=1080):
    image = ImageGrab.grab((x, y, x + x_size, y + y_size))
    image.save(os.getcwd() + '\\screenshot_' +
               str(int(time.time())) + '.png', 'PNG')


def scroll_up():
    windows.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 100)


def left_click():
    windows.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    windows.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


if __name__ == '__main__':
    left_click()