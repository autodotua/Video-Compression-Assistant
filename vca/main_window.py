from vca.main_window_layout import Ui_MainWindow
from vca.excute_thread import *
from vca.print_redirect import PrintRedirect
from vca.dicts import *
from vca.tools import *
from vca.model.file_list_model import FileListModel
from vca.model.file_model import FileModel
from vca.model.output_model import OutputModel
from vca.model.config import *
from vca.model.status import Status
import sys
import os
import platform
import subprocess
import threading
import asyncio
from io import StringIO
from pathlib import Path
from datetime import timedelta
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWinExtras import QWinTaskbarProgress, QWinTaskbarButton
import pickle
import subprocess
import psutil
import math


class VcaMainWindow(QMainWindow):
    isWorking = False

    def closeEvent(self, event):
        if self.isWorking:
            QMessageBox.warning(self, "警告", "请先停止正在进行的任务")
            event.ignore()


class Application(Ui_MainWindow):
    converting = False
    config = Config.restore()
    last_outputs = ""

    def __init__(self):
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        pass

    def show(self):
        app = QApplication(sys.argv)
        self.MainWindow = VcaMainWindow()
        self.setupUi(self.MainWindow)

        self.init_task_bar()
        self.setup_init_values()
        self.setup_events()
        if platform.system() == "Windows":
            app.setFont(QFont("Microsoft Yahei UI", 9))
        self.MainWindow.show()
        self.taskbar_progress.show()
        self.taskbar_button.setWindow(self.MainWindow.windowHandle())
        icon = QIcon()
        icon.addPixmap(QPixmap("icon.ico" if app_dir is None else os.path.join(app_dir, "icon.ico")),
                       QIcon.Normal, QIcon.Off)
        self.MainWindow.setWindowIcon(icon)
        sys.exit(app.exec_())

    def init_task_bar(self):
        self.taskbar_button = QWinTaskbarButton()
        self.taskbar_progress = self.taskbar_button.progress()
        self.taskbar_progress.setRange(0, 100)

    def setup_init_values(self):
        self.update_progress(None)
        self.txt_last_output.setText("")
        self.files = FileListModel(
            self.config.files) if self.config.autosave else FileListModel()
        self.lst.setModel(self.files)
        self.apply_output_ui()
        self.lbl_preset.setText(presets[self.sld_preset.value()]["desc"])
        self.btn_pause.hide()

    def apply_output_ui(self):
        model = self.config.output_args
        if model.video_filter is None:
            self.grpb_video.setChecked(False)
        else:
            self.grpb_video.setChecked(True)
            video = model.video_filter
            self.cbb_encoder.setCurrentText(video.encoder)
            self.sld_preset.setValue(video.preset)

            if video.crf is None:
                self.chk_crf.setChecked(False)
            else:
                self.lbl_crf.setText(str(video.crf))
                self.chk_crf.setChecked(True)
                self.sld_crf.setValue(video.crf)

            if video.size is None:
                self.chk_size.setChecked(False)
            else:
                self.chk_size.setChecked(True)
                self.txt_size.setText(video.size)

            if video.bitrate is None:
                self.chk_bitrate.setChecked(False)
            else:
                self.chk_bitrate.setChecked(True)
                self.txt_bitrate.setValue(video.bitrate)

            if video.max_bitrate is None:
                self.chk_bitrate_max.setChecked(False)
            else:
                self.chk_bitrate_max.setChecked(True)
                self.txt_bitrate_max.setValue(video.max_bitrate)
                self.txt_bufsize.setValue(video.bufsize)


            if video.fps is None:
                self.chk_fps.setChecked(False)
            else:
                self.chk_fps.setChecked(True)
                self.cbb_fps.setCurrentText(video.fps)

        audio = model.audio_filter
        if audio.mode == "copy":
            self.cbb_audio_mode.setCurrentText("复制")
        elif audio.mode == "encode":
            self.cbb_audio_mode.setCurrentText("重编码（自动）")
        elif audio.mode == "aac":
            self.cbb_audio_mode.setCurrentText("重编码AAC")
        elif audio.mode == "default":
            self.cbb_audio_mode.setCurrentText("默认")
        elif audio.mode == "none":
            self.cbb_audio_mode.setCurrentText("不导出")
        self.cbb_bitrate_a.setCurrentText(str(audio.bitrate))

        self.txt_filter_extra_args.setPlainText(model.extra_args)

    def get_output_args(self):
        model = OutputModel()
        if not self.grpb_video.isChecked():
            video_model = None
        else:
            video_model = OutputModel.VideoFilterModel()

            video_model.encoder = self.cbb_encoder.currentText()
            video_model.preset = self.sld_preset.value()
            video_model.crf = self.sld_crf.value() if self.chk_crf.isChecked() else None
            video_model.size = self.txt_size.text() if self.chk_size.isChecked() else None
            video_model.bitrate = self.txt_bitrate.value(
            ) if self.chk_bitrate.isChecked() else None
            video_model.max_bitrate = self.txt_bitrate_max.value(
            ) if self.chk_bitrate_max.isChecked() else None
            video_model.bufsize = self.txt_bufsize.value() 
            video_model.fps = self.cbb_fps.currentText() if self.chk_fps.isChecked() else None

        audio_model = OutputModel.AudioFilterModel()
        mode_text = self.cbb_audio_mode.currentText()
        audio_model.bitrate = math.floor(
            float(self.cbb_bitrate_a.currentText()))
        if mode_text == "复制":
            audio_model.mode = "copy"
        elif mode_text == "重编码AAC":
            audio_model.mode = "aac"
        elif mode_text == "重编码（自动）":
            audio_model.mode = "encode"
        elif mode_text == "默认":
            audio_model.mode = "default"
        else:
            audio_model.mode = "none"

        model.extra_args = self.txt_filter_extra_args.toPlainText()

        model.video_filter = video_model
        model.audio_filter = audio_model
        return model

    def starting(self):
        self.converting = True
        self.pausing = False
        self.btn_start.setText("停止")
        self.btn_pause.setFocus()
        self.btn_pause.setText("暂停")
        self.MainWindow.isWorking = True
        # self.table_input.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def finished(self):
        self.converting = False
        print("finished")
        self.btn_start.setEnabled(True)
        self.btn_start.setText("开始")
        self.update_progress(None)
        self.MainWindow.isWorking = False

    def status_changed(self, i):
        pass

    def format_datetime(self, time):
        month = time.month
        day = time.day
        hour = time.hour
        minute = time.minute
        second = time.second
        return "{}月{}日 {:02}:{:02}:{:02}".format(month, day, hour, minute, second)

    def format_delta(self, time):
        seconds = int(time.total_seconds())
        second = seconds % 60
        minute = int(seconds / 60) % 60
        hour = int(seconds/3600)
        return "{}:{:02}:{:02}".format(hour, minute, second)

    def update_progress(self, current):
        if current is None:
            self.lbl_current_file.setText("")
            self.lbl_current_frame_time.setText("")
            self.lbl_current_speed.setText("")
            self.lbl_current_bitrate.setText("")
            self.lbl_current_time.setText("")
            # self.txt_current_cmd.setText("")
            self.prgb_current.setMaximum(100)
            self.prgb_current.reset()
            self.btn_pause.hide()
            self.taskbar_progress.hide()
        else:
            self.txt_current_cmd.setText(current.cmd)

            if current.unkown == True:
                self.prgb_current.setMaximum(0)

            else:
                try:
                    self.lbl_current_file.setText(current.input.input)
                except:
                    pass

                self.lbl_current_frame_time.setText(
                    "第"+current.frame + "帧  "+current.time)
                self.lbl_current_speed.setText(
                    current.fps + "FPS  "+current.speed+"×")
                self.lbl_current_bitrate.setText(
                    current.bitrate+"  q="+current.q)
                self.prgb_current.setMaximum(10000)
                if current.percent:
                    self.prgb_current.setFormat(
                        format(int(current.percent*10000)/100, '.2f')+"%")
                    self.prgb_current.setValue(int(current.percent*10000))
                    self.lbl_current_time.setText(
                        "已用："+self.format_delta(current.elapsed) + "    剩余："+self.format_delta(current.left)+"    预计完成："+self.format_datetime(current.complete_time))
                    self.taskbar_progress.setValue(int(current.percent*100))

    def show_comparision_result(self, args):
        QMessageBox.information(
            None, "比较结果", "结构程度：\n"+args["ssim"].replace(" (", "（").replace(
                " ", "\n").replacevalue("（", " (")+"\n\n信噪比：\n"+args["psnr"].replace(" ", "\n"))

    def update_last_outputs(self, value):
        self.txt_last_output.setText(self.last_outputs+"\r\n"+value)
        self.last_outputs = value
        print("program output: "+value)

    def save_config(self, path=None):
        self.config.files = self.files.files
        self.config.output_args = self.get_output_args()
        if path:
            self.config.save(path)
        else:
            self.config.save()

    def pause(self):
        if not self.pausing:
            self.thread.pause()
            self.pausing = True
            self.btn_pause.setText("继续")
            self.taskbar_progress.pause()
        else:
            self.thread.resume()
            self.pausing = False
            self.btn_pause.setText("暂停")
            self.taskbar_progress.resume()

    def clear_temp_files(self):
        g = os.walk(os.getcwd())
        for path, dir_list, file_list in g:
            for file in filter(lambda p: p.startswith('temp'), file_list):
                os.remove(file)
            return

    def start(self):
        if self.converting:
            if QMessageBox.question(self.MainWindow, '警告', "是否结束任务?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                self.btn_start.setEnabled(False)
                self.thread.stop()
                self.btn_pause.hide()
                self.taskbar_progress.stop()
        else:
            self.save_config()
            if self.files.rowCount() == 0:
                QMessageBox.critical(self.MainWindow, "错误",
                                     "还没有选择任何文件", QMessageBox.Ok)
                return
            self.starting()
            self.btn_pause.show()
            self.taskbar_progress.setPaused(False)
            self.taskbar_progress.resume()
            self.taskbar_progress.reset()
            self.taskbar_progress.show()
            if self.rbtn_convert.isChecked():
                self.thread = ExcuteThread(
                    self.files.files, self.get_output_args())
            elif self.rbtn_custom.isChecked():
                self.thread = ExcuteThread(
                    cmd="ffmpeg -y -hide_banner "+self.txt_filter_extra_args.toPlainText())
            elif self.rbtn_concat.isChecked():
                if self.files.rowCount() < 2:
                    QMessageBox.critical(
                        None, "错误", "输入文件必须大于2个", QMessageBox.Ok)
                    return
                cmds = []
                ts_files = []
                index = 1
                output_args = self.get_output_args()
                for file in self.files.files:
                    cmd_list = [
                        'ffmpeg -y -hide_banner -i "{}"'.format(file.input)]
                    if output_args.video_filter:
                        generate_args_command(
                            cmd_list, output_args.video_filter.get_filter_args())
                    else:
                        cmd_list.append("-c:v copy")
                    generate_args_command(
                        cmd_list, output_args.audio_filter.get_filter_args())
                    cmd_list.append(self.txt_filter_extra_args.toPlainText())
                    cmd_list.append('temp_{}.ts' .format(str(index)))
                    cmds.append(' '.join(cmd_list))
                    ts_files.append("temp_{}.ts".format(str(index)))
                    index += 1

                outputcmd = 'ffmpeg  -y -hide_banner -i "concat:{}" -c copy  {}'.format(
                    '|'.join(ts_files), get_unique_file_name(self.files.files[0].output, ".mp4"))
                cmds.append(outputcmd)
                self.thread = ExcuteThread(cmd=cmds)

            elif self.rbtn_compare.isChecked():
                if self.files.rowCount() != 2:
                    QMessageBox.critical(
                        None, "错误", "输入文件必须为2个", QMessageBox.Ok)
                    return
                input1 = self.files.files[0].input
                input2 = self.files.files[1].input
                cmd = 'ffmpeg -i "{}" -i "{}" -lavfi "ssim;[0:v][1:v]psnr" -f null -' .format(
                    input1, input2)
                self.thread = ExcuteThread(cmd=cmd)
            elif self.rbtn_merge.isChecked():
                if self.files.rowCount() != 2:
                    QMessageBox.critical(
                        None, "错误", "输入文件必须为2个", QMessageBox.Ok)
                    return
                input1 = self.files.files[0].input
                input2 = self.files.files[1].input
                if input1.endswith("weba") or input1.endswith("aac") or input1.endswith("m4a"):
                    temp = input1
                    input1 = input2
                    input2 = temp
                output = get_unique_file_name('.'.join(self.files.files[0].output.split('.')[
                                              0:-1])+'.'+input1.split('.')[-1])
                cmd = 'ffmpeg -i "{}" -i "{}" -strict -2 -c:v copy -c:a copy "{}"' .format(
                    input1, input2, output)
                self.thread = ExcuteThread(cmd=cmd)
            elif self.rbtn_sub.isCheckable():
                output = OutputModel()
                output.manual = True
                output.output_format = ".srt"
                self.thread = ExcuteThread(self.files.files, output)
            self.thread.print_signal.connect(self.update_last_outputs)
            self.thread.progress_signal.connect(self.update_progress)
            self.thread.comparison_signal.connect(self.show_comparision_result)
            self.thread.finished.connect(self.finished)
            self.thread.status_signal.connect(self.status_changed)
            self.thread.finish_signal.connect(self.clear_temp_files)
            self.thread.start()

    def encoder_changed(self, value):
        self.sld_crf.setMaximum(encoder_infos[value]["crf"]["max"])
        self.sld_crf.setValue(encoder_infos[value]["crf"]["default"])

    def btn_clear_inputs_click(self):
        self.files.removeAllFiles()

    def btn_input_clicked(self):
        paths = QFileDialog.getOpenFileNames(
            self.MainWindow, "打开",  filter="所有文件 (*.*)")
        if paths[0]:
            for path in paths[0]:
                self.files.addFile(FileModel(path, path))

    def delete_selection(self):
        indexex = self.lst.selectionModel().selection().indexes()
        files = []
        for index in indexex:
            files.append(self.files.files[index.row()])

        for file in files:
            index = self.files.files.index(file)
            self.files.removeFile(index)

    def selected_file_changed(self, index):
        if index is None or len(index.indexes()) != 1:
            self.gpb_file.setEnabled(False)
        else:
            row = index.indexes()[0].row()
            file = self.files.files[row]
            self.gpb_file.setEnabled(True)
            self.txt_input.setText(file.input)
            self.txt_output.setText(file.output)
            self.chk_image_seq.setChecked(file.image_seq)
            self.chk_force_ext.setChecked(file.force_ext)
            self.chk_cut.setChecked(file.need_cut)
            if file.need_cut:
                time_from = file.cut[0]
                time_to = file.cut[1]
                self.time_from.setTime(seconds_to_qtime(time_from))
                self.time_to.setTime(seconds_to_qtime(time_to))
            input_fps = file.input_fps
            self.chk_input_fps.setChecked(input_fps > 0)
            self.txt_input_extra_args.setText(file.extra_args)
            if input_fps > 0:
                self.cbb_input_fps.setCurrentText(str(input_fps))

    def cut_changed(self, checked):
        self.time_from.setEnabled(checked)
        self.time_to.setEnabled(checked)

    def save_io_settings(self):
        index = self.lst.selectionModel().selection().indexes()[0]
        file = FileModel(self.txt_input.text(),
                         self.txt_output.text(),
                         [qtime_to_seconds(self.time_from.time()), qtime_to_seconds(
                             self.time_to.time())] if self.chk_cut.isChecked() else None,
                         self.chk_image_seq.isChecked(),
                         self.chk_force_ext.isChecked(),
                         float(self.cbb_input_fps.currentText()
                               ) if self.chk_input_fps.isChecked() else 0,
                         self.txt_input_extra_args.text())
        self.files.editFile(index.row(), file)
        pass

    def chk_input_fps_toggled(self, checked):
        self.cbb_input_fps.setEnabled(checked)

    def list_file_dropped(self, files):
        for file in files:
            self.files.addFile(FileModel(file, file))

    def import_config(self):
        path = QFileDialog.getOpenFileName(
            self.MainWindow, "保存",  filter="JSON文件 (*.json)")[0]
        if path:
            self.config = Config.restore(path)
            self.setup_init_values()
        pass

    def export_config(self):
        path = QFileDialog.getSaveFileName(
            self.MainWindow, "保存",  filter="JSON文件 (*.json)")[0]
        if path:
            self.save_config(path)
        pass

    def setup_events(self):
        self.btn_start.clicked.connect(self.start)
        self.btn_pause.clicked.connect(self.pause)
        self.cbb_encoder.currentTextChanged.connect(self.encoder_changed)
        self.sld_crf.valueChanged.connect(
            lambda value: self.lbl_crf.setText(str(value)))
        self.sld_preset.valueChanged.connect(
            lambda value: self.lbl_preset.setText(str(presets[value]["desc"])))
        self.btn_input.clicked.connect(self.btn_input_clicked)
        self.btn_clear_inputs.clicked.connect(self.btn_clear_inputs_click)
        self.btn_delete.clicked.connect(self.delete_selection)
        self.lst.selectionModel().selectionChanged.connect(self.selected_file_changed)

        self.chk_cut.toggled.connect(self.cut_changed)
        self.chk_input_fps.toggled.connect(self.chk_input_fps_toggled)
        self.btn_io_save.clicked.connect(self.save_io_settings)
        self.btn_io_reset.clicked.connect(
            lambda: self.selected_file_changed(self.lst.selectionModel().selection()))

        self.lst.dropped.connect(self.list_file_dropped)
        self.menu_import.triggered.connect(self.import_config)
        self.menu_export.triggered.connect(self.export_config)
