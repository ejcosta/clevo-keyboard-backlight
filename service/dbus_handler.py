__author__ = 'ejcosta'

import dbus
from TuxedoWmi.utils import KeyboardDimThread


def register_signal_watch(lp, cfg, kb_dvr):
    global bus, config, kb_driver, loop, session, dim_thread

    loop = lp
    config = cfg
    kb_driver = kb_dvr
    bus_name = "org.freedesktop.login1"
    bus = dbus.SystemBus()
    dim_thread = KeyboardDimThread(config.get('service', 'dim_delay', 10), kb_driver)

    # Register signal handler for org.freedesktop.DBus.Properties.PropertiesChanged event.
    # (for details see http://dbus.freedesktop.org/doc/dbus-specification.html#standard-interfaces-properties)
    bus.add_signal_receiver(signal_handler,
                            signal_name='PropertiesChanged',
                            dbus_interface="org.freedesktop.DBus.Properties",
                            path="/org/freedesktop/login1")

    # Based on default seat we get active session in order to find his IdleHint parameter value.
    # This parameter changes between True and False based on session idle status.
    # (for details see http://www.freedesktop.org/wiki/Software/systemd/logind/)

    # Get default seat to find active session.
    # (on multi-seat configuration seat0 is always chosen)
    seat = bus.get_object(bus_name, "/org/freedesktop/login1/seat/seat0")

    # Session object active on default seat
    session = bus.get_object(bus_name, seat.Get('org.freedesktop.login1.Seat','ActiveSession')[1])

    # Launch dbus main loop
    loop.run()


def unregister_signal_watch():
    try:
        bus.remove_signal_receiver(signal_handler,
                                   dbus_interface="org.freedesktop.DBus.Properties",
                                   path="/org/freedesktop/login1")
    except:
        print "Exception on remove_signal_receiver!"


def signal_handler(*args, **kwargs):
    if 'IdleHint' in args[2]:
        if session.Get('org.freedesktop.login1.Session', 'IdleHint'):
            _dim_keyboard_lights()
        else:
            _power_up_keyboard_lights()


def _dim_keyboard_lights():
    global dim_thread
    dim_thread = KeyboardDimThread(config.get('service', 'dim_delay', 10), kb_driver)
    dim_thread.start()


def _power_up_keyboard_lights():
    dim_thread.wake_up()
    kb_driver.set_state_off(False)
    kb_driver.set_brightness(dim_thread.initial_brightness)


if __name__ == "__main__":
    import ConfigParser
    import TuxedoWmi
    from dbus.mainloop.glib import (DBusGMainLoop, threads_init)
    DBusGMainLoop(set_as_default=True)
    import gobject
    try:
        loop = gobject.MainLoop()
        config = ConfigParser.ConfigParser()
        config.readfp(open('kb_light_stats.conf', 'r'))
        kb_driver = TuxedoWmi.Keyboard("/sys/module/tuxedo_wmi/parameters/")
        register_signal_watch(loop, config, kb_driver)
    except KeyboardInterrupt:
        unregister_signal_watch()
