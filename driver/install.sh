#!/usr/bin/env bash

make
make install
# uncomment this line if make install gets error
#cp tuxedo-wmi.ko /lib/modules/`uname -r`/extra/
depmod -a
echo "tuxedo-wmi" >> /etc/modules
modprobe tuxedo-wmi
