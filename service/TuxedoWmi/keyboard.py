__author__ = 'ejcosta'

import os


class Keyboard(object):
    driver_location = ""
    driver_ok = False
    brightness = 10
    state_off = False
    colors_code = {
        'off':    '0',
        'blue':   '1',
        'red':    '2',
        'purple': '3',
        'green':  '4',
        'ice':    '5',
        'yellow': '6',
        'white':  '7',
        'aqua':   '8',
    }
    colors = {
        'left':   'blue',
        'center': 'blue',
        'right':  'blue'}

    def __init__(self, driver_location):
        self.driver_location = driver_location
        if not self.check_driver():
            return
        self.get_brightness()
        self.get_colors(["left", "center", "right"])

    def check_driver(self):
        self.driver_ok = os.path.isdir(self.driver_location)
        return self.driver_ok

    """ Getters """
    def get_brightness(self):
        if not self.driver_ok:
            return
        self.brightness = int(self.__get_kernel_param("kb_brightness"))
        return int(self.brightness)

    def get_state_off(self):
        if not self.driver_ok:
            return
        self.state_off = bool(int(self.__get_kernel_param("kb_off")))
        return self.state_off

    def get_colors(self, kb_sections):
        if not self.driver_ok:
            return
        for section in kb_sections:
            if section in self.colors:
                self.colors[section] = self.colors_code.keys()[self.colors_code.values()
                    .index(self.__get_kernel_param("kb_{}".format(section)))]
        return self.colors

    """ Setters """
    def set_brightness(self, val):
        if not self.driver_ok:
            return
        self.__set_kernel_param("kb_brightness", str(val))
        return self.get_brightness()

    def set_state_off(self, val):
        if not self.driver_ok:
            return
        self.__set_kernel_param("kb_off", '1' if val else '0')
        return self.get_state_off()

    def set_colors(self, colors):
        if not self.driver_ok:
            return
        for section in self.colors.keys():
            if section in colors:
                self.__set_kernel_param("kb_{}".format(section), self.colors_code[colors[section]])
        return self.get_colors(colors.keys())

    """ Kernel Ops """
    def __get_kernel_param(self, filename):
        with open(self.driver_location + filename, 'r') as f:
            return str(int([x for x in f][0]))

    def __set_kernel_param(self, filename, val):
        if self.__get_kernel_param(filename) != val:
            with open(self.driver_location + filename, 'w') as f:
                f.write(val)

if __name__ == "__main__":
    kb = Keyboard("/sys/module/tuxedo_wmi/parameters/")
    print "Brightness: {}".format(kb.get_brightness())
    print "State Off: {}".format(kb.get_state_off())
    print "Left Color: {left}\n" \
          "Center Color: {center}\n" \
          "Right Color: {right}"\
        .format(**kb.get_colors(["left", "center", "right"]))
