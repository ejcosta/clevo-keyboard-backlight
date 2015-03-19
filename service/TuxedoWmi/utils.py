__author__ = 'ejcosta'

from threading import Thread
import time


def percent_to_kb_color(percent, thresholds):
    if percent <= thresholds[0]:
        return 'green'
    if thresholds[0] < percent < thresholds[1]:
        return 'yellow'
    if percent >= thresholds[1]:
        return 'red'


class KeyboardDimThread(Thread):

    wake_up_flag = False
    initial_brightness = 10

    def __init__(self, dim_delay, kb_driver):
        Thread.__init__(self)
        self.dim_delay = int(dim_delay)
        self.kb_driver = kb_driver
        self.initial_brightness = self.kb_driver.get_brightness()

    def run(self):
        try:
            for x in xrange(self.dim_delay, -1, -1):
                if x == 0:
                    break
                if self.wake_up_flag:
                    break
                brightness = self.kb_driver.get_brightness()
                if brightness > x:
                    self.kb_driver.set_brightness(x)
                time.sleep(1)
            if not self.wake_up_flag:
                self.kb_driver.set_state_off(True)
        except:
            self.kb_driver.set_brightness(self.initial_brightness)

    def wake_up(self):
        self.wake_up_flag = True