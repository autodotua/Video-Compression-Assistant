from vca.main_window_layout import Ui_MainWindow
from vca.excute_thread import ExcuteThread
from vca.print_redirect import PrintRedirect
from vca.dicts import *
from vca.tools import *
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

    def __init__(self):
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        pass

    def show(self):
        app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.setupUi(self.MainWindow)
        self.setup_events()
        self.setup_values()
        self.setup_items()
        if platform.system() == "Windows":
            app.setFont(QFont("Microsoft Yahei UI", 9))
        self.MainWindow.show()
        icon = QIcon()
        # icon.addPixmap(QPixmap("niconvert/fz/icon.ico"),
        # QIcon.Normal, QIcon.Off)
        self.MainWindow.setWindowIcon(icon)
        sys.exit(app.exec_())

    def setup_items(self):
        self.cbb_encoder.setCurrentIndex(1)
        self.cbb_encoder.setCurrentIndex(0)
        self.update_progress(None)

    def get_input_args(self):
        args = {}
        if self.grpb_cut.isChecked():
            time_from = self.time_start.time()
            time_to = self.time_to.time()
            second1 = time_from.hour()*3600+time_from.minute()*60+time_from.second()
            second2 = time_to.hour()*3600+time_to.minute()*60+time_to.second()
            span = second2-second1
            if second1 > 0:
                args["ss"] = second1
            args["t"] = span
        return args

    def get_output_args(self):
        args = {}
        if not self.grpb_video.isChecked():
            args["c:v"] = "copy"
        else:
            args["c:v"] = encoder_infos[self.cbb_encoder.currentText()]["lib"]
            args["preset"] = presets[self.sld_preset.value()]["code"]
            if self.chk_crf.isEnabled() and self.chk_crf.isChecked():
                args["crf"] = self.sld_crf.value()
                if self.encoder == "VP9":
                    args["b:v"] = "0"
            if self.chk_size.isChecked():
                args["s"] = self.txt_size.text()
            if self.chk_bitrate.isEnabled() and self.chk_bitrate.isChecked():
                args["b:v"] = str(self.txt_bitrate.value())+"M"
            if self.chk_bitrate_max.isChecked():
                args["maxrate"] = str(self.txt_bitrate_max.value())+"M"
                args["bufsize"]= str(self.txt_bitrate_max.value()*2)+"M"
            if self.chk_bitrate_min.isChecked():
                args["minrate"] = str(self.txt_bitrate_min.value())+"M"
            if self.chk_fps.isChecked():
                args["r"] = self.cbb_fps.currentText()
                print("output args is "+str(args))

        if not self.grpb_audio.isChecked():
            args["c:a"] = "copy"
        else:
            args["b:a"] = self.cbb_bitrate_a.currentText()+"k"
        return args

    def get_io_args(self, ext):
        args = []
        for row in range(0, self.table_input.rowCount()):
            output = self.table_input.item(row, 1).text(
            )+"."+ext
            output = get_unique_file_name(output)
            args.append({"index": row,
                         "input": self.table_input.item(row, 0).text(),
                         "output": output
                         })

        return args

    def starting(self):
        self.converting = True
        self.btn_start.setText("停止")
        self.table_input.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def finished(self):
        self.converting = False
        print("finished")
        self.btn_start.setEnabled(True)
        self.btn_start.setText("开始")
        self.update_progress(None)
        self.table_input.resizeColumnsToContents()
        self.table_input.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)

    def status_changed(self, i):
        self.table_input.setItem(i["index"], 2, QTableWidgetItem(i["status"]))
        self.table_input.resizeColumnsToContents()

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
            if self.table_input.rowCount() == 0:
                QMessageBox.critical(None, "错误", "还没有选择任何文件", QMessageBox.Ok)
                return
            self.starting()
            if self.rbtn_convert.isChecked():
                self.thread = ExcuteThread(self.get_io_args(encoder_infos[self.cbb_encoder.currentText()]["ext"]),
                                           self.get_input_args(), self.get_output_args())
            elif self.rbtn_compare.isChecked():
                if self.table_input.rowCount() != 2:
                    QMessageBox.critical(
                        None, "错误", "输入文件必须为2个", QMessageBox.Ok)
                    return
                cmd = 'ffmpeg -i {} -i {} -lavfi "ssim;[0:v][1:v]psnr" -f null -' .format(
                    self.table_input.item(0, 0).text(), self.table_input.item(1, 0).text())
                self.thread = ExcuteThread(cmd=cmd)
            elif self.rbtn_sub.isCheckable():
                self.thread = ExcuteThread(self.get_io_args("srt"),
                                           self.get_input_args(), {})
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
        self.encoder = value
        self.sld_crf.setMaximum(encoder_infos[value]["crf"]["max"])
        self.sld_crf.setValue(encoder_infos[value]["crf"]["default"])

    def btn_input_clicked(self):
        paths = QFileDialog.getOpenFileNames(
            self.MainWindow, "打开",  filter="所有文件 (*.*)")
        if paths[0]:
            index = self.table_input.rowCount()
            self.table_input.setRowCount(index+len(paths[0]))
            for path in paths[0]:
                row = self.table_input.rowCount()
                name, ext = os.path.splitext(path)
                self.table_input.setItem(index, 0, QTableWidgetItem(path))
                self.table_input.setItem(
                    index, 1, QTableWidgetItem(name))
                index += 1

        self.table_input.resizeColumnsToContents()

    def delete_selection(self):
        rows = self.table_input.selectionModel().selectedRows()
        for row in rows:
            self.table_input.removeRow(row.row())
            pass

    def setup_events(self):
        self.btn_start.clicked.connect(self.start)
        self.cbb_encoder.currentTextChanged.connect(self.encoder_changed)
        # self.cbb_encode_mode.currentIndexChanged.connect(
        #     self.encode_mode_changed)
        self.sld_crf.valueChanged.connect(
            lambda value: self.lbl_crf.setText(str(value)))
        self.sld_preset.valueChanged.connect(
            lambda value: self.lbl_preset.setText(str(presets[value]["desc"])))
        self.btn_input.clicked.connect(self.btn_input_clicked)
        self.btn_delete.clicked.connect(self.delete_selection)

    def setup_values(self):
        self.lbl_preset.setText(presets[self.sld_preset.value()]["desc"])
