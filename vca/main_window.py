from vca.main_window_layout import Ui_MainWindow
from vca.excute_thread import ExcuteThread
from vca.print_redirect import PrintRedirect
from vca.dicts import *
from vca.tools import *
from vca.model.file_list_model import FileListModel
from vca.model.file_model import FileModel
import sys
import os
import platform
import subprocess
import threading
import asyncio
from io import StringIO
from pathlib import Path
from datetime import timedelta
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pickle
import subprocess


class Application(Ui_MainWindow):
    converting = False
    files = FileListModel()

    def __init__(self):
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        pass

    def show(self):
        app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.setupUi(self.MainWindow)
        self.setup_init_values()
        self.setup_events()
        if platform.system() == "Windows":
            app.setFont(QFont("Microsoft Yahei UI", 9))
        self.MainWindow.show()
        icon = QIcon()
        # icon.addPixmap(QPixmap("niconvert/fz/icon.ico"),
        # QIcon.Normal, QIcon.Off)
        self.MainWindow.setWindowIcon(icon)
        sys.exit(app.exec_())

    def setup_init_values(self):
        self.update_progress(None)
        self.lst.setModel(self.files)
        self.lbl_preset.setText(presets[self.sld_preset.value()]["desc"])

    def get_output_args(self):
        args = {}
        if not self.grpb_video.isChecked():
            args["c:v"] = "copy"
            encoder = None
        else:
            encoder = self.cbb_encoder.currentText()
            args["c:v"] = encoder_infos[encoder]["lib"]
            args["preset"] = presets[self.sld_preset.value()]["code"]
            if self.chk_crf.isEnabled() and self.chk_crf.isChecked():
                args["crf"] = self.sld_crf.value()
                if encoder == "VP9":
                    args["b:v"] = "0"
            if self.chk_size.isChecked():
                args["s"] = self.txt_size.text()
            if self.chk_bitrate.isEnabled() and self.chk_bitrate.isChecked():
                args["b:v"] = str(self.txt_bitrate.value())+"M"
            if self.chk_bitrate_max.isChecked():
                args["maxrate"] = str(self.txt_bitrate_max.value())+"M"
                args["bufsize"] = str(self.txt_bitrate_max.value()*2)+"M"
            if self.chk_bitrate_min.isChecked():
                args["minrate"] = str(self.txt_bitrate_min.value())+"M"
            if self.chk_fps.isChecked():
                args["r"] = self.cbb_fps.currentText()
                print("output args is "+str(args))

        if not self.grpb_audio.isChecked():
            pass
            #args["c:a"] = "copy"
        else:
            args["b:a"] = self.cbb_bitrate_a.currentText()+"k"

        return {"filter_args": args, "encoder": encoder}

    def starting(self):
        self.converting = True
        self.btn_start.setText("停止")
        # self.table_input.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def finished(self):
        self.converting = False
        print("finished")
        self.btn_start.setEnabled(True)
        self.btn_start.setText("开始")
        self.update_progress(None)
        # self.table_input.resizeColumnsToContents()
        # self.table_input.setEditTriggers(
        #     QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)

    def status_changed(self, i):
        # self.table_input.setItem(i["index"], 2, QTableWidgetItem(i["status"]))
        # self.table_input.resizeColumnsToContents()
        pass

    def format_delta(self, time):
        seconds = int(time.total_seconds())
        second = seconds % 60
        minute = int(seconds / 60) % 60
        hour = int(seconds/3600)
        return "{}:{:02}:{:02}".format(hour, minute, second)

    def update_progress(self, progress):
        if progress is None:
            self.lbl_current_file.setText("")
            self.lbl_current_frame_time.setText("")
            self.lbl_current_speed.setText("")
            self.lbl_current_bitrate.setText("")
            self.lbl_current_time.setText("")
            self.prgb_current.setMaximum(100)
            self.prgb_current.reset()

        elif progress["unkonwn"] == True:
            self.prgb_current.setMaximum(0)

        else:
            self.lbl_current_file.setText(progress["file"])
            self.lbl_current_frame_time.setText(
                "第"+progress["frame"] + "帧  "+progress["time"])
            self.lbl_current_speed.setText(
                progress["fps"] + "FPS  "+progress["speed"]+"×")
            self.lbl_current_bitrate.setText(progress["bitrate"])
            self.prgb_current.setMaximum(100)
            if "percent" in progress:
                self.prgb_current.setValue(int(progress["percent"]*100))
                self.lbl_current_time.setText(
                    "已用"+self.format_delta(progress["elapsed"]) + "  剩余"+self.format_delta(progress["left"]))

    def show_comparision_result(self, args):
        QMessageBox.information(
            None, "比较结果", "结构程度：\n"+args["ssim"].replace(" (", "（").replace(
                " ", "\n").replace("（", " (")+"\n\n信噪比：\n"+args["psnr"].replace(" ", "\n"))

    def start(self):
        if self.converting:
            self.btn_start.setEnabled(False)
            self.thread.stop()
        else:
            if False:
                QMessageBox.critical(None, "错误", "还没有选择任何文件", QMessageBox.Ok)
                return
            self.starting()
            if self.rbtn_convert.isChecked():
                self.thread = ExcuteThread(
                    self.files.files, self.get_output_args())
            elif self.rbtn_compare.isChecked():
                if self.files.rowCount() != 2:
                    QMessageBox.critical(
                        None, "错误", "输入文件必须为2个", QMessageBox.Ok)
                    return
                input1 = self.files.files[0].input
                input2 = self.files.files[1].input
                cmd = 'ffmpeg -i {} -i {} -lavfi "ssim;[0:v][1:v]psnr" -f null -' .format(
                    input1, input2)
                self.thread = ExcuteThread(cmd=cmd)
            elif self.rbtn_sub.isCheckable():
                self.thread = ExcuteThread(self.files.files, {
                                           "encoder": "Srt", "filter_args": {}})
            self.thread.print_signal.connect(lambda p:  self.txt_log.append(p))
            self.thread.progress_signal.connect(self.update_progress)
            self.thread.comparison_signal.connect(self.show_comparision_result)
            self.thread.finished.connect(self.finished)
            self.thread.status_signal.connect(self.status_changed)
            self.thread.start()

    # def encode_mode_changed(self, index):
    #     self.chk_crf.setEnabled(index == 0)
    #     self.sld_crf.setEnabled(index == 0)
    #     self.chk_bitrate.setEnabled(index == 1)
    #     self.txt_bitrate.setEnabled(index == 1)

    def encoder_changed(self, value):
        self.sld_crf.setMaximum(encoder_infos[value]["crf"]["max"])
        self.sld_crf.setValue(encoder_infos[value]["crf"]["default"])

    def btn_input_clicked(self):
        paths = QFileDialog.getOpenFileNames(
            self.MainWindow, "打开",  filter="所有文件 (*.*)")
        if paths[0]:
            for path in paths[0]:
                self.files.addFile(FileModel(path,path))

    def delete_selection(self):
        indexex = self.lst.selectionModel().selection().indexes()
        files=[]
        for index in indexex:
            files.append(self.files.files[index.row()])

        for file in files:
            index=self.files.files.index(file)
            self.files.removeFile(index)

    def selected_file_changed(self, index):
        if index is None or len(index.indexes()) != 1:
            self.gpb_file.setEnabled(False)
        else:
            self.gpb_file.setEnabled(True)
            row = index.indexes()[0].row()
            self.txt_input.setText(self.files.files[row].input)
            self.txt_output.setText(self.files.files[row].output)
            self.chk_image_seq.setChecked(self.files.files[row].image_seq)
            self.chk_force_ext.setChecked(self.files.files[row].force_ext)
            self.chk_cut.setChecked(self.files.files[row].need_cut)
            if self.files.files[row].need_cut:
                time_from = self.files.files[row].cut[0]
                time_to = self.files.files[row].cut[1]
                self.time_from.setTime(seconds_to_qtime(time_from))
                self.time_to.setTime(seconds_to_qtime(time_to))
            input_fps = self.files.files[row].input_fps
            self.chk_input_fps.setChecked(input_fps > 0)
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
                         float(self.cbb_input_fps.currentText()) if self.chk_input_fps.isChecked() else 0)
        self.files.editFile(index.row(), file)
        pass

    def chk_input_fps_toggled(self, checked):
        self.cbb_input_fps.setEnabled(checked)

    def setup_events(self):
        self.btn_start.clicked.connect(self.start)
        self.cbb_encoder.currentTextChanged.connect(self.encoder_changed)
        self.sld_crf.valueChanged.connect(
            lambda value: self.lbl_crf.setText(str(value)))
        self.sld_preset.valueChanged.connect(
            lambda value: self.lbl_preset.setText(str(presets[value]["desc"])))
        self.btn_input.clicked.connect(self.btn_input_clicked)
        self.btn_delete.clicked.connect(self.delete_selection)
        self.lst.selectionModel().selectionChanged.connect(self.selected_file_changed)

        self.chk_cut.toggled.connect(self.cut_changed)
        self.chk_input_fps.toggled.connect(self.chk_input_fps_toggled)
        self.btn_io_save.clicked.connect(self.save_io_settings)
        self.btn_io_reset.clicked.connect(
            lambda: self.selected_file_changed(self.lst.selectionModel().selection()))
