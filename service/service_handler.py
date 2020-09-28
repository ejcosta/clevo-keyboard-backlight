__author__ = 'ejcosta'

import time
import ConfigParser
import TuxedoWmi
import threading
from dbus_handler import (
    register_signal_watch,
    unregister_signal_watch,
)
from stats import (
    cpu,
    memory,
    gpu
)
from TuxedoWmi.utils import percent_to_kb_color
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
import gobject


def initial_program_setup(config_file):
    global config, kb_driver, polling_interval, thresholds, def_color

    # Load config
    config = ConfigParser.ConfigParser()
    config.readfp(config_file)

    # Setup keyboard driver object
    kb_driver = TuxedoWmi.Keyboard(config.get('driver', 'location', "/sys/module/tuxedo_wmi/parameters/"))

    # Load polling interval used to sleep during main cycle
    polling_interval = config.get('service', 'polling_interval', 60)

    # Load thresholds used to define colors by percentage
    thresholds = [int(config.get('thresholds', 'green', 40)), int(config.get('thresholds', 'yellow', 60))]

    # Load default keyboard color
    def_color = config.get('service', 'def_color', 'blue')


def do_main_program():
    global dbus_thread, loop

    # Based on documentation:
    # This must be called before creating a second thread in a program that uses this module.
    gobject.threads_init()

    # Init dbus main loop
    loop = gobject.MainLoop()

    # Create and start thread responsible for power off/on keyboard lights on dbus events
    dbus_thread = threading.Thread(target=register_signal_watch, args=(loop, config, kb_driver))
    dbus_thread.daemon = True
    dbus_thread.start()

    # Main cycle
    while True:
        update_stats()
        try:
            time.sleep(int(polling_interval))
        except KeyboardInterrupt:
            unregister_signal_watch()
            loop.quit()
            break


def program_cleanup():
    kb_driver.set_colors({'left': def_color, 'center': def_color, 'right': def_color})


def update_stats():
    # CPU
    cpu_cfg = config.get('stats', 'cpu', '')
    if cpu_cfg in ('left', 'center', 'right'):
        kb_driver.set_colors({cpu_cfg: percent_to_kb_color(cpu.get_cpu_load(), thresholds)})

    # Memory
    memory_cfg = config.get('stats', 'memory', '')
    if memory_cfg in ('left', 'center', 'right'):
        kb_driver.set_colors({memory_cfg: percent_to_kb_color(memory.get_mem_usage(), thresholds)})

    # GPU
    gpu_cfg = config.get('stats', 'gpu', '')
    if gpu_cfg in ('left', 'center', 'right'):
        kb_driver.set_colors({gpu_cfg: percent_to_kb_color(gpu.get_gpu_load(), thresholds)})


if __name__ == "__main__":
        try:
            initial_program_setup(open('kb_light_stats.conf', 'r'))
            do_main_program()
        finally:
            program_cleanup()
