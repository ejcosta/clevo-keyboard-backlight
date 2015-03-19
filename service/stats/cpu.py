__author__ = 'ejcosta'

import psutil


def get_cpu_load():
    return psutil.cpu_percent(interval=1)


def print_cpu_load():
    print("CPU Percent: {}".format(get_cpu_load()))

if __name__ == "__main__":
    print_cpu_load()