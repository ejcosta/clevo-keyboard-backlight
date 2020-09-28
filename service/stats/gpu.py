__author__ = 'harenbrs'

import subprocess
from xml.dom import minidom


def get_gpu_load():
    try:
        xml = subprocess.check_output(['nvidia-smi', '-q', '-x'])
    except FileNotFoundError:
        return 0
    
    dom = minidom.parseString(xml)
    extract_util = lambda tag: int(
        dom.getElementsByTagName(tag)[0].childNodes[0].data.split(' %')[0]
    )
    utils = list(
        map(extract_util, ['gpu_util', 'memory_util', 'encoder_util', 'decoder_util'])
    )
    extract_memory = lambda i: int(
        dom.getElementsByTagName('fb_memory_usage')[0]
        .childNodes[i]
        .childNodes[0]
        .data.split(' ')[0]
    )
    total, used, free = map(extract_memory, [1, 3, 5])
    memory_usage = 100*used//total
    return max(memory_usage, *utils)


def print_gpu_load():
    print("GPU Percent: {}".format(get_gpu_load()))


if __name__ == "__main__":
    print_gpu_load()
