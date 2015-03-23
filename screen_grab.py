__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

from PIL import ImageGrab
import os
import time


def screen_grab(x=0, y=0, x_size=1920, y_size=1080):
    image = ImageGrab.grab((x, y, x + x_size, y + y_size))
    image.save(os.getcwd() + '\\screenshot_' +
               str(int(time.time())) + '.png', 'PNG')


if __name__ == '__main__':
    screen_grab()