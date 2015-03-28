__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import win32api as windows
import win32con
import time


# WINDOWS FUNCTIONS
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


def type_something():
    windows.keybd_event(ord('a'), 0, 0, 0)
