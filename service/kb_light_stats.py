#!/usr/bin/env python

__author__ = 'ejcosta'
__service_name__ = 'kb_light_stats'

import grp
import signal
import daemon
from lockfile import pidlockfile
from service_handler import (
    initial_program_setup,
    do_main_program,
    program_cleanup,
    )

pidfile = pidlockfile.PIDLockFile("/var/run/{}.pid".format(__service_name__))
context = daemon.DaemonContext(
    working_directory="/var/lib/{}".format(__service_name__),
    umask=0o002,
    pidfile=pidfile,
    )

context.signal_map = {signal.SIGTERM: program_cleanup}
context.gid = grp.getgrnam('root').gr_gid

config_file = open("/etc/{0}/{0}.conf".format(__service_name__), 'r')
context.files_preserve = [config_file]

initial_program_setup(config_file)

with context:
    do_main_program()