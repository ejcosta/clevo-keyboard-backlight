__author__ = 'ejcosta'

import psutil


def get_mem_usage():
    return psutil.virtual_memory().percent


def print_mem_usage():
    print("Memory Percent: {}".format(get_mem_usage()))

if __name__ == "__main__":
    print_mem_usage()