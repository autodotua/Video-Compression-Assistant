from vca.main_window_layout import Ui_MainWindow
from vca.excute_thread import *
from vca.print_redirect import PrintRedirect
from vca.dicts import *
from vca.tools import *
from vca.model.file_list_model import FileListModel
from vca.model.file_model import FileModel
from vca.model.output_model import OutputModel
from vca.model.config import Config
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
import pickle
import subprocess


class Application(Ui_MainWindow):
    converting = False
    config = Config.restore()

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
        icon.addPixmap(QPixmap("icon.ico"),
                       QIcon.Normal, QIcon.Off)
        self.MainWindow.setWindowIcon(icon)
        sys.exit(app.exec_())

    def setup_init_values(self):
        self.update_progress(None)
        self.files = FileListModel(self.config.files) if self.config.autosave else FileListModel()
        self.lst.setModel(self.files)
        self.lbl_preset.setText(presets[self.sld_preset.value()]["desc"])

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
            video_model.min_bitrate = self.txt_bitrate_min.value(
            ) if self.chk_bitrate_min.isChecked() else None
            video_model.fps = self.cbb_fps.currentText() if self.chk_fps.isChecked() else None
            model.extra_args = self.txt_filter_extra_args.toPlainText()

        audio_model = OutputModel.AudioFilterModel()
        mode_text = self.cbb_audio_mode.currentText
        if mode_text == "复制":
            audio_model.mode = "copy"
        elif mode_text == "编码":
            audio_model.mode = "encode"
            audio_model.bitrate = self.cbb_bitrate_a.currentText()
        else:
            audio_model.mode = "none"

        model.video_filter = video_model
        model.audio_filter = audio_model
        return model

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

    def update_progress(self, current):
        if current is None:
            self.lbl_current_file.setText("")
            self.lbl_current_frame_time.setText("")
            self.lbl_current_speed.setText("")
            self.lbl_current_bitrate.setText("")
            self.lbl_current_time.setText("")
            self.txt_current_cmd.setText("")
            self.prgb_current.setMaximum(100)
            self.prgb_current.reset()
        else:
            self.txt_current_cmd.setText(current.cmd)

            if current.unkown == True:
                self.prgb_current.setMaximum(0)

            else:
                self.lbl_current_file.setText(current.input.input)
                self.lbl_current_frame_time.setText(
                    "第"+current.frame + "帧  "+current.time)
                self.lbl_current_speed.setText(
                    current.fps + "FPS  "+current.speed+"×")
                self.lbl_current_bitrate.setText(
                    current.bitrate+"  q="+current.q)
                self.prgb_current.setMaximum(100)
                if current.percent:
                    self.prgb_current.setValue(int(current.percent*100))
                    self.lbl_current_time.setText(
                        "已用"+self.format_delta(current.elapsed) + "  剩余"+self.format_delta(current.left))

    def show_comparision_result(self, args):
        QMessageBox.information(
            None, "比较结果", "结构程度：\n"+args["ssim"].replace(" (", "（").replace(
                " ", "\n").replace("（", " (")+"\n\n信噪比：\n"+args["psnr"].replace(" ", "\n"))

    def save_config(self):
        self.config.files = self.files.files
        Config.save(self.config)

    def start(self):
        if self.converting:
            self.btn_start.setEnabled(False)
            self.thread.stop()
        else:
            if self.files.rowCount == 0:
                QMessageBox.critical(None, "错误", "还没有选择任何文件", QMessageBox.Ok)
                return
            self.save_config()
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

    def encoder_changed(self, value):
        self.sld_crf.setMaximum(encoder_infos[value]["crf"]["max"])
        self.sld_crf.setValue(encoder_infos[value]["crf"]["default"])

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
        Config.restore()
        pass

    def export_config(self):
        Config.save(Config())
        pass

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

        self.lst.dropped.connect(self.list_file_dropped)
        self.menu_import.triggered.connect(self.import_config)
        self.menu_export.triggered.connect(self.export_config)
