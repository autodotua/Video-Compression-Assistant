import re
import os
import sys
import time
import subprocess
from vca.print_redirect import PrintRedirect
from PyQt5.QtCore import *
from subprocess import Popen, DEVNULL, STDOUT
from datetime import datetime, timedelta
import traceback


class ExcuteThread(QThread):
    print_signal = pyqtSignal(str)
    status_signal = pyqtSignal(dict)
    progress_signal = pyqtSignal(dict)
    stream_signal = pyqtSignal(subprocess.Popen)
    comparison_signal = pyqtSignal(dict)
    r_ffmpeg_time = re.compile(
        r"([0-9]{2,}):([0-9][0-9]):([0-9][0-9])\.([0-9][0-9])")
    r_progress = re.compile(
        r'frame= *([0-9]+) *fps= *([0-9\.]+) *q= *([0-9\.]+) *size= *([0-9\.a-zA-Z]+) *time= *([0-9\.:]+) *bitrate= *([0-9\.a-z/]+) *speed= *([0-9\.]+)x')
    r_ssim = re.compile(r"SSIM (([YUVAll]+:[0-9\.\(\) ]+)+)")
    r_psnr = re.compile(r"PSNR (([yuvaverageminmax]+:[0-9\. ]+)+)")
    stopping = False
    ssim = False

    def __init__(self, io_args=None, input_args=None, output_args=None, cmd=None):
        self.cmd = cmd
        self.io_args = io_args
        self.input_args = input_args
        self.output_args = output_args
        super(ExcuteThread, self).__init__()

    def generate_args_command(self, cmd_list, arg_dict):
        for key, value in arg_dict.items():
            cmd_list.append("-"+key)
            if value:
                cmd_list.append(str(value))

    def generate_command(self, io):
        cmd_list = ["ffmpeg -y -hide_banner"]
        if self.input_args:
            self.generate_args_command(cmd_list, self.input_args)
        cmd_list.append("-i")
        cmd_list.append(io["input"])
        if self.output_args:
            self.generate_args_command(cmd_list, self.output_args)
        cmd_list.append(io["output"])
        cmd = ' '.join(cmd_list)
        return cmd

    def get_ffmpeg_seconds(self, time):
        match = self.r_ffmpeg_time.match(time)
        if not match:
            return None
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        mseconds = int(match.group(4))
        seconds = hours*3600+minutes*60+seconds+mseconds/100.0
        return seconds

    def match_progress(self, io,start_time,length, output):
        match = self.r_progress.match(output)
        if match:
            now = datetime.now()
            progress = {
                "file": io["input"],
                "frame": match.group(1),
                "fps": match.group(2),
                "q": match.group(3),
                "size": match.group(4),
                "time": match.group(5),
                "bitrate": match.group(6),
                "speed": match.group(7),
                "elapsed": now-start_time,
                "unkonwn": False
            }
            if length > 0:
                percent = self.get_ffmpeg_seconds(
                    match.group(5))/length
                progress["percent"] = percent
                progress["left"] = (now-start_time) * \
                    ((1-percent)/percent)
        else:
            progress = {"unkonwn": True}
        
        self.progress_signal.emit(progress)

    def match_comparison(self, output):
        match = self.r_psnr.search(output)
        if match:
            if self.ssim:
                self.comparison_signal.emit(
                    {"ssim": self.ssim, "psnr": match.group(1)})
                self.ssim = None
                return
        match = self.r_ssim.search(output)
        if match:
            self.ssim = match.group(1)

    def excute_cmd(self, io, length):
        start_time = datetime.now()
        cmd = self.cmd if self.cmd is not None else self.generate_command(io)
        self.ff_process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT, encoding="utf8", universal_newlines=True,
                                           creationflags=subprocess.CREATE_NO_WINDOW)
        l = 0
        while not self.ff_process.poll():
            output = self.ff_process.stdout.readline()
            if len(output) == 0:
                break
            self.match_progress(io, start_time,length,output)
            self.match_comparison(output)
            self.print_signal.emit(output.strip())

    def run(self):
        try:
            if self.cmd:
                self.excute_cmd(None, -1)
            else:
                for io in self.io_args:
                    if self.stopping:
                        return
                    self.status_signal.emit(
                        {"index": io["index"], "status": "处理中"})
                    info_process = subprocess.Popen("ffprobe.exe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "+io["input"],
                                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                    creationflags=subprocess.CREATE_NO_WINDOW,
                                                    stderr=subprocess.STDOUT, encoding="utf8", universal_newlines=True)
                    output = info_process.communicate()[0].strip()
                    length = float(output)
                    self.excute_cmd(io, length)

                    self.status_signal.emit(
                        {"index": io["index"], "status": "完成"})
            # p=subprocess.Popen("ffmpeg -i input.mp4 output.flv", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as ex:

            self.print_signal.emit(traceback.format_exc())
        # self.stream_signal.emit(p)
        # while True:
        #     line = p.stderr.readline()
        #     if(line):
        #         self.print_signal.emit(line.decode("utf-8"))

    def stop(self):
        self.stopping = True
        self.ff_process.stdin.write("q")
        self.ff_process.stdin.flush()
