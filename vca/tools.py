import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


def get_unique_file_name(path, ext=None):
    name, ext2 = os.path.splitext(path)
    if ext is None:
        ext = ext2
    if not os.path.isfile(name+ext):
        return name+ext
    index = 1
    while os.path.isfile(name+"_"+str(index)+ext):
        index += 1
    return name+"_"+str(index)+ext
    # return name+"_"+str(index)+ext


def qtime_to_seconds(time):
    return time.hour()*3600+time.minute()*60+time.second()+time.msec()*0.001


def seconds_to_qtime(seconds):
    h = int(seconds/3600)
    m = int(seconds/60) % 60
    s = seconds % 60
    ms=int((seconds%1)*1000)
    return QTime(h, m, s,ms)

def generate_args_command(cmd_list, arg_dict):
    if isinstance(arg_dict, str):
        cmd_list.append(arg_dict)
        return
    for key, value in arg_dict.items():
        if key != "":
            cmd_list.append("-"+key)
        if value:
            cmd_list.append(str(value))