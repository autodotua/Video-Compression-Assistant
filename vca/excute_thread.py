import re
import os
import sys
import time
import subprocess
from vca.print_redirect import PrintRedirect
from vca.tools import *
from vca.dicts import *
from PyQt5.QtCore import *
from subprocess import Popen, DEVNULL, STDOUT
from datetime import datetime, timedelta
import traceback
import psutil
from vca.model.status import Status


class ExcuteThread(QThread):
    finish_signal = pyqtSignal()
    print_signal = pyqtSignal(str)
    status_signal = pyqtSignal(dict)
    progress_signal = pyqtSignal(Status)
    stream_signal = pyqtSignal(subprocess.Popen)
    comparison_signal = pyqtSignal(dict)
    r_ffmpeg_time = re.compile(
        r"([0-9]{2,}):([0-9][0-9]):([0-9][0-9])\.([0-9][0-9])")
    r_progress = re.compile(
        r'frame= *([0-9]+) *fps= *([0-9\.]+) *q= *([0-9\.\-]+) *size= *([0-9\.a-zA-Z]+) *time= *([0-9\.:]+) *bitrate= *([0-9\.a-z/]+).*speed= *([0-9\.]+)x')
    r_ssim = re.compile(r"SSIM (([YUVAll]+:[0-9\.\(\) ]+)+)")
    r_psnr = re.compile(r"PSNR (([yuvaverageminmax]+:[0-9\. ]+)+)")
    stopping = False
    ssim = False

    def __init__(self, input_args=None, output_args=None, cmd=None):
        self.cmd = cmd
        self.input_args = input_args
        self.output_args = output_args
        self.current = Status()
        self.stopping = False
        self.pausing = False
        super(ExcuteThread, self).__init__()

  

    def generate_command(self, input):
        cmd_list = ["ffmpeg -y -hide_banner"]
        if self.input_args:
            generate_args_command(cmd_list, input.get_input_args())

        cmd_list.append("-i")
        cmd_list.append('"'+input.input+'"')
        if input.subtitle_path is not None:
            cmd_list.append("-i")
            cmd_list.append('"'+input.subtitle_path+'"')
            cmd_list.append('-c:s copy') 

        if self.output_args:
            generate_args_command(
                cmd_list, self.output_args.get_filter_args())

        if self.output_args.video_filter is None or self.output_args.video_filter.encoder is None or input.force_ext:
            output = get_unique_file_name(input.output)
        elif self.output_args.output_format is not None:
            output = get_unique_file_name(
                input.output, self.output_args.output_format)
        else:
            ext = encoder_infos[self.output_args.video_filter.encoder]["ext"]
            output = get_unique_file_name(input.output, ext)

        cmd_list.append('"'+output+'"')
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

    def match_progress(self, output):
        match = self.r_progress.match(output)

        if match:
            now = datetime.now()
            self.current.frame = match.group(1)
            self.current.fps = match.group(2)
            self.current.q = match.group(3)
            self.current.size = match.group(4)
            self.current.time = match.group(5)
            self.current.bitrate = match.group(6)
            self.current.speed = match.group(7)
            self.current.elapsed = now-self.current.start_time
            self.current.unkown = False
            if self.current.length > 0:
                percent = self.get_ffmpeg_seconds(
                    match.group(5))/self.current.length
                self.current.percent = percent
                self.current.left = (now-self.current.start_time) * \
                    ((1-percent)/percent)
                self.current.complete_time = now+self.current.left
            else:
                self.current.percent = None
        else:
            self.current.unkown = True

        self.progress_signal.emit(self.current)

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

    def write_log(self,msg):
        if self.current.start_time is None:
            return
        log_dir = './logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        file=log_dir+'/vca_'+self.current.start_time.strftime('%Y%m%d_%H%M%S')+".log"
        with open(file,'a+') as f:
            f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:23]+"    "+(msg.strip() if isinstance(msg,str) else "未知日志输出")+'\n')

    def excute_cmd(self):
        self.current.start_time = datetime.now()
        self.write_log("开始执行命令："+self.current.cmd)
        self.ff_process = subprocess.Popen(self.current.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT, encoding="utf8", universal_newlines=True,
                                           creationflags=subprocess.CREATE_NO_WINDOW)
        l = 0
        if self.stopping:
            return
        while not self.ff_process.poll():
            try:
                output = self.ff_process.stdout.readline()
                self.write_log(output)
            except Exception as ex:
                self.print_signal.emit("读取输出失败："+str(ex))
                self.write_log("读取输出失败："+str(ex))
                continue
            if len(output) == 0:
                break
            self.match_progress(output)
            self.match_comparison(output)
            self.print_signal.emit(output.strip())

    def get_length(self, input):
        try:
            path = input.input
            if input.image_seq:
                dir = os.path.dirname(path)
                count = len([name for name in os.listdir(dir) if os.path.isfile(
                    os.path.join(dir, name))])  # 文件夹内文件总数
                if "r" in self.output_args["filter_args"]:
                    r = self.output_args["filter_args"]["r"]  # 帧率
                else:
                    r = 25
                return count/r
            else:
                info_process = subprocess.Popen('ffprobe.exe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "'+path+'"',
                                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                creationflags=subprocess.CREATE_NO_WINDOW,
                                                stderr=subprocess.STDOUT, encoding="utf8", universal_newlines=True)
                outputs = info_process.communicate()
                if len(outputs) == 0:
                    return 0
                output = outputs[0].strip()
                if output == "N/A":
                    length = 0
                else:
                    length = float(output)
                
                return length
        except Exception as ex:
            self.print_signal.emit("获取视频长度失败"+str(ex))
            print("error to get length:"+str(ex))
            return 0

    def has_audio(self, path):
        info_process = subprocess.Popen("ffprobe.exe -show_streams -select_streams a -loglevel error "+path,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        creationflags=subprocess.CREATE_NO_WINDOW,
                                        stderr=subprocess.STDOUT, encoding="utf8", universal_newlines=True)
        output = info_process.communicate()[0].strip()
        print("has audio output is "+output + str(bool(output)))
        return bool(output)

    def run(self):
        try:
            if self.cmd:
                if isinstance(self.cmd, list):
                    for c in self.cmd:
                        if self.stopping:
                            return
                        self.current.cmd = c
                        self.excute_cmd()
                else:
                    self.current.cmd = self.cmd
                    self.excute_cmd()
            else:
                for input in self.input_args:
                    if self.stopping:
                        return
                    self.current.input = input
                    if input.cut:
                        self.current.length=input.cut[1]-input.cut[0]
                    else:
                        self.current.length = self.get_length(input)
                    self.current.cmd = self.cmd if self.cmd is not None else self.generate_command(
                        input)

                    self.excute_cmd()
        except Exception as ex:
            self.print_signal.emit(traceback.format_exc())

        self.finish_signal.emit()

    def stop(self):
        self.write_log("停止")
        self.stopping = True
        if self.pausing:
            self.resume()
        if hasattr(self, 'ff_process'):
            self.ff_process.stdin.write("q")
            self.ff_process.stdin.flush()

    def pause(self):
        self.write_log("暂停")
        self.pausing = True
        self.pause_start_time = datetime.now()
        psutil.Process(pid=self.ff_process.pid).suspend()

    def resume(self):
        self.write_log("恢复")
        self.pausing = False
        self.current.start_time = self.current.start_time + \
            (datetime.now()-self.pause_start_time)
        psutil.Process(pid=self.ff_process.pid).resume()
