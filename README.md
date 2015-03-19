# clevo-keyboard-backlight

This is a bundle of TuxedoWmi driver for Clevo's keyboard with some additional extras. 
I've made some changes to kernel module in order to export parameters so you can control keyboard sectors and colors independently. 
A mix between [this][1] and [this][2]. 

*This was done for Ubuntu, feel free to adapt and test on other distros.*

Additionally I’ve done a simple service in python to explore keyboard's functionalities and give some useful feedback to user. This service runs in background and have this features:

 - Reads **CPU load** and based in this value, changes the color on one of keyboard's sector between green, yellow and red.
 - Reads **Memory usage** and based in this value, changes the color on one of keyboard's sector between green, yellow and red.
 - Detects display event of going idle and dims keyboard light gradually to zero till screen gets blank. On wakeup, keyboard's brightness is restored to its original value. *(this is done based on dbus events, see code for details)*


Code is divided in two parts (driver and service) in case you just want one of them.

## Installation
### Driver
Prior to install driver you probably need run this:
```sh
$ sudo apt-get update
$ sudo apt-get install git build-essential linux-source
```
Running "***driver/install.sh***" should be enough to get module compiled and running. This script is self-explanatory; compile kernel module, install and load. Additionally it adds an entry on "***/etc/modules***" to persist between restarts.

### Service
Prior to install service you need install some dependencies:
```sh
$ pip install -r service/requirements.txt
```
Run "***service/install.sh***" to copy app to "***/var/lib/kb_light_stats***" and config file to "***/etc/kb_light_stats/kb_light_stats.conf***".
Edit this config file to fit your needs.

### Todo's
 - Install python app as a service

Feel free to fork, change, discuss, etc.

[1]:http://askubuntu.com/questions/184593/reverse-engineer-driver-for-multi-colored-backlit-keyboard-on-clevo-laptops
[2]:http://www.linux-onlineshop.de/forum/index.php?page=Thread&threadID=26