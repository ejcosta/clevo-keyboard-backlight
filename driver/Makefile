obj-m += tuxedo-wmi.o
#CFLAGS_tuxedo-wmi.o := -DDEBUG
#KDIR := /lib/modules/$(shell uname -r)/build
KDIR := /lib/modules/$(shell pacman -Q linux | cut -f 2 -d " " | sed 's/\.arch/-arch/g')/build
PWD := $(shell pwd)

all:
	make -C $(KDIR) M=$(PWD) modules

install:
	make -C $(KDIR) M=$(PWD) modules_install

clean:
	make -C $(KDIR) M=$(PWD) clean
