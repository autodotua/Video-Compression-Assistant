# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\autod\OneDrive\同步\开发\视频压制助手\vca\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1126, 930)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lst = QtWidgets.QListView(self.groupBox_6)
        self.lst.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lst.setObjectName("lst")
        self.gridLayout.addWidget(self.lst, 0, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.btn_input = QtWidgets.QPushButton(self.groupBox_6)
        self.btn_input.setObjectName("btn_input")
        self.gridLayout.addWidget(self.btn_input, 1, 1, 1, 1)
        self.btn_delete = QtWidgets.QPushButton(self.groupBox_6)
        self.btn_delete.setAutoFillBackground(False)
        self.btn_delete.setObjectName("btn_delete")
        self.gridLayout.addWidget(self.btn_delete, 1, 2, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout)
        self.gpb_file = QtWidgets.QGroupBox(self.groupBox_6)
        self.gpb_file.setEnabled(False)
        self.gpb_file.setObjectName("gpb_file")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.gpb_file)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_18 = QtWidgets.QLabel(self.gpb_file)
        self.label_18.setObjectName("label_18")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.txt_input = QtWidgets.QLineEdit(self.gpb_file)
        self.txt_input.setObjectName("txt_input")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_input)
        self.label_19 = QtWidgets.QLabel(self.gpb_file)
        self.label_19.setObjectName("label_19")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_19)
        self.txt_output = QtWidgets.QLineEdit(self.gpb_file)
        self.txt_output.setObjectName("txt_output")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_output)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.time_from = QtWidgets.QTimeEdit(self.gpb_file)
        self.time_from.setEnabled(False)
        self.time_from.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
        self.time_from.setObjectName("time_from")
        self.horizontalLayout_3.addWidget(self.time_from)
        self.label_20 = QtWidgets.QLabel(self.gpb_file)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_3.addWidget(self.label_20)
        self.time_to = QtWidgets.QTimeEdit(self.gpb_file)
        self.time_to.setEnabled(False)
        self.time_to.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
        self.time_to.setObjectName("time_to")
        self.horizontalLayout_3.addWidget(self.time_to)
        self.formLayout_2.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.chk_cut = QtWidgets.QCheckBox(self.gpb_file)
        self.chk_cut.setObjectName("chk_cut")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.chk_cut)
        self.gridLayout_4.addLayout(self.formLayout_2, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.chk_force_ext = QtWidgets.QCheckBox(self.gpb_file)
        self.chk_force_ext.setObjectName("chk_force_ext")
        self.gridLayout_3.addWidget(self.chk_force_ext, 1, 0, 1, 2)
        self.chk_input_fps = QtWidgets.QCheckBox(self.gpb_file)
        self.chk_input_fps.setObjectName("chk_input_fps")
        self.gridLayout_3.addWidget(self.chk_input_fps, 2, 0, 1, 1)
        self.cbb_input_fps = QtWidgets.QComboBox(self.gpb_file)
        self.cbb_input_fps.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhFormattedNumbersOnly|QtCore.Qt.ImhPreferNumbers)
        self.cbb_input_fps.setEditable(True)
        self.cbb_input_fps.setObjectName("cbb_input_fps")
        self.cbb_input_fps.addItem("")
        self.cbb_input_fps.addItem("")
        self.cbb_input_fps.addItem("")
        self.cbb_input_fps.addItem("")
        self.cbb_input_fps.addItem("")
        self.cbb_input_fps.addItem("")
        self.cbb_input_fps.addItem("")
        self.cbb_input_fps.addItem("")
        self.cbb_input_fps.addItem("")
        self.cbb_input_fps.addItem("")
        self.cbb_input_fps.addItem("")
        self.cbb_input_fps.addItem("")
        self.cbb_input_fps.addItem("")
        self.gridLayout_3.addWidget(self.cbb_input_fps, 2, 1, 1, 1)
        self.chk_image_seq = QtWidgets.QCheckBox(self.gpb_file)
        self.chk_image_seq.setObjectName("chk_image_seq")
        self.gridLayout_3.addWidget(self.chk_image_seq, 0, 0, 1, 2)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.btn_io_reset = QtWidgets.QPushButton(self.gpb_file)
        self.btn_io_reset.setObjectName("btn_io_reset")
        self.horizontalLayout_6.addWidget(self.btn_io_reset)
        self.btn_io_save = QtWidgets.QPushButton(self.gpb_file)
        self.btn_io_save.setObjectName("btn_io_save")
        self.horizontalLayout_6.addWidget(self.btn_io_save)
        self.gridLayout_4.addLayout(self.horizontalLayout_6, 1, 0, 1, 2)
        self.horizontalLayout_5.addLayout(self.gridLayout_4)
        self.horizontalLayout_4.addWidget(self.gpb_file)
        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 3)
        self.verticalLayout_2.addWidget(self.groupBox_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 952, 305))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.grpb_audio = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.grpb_audio.setCheckable(True)
        self.grpb_audio.setChecked(False)
        self.grpb_audio.setObjectName("grpb_audio")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.grpb_audio)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_25 = QtWidgets.QLabel(self.grpb_audio)
        self.label_25.setObjectName("label_25")
        self.gridLayout_8.addWidget(self.label_25, 0, 0, 1, 1)
        self.cbb_bitrate_a = QtWidgets.QComboBox(self.grpb_audio)
        self.cbb_bitrate_a.setEditable(True)
        self.cbb_bitrate_a.setObjectName("cbb_bitrate_a")
        self.cbb_bitrate_a.addItem("")
        self.cbb_bitrate_a.addItem("")
        self.cbb_bitrate_a.addItem("")
        self.cbb_bitrate_a.addItem("")
        self.cbb_bitrate_a.addItem("")
        self.cbb_bitrate_a.addItem("")
        self.gridLayout_8.addWidget(self.cbb_bitrate_a, 0, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.grpb_audio)
        self.label_26.setObjectName("label_26")
        self.gridLayout_8.addWidget(self.label_26, 0, 2, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.grpb_audio, 0, 1, 1, 1)
        self.grpb_video = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpb_video.sizePolicy().hasHeightForWidth())
        self.grpb_video.setSizePolicy(sizePolicy)
        self.grpb_video.setCheckable(True)
        self.grpb_video.setObjectName("grpb_video")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.grpb_video)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtWidgets.QLabel(self.grpb_video)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 1, 1, 1)
        self.chk_crf = QtWidgets.QCheckBox(self.grpb_video)
        self.chk_crf.setText("")
        self.chk_crf.setChecked(True)
        self.chk_crf.setObjectName("chk_crf")
        self.gridLayout_2.addWidget(self.chk_crf, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.grpb_video)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 6, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.grpb_video)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.grpb_video)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 5, 3, 1, 1)
        self.cbb_encoder = QtWidgets.QComboBox(self.grpb_video)
        self.cbb_encoder.setObjectName("cbb_encoder")
        self.cbb_encoder.addItem("")
        self.cbb_encoder.addItem("")
        self.cbb_encoder.addItem("")
        self.gridLayout_2.addWidget(self.cbb_encoder, 0, 2, 1, 1)
        self.cbb_fps = QtWidgets.QComboBox(self.grpb_video)
        self.cbb_fps.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhFormattedNumbersOnly|QtCore.Qt.ImhPreferNumbers)
        self.cbb_fps.setEditable(True)
        self.cbb_fps.setObjectName("cbb_fps")
        self.cbb_fps.addItem("")
        self.cbb_fps.addItem("")
        self.cbb_fps.addItem("")
        self.cbb_fps.addItem("")
        self.cbb_fps.addItem("")
        self.cbb_fps.addItem("")
        self.cbb_fps.addItem("")
        self.cbb_fps.addItem("")
        self.cbb_fps.addItem("")
        self.cbb_fps.addItem("")
        self.cbb_fps.addItem("")
        self.cbb_fps.addItem("")
        self.cbb_fps.addItem("")
        self.gridLayout_2.addWidget(self.cbb_fps, 4, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.grpb_video)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.grpb_video)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 4, 1, 1, 1)
        self.txt_bitrate_max = QtWidgets.QDoubleSpinBox(self.grpb_video)
        self.txt_bitrate_max.setDecimals(1)
        self.txt_bitrate_max.setMaximum(500.0)
        self.txt_bitrate_max.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)
        self.txt_bitrate_max.setProperty("value", 20.0)
        self.txt_bitrate_max.setObjectName("txt_bitrate_max")
        self.gridLayout_2.addWidget(self.txt_bitrate_max, 6, 2, 1, 1)
        self.sld_crf = QtWidgets.QSlider(self.grpb_video)
        self.sld_crf.setMaximum(99)
        self.sld_crf.setPageStep(2)
        self.sld_crf.setProperty("value", 28)
        self.sld_crf.setOrientation(QtCore.Qt.Horizontal)
        self.sld_crf.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld_crf.setTickInterval(5)
        self.sld_crf.setObjectName("sld_crf")
        self.gridLayout_2.addWidget(self.sld_crf, 2, 2, 1, 1)
        self.sld_preset = QtWidgets.QSlider(self.grpb_video)
        self.sld_preset.setMinimum(-5)
        self.sld_preset.setMaximum(3)
        self.sld_preset.setPageStep(1)
        self.sld_preset.setOrientation(QtCore.Qt.Horizontal)
        self.sld_preset.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld_preset.setObjectName("sld_preset")
        self.gridLayout_2.addWidget(self.sld_preset, 1, 2, 1, 1)
        self.chk_size = QtWidgets.QCheckBox(self.grpb_video)
        self.chk_size.setText("")
        self.chk_size.setObjectName("chk_size")
        self.gridLayout_2.addWidget(self.chk_size, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.grpb_video)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 1, 1, 1)
        self.lbl_preset = QtWidgets.QLabel(self.grpb_video)
        self.lbl_preset.setObjectName("lbl_preset")
        self.gridLayout_2.addWidget(self.lbl_preset, 1, 3, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.grpb_video)
        self.label_24.setObjectName("label_24")
        self.gridLayout_2.addWidget(self.label_24, 5, 1, 1, 1)
        self.txt_size = QtWidgets.QLineEdit(self.grpb_video)
        self.txt_size.setObjectName("txt_size")
        self.gridLayout_2.addWidget(self.txt_size, 3, 2, 1, 1)
        self.txt_bitrate = QtWidgets.QDoubleSpinBox(self.grpb_video)
        self.txt_bitrate.setDecimals(1)
        self.txt_bitrate.setMaximum(500.0)
        self.txt_bitrate.setProperty("value", 10.0)
        self.txt_bitrate.setObjectName("txt_bitrate")
        self.gridLayout_2.addWidget(self.txt_bitrate, 5, 2, 1, 1)
        self.chk_fps = QtWidgets.QCheckBox(self.grpb_video)
        self.chk_fps.setText("")
        self.chk_fps.setObjectName("chk_fps")
        self.gridLayout_2.addWidget(self.chk_fps, 4, 0, 1, 1)
        self.chk_bitrate_max = QtWidgets.QCheckBox(self.grpb_video)
        self.chk_bitrate_max.setText("")
        self.chk_bitrate_max.setObjectName("chk_bitrate_max")
        self.gridLayout_2.addWidget(self.chk_bitrate_max, 6, 0, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.grpb_video)
        self.label_23.setObjectName("label_23")
        self.gridLayout_2.addWidget(self.label_23, 0, 1, 1, 1)
        self.lbl_crf = QtWidgets.QLabel(self.grpb_video)
        self.lbl_crf.setObjectName("lbl_crf")
        self.gridLayout_2.addWidget(self.lbl_crf, 2, 3, 1, 1)
        self.chk_bitrate = QtWidgets.QCheckBox(self.grpb_video)
        self.chk_bitrate.setText("")
        self.chk_bitrate.setObjectName("chk_bitrate")
        self.gridLayout_2.addWidget(self.chk_bitrate, 5, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.grpb_video)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 6, 3, 1, 1)
        self.chk_bitrate_min = QtWidgets.QCheckBox(self.grpb_video)
        self.chk_bitrate_min.setText("")
        self.chk_bitrate_min.setObjectName("chk_bitrate_min")
        self.gridLayout_2.addWidget(self.chk_bitrate_min, 7, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.grpb_video)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 7, 1, 1, 1)
        self.txt_bitrate_min = QtWidgets.QDoubleSpinBox(self.grpb_video)
        self.txt_bitrate_min.setDecimals(1)
        self.txt_bitrate_min.setMaximum(500.0)
        self.txt_bitrate_min.setObjectName("txt_bitrate_min")
        self.gridLayout_2.addWidget(self.txt_bitrate_min, 7, 2, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.grpb_video)
        self.label_17.setObjectName("label_17")
        self.gridLayout_2.addWidget(self.label_17, 7, 3, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.grpb_video, 0, 0, 2, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.gridGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.gridGroupBox.setObjectName("gridGroupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.gridGroupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.rbtn_convert = QtWidgets.QRadioButton(self.gridGroupBox)
        self.rbtn_convert.setChecked(True)
        self.rbtn_convert.setObjectName("rbtn_convert")
        self.verticalLayout_4.addWidget(self.rbtn_convert)
        self.rbtn_compare = QtWidgets.QRadioButton(self.gridGroupBox)
        self.rbtn_compare.setObjectName("rbtn_compare")
        self.verticalLayout_4.addWidget(self.rbtn_compare)
        self.rbtn_sub = QtWidgets.QRadioButton(self.gridGroupBox)
        self.rbtn_sub.setObjectName("rbtn_sub")
        self.verticalLayout_4.addWidget(self.rbtn_sub)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.btn_start = QtWidgets.QPushButton(self.gridGroupBox)
        self.btn_start.setObjectName("btn_start")
        self.verticalLayout_4.addWidget(self.btn_start)
        self.horizontalLayout_2.addWidget(self.gridGroupBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txt_log = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_log.setReadOnly(True)
        self.txt_log.setObjectName("txt_log")
        self.horizontalLayout.addWidget(self.txt_log)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(7, -1, -1, -1)
        self.formLayout.setObjectName("formLayout")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.lbl_current_file = QtWidgets.QLabel(self.centralwidget)
        self.lbl_current_file.setObjectName("lbl_current_file")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lbl_current_file)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.lbl_current_frame_time = QtWidgets.QLabel(self.centralwidget)
        self.lbl_current_frame_time.setObjectName("lbl_current_frame_time")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lbl_current_frame_time)
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.lbl_current_speed = QtWidgets.QLabel(self.centralwidget)
        self.lbl_current_speed.setObjectName("lbl_current_speed")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lbl_current_speed)
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setObjectName("label_15")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.lbl_current_time = QtWidgets.QLabel(self.centralwidget)
        self.lbl_current_time.setObjectName("lbl_current_time")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lbl_current_time)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.lbl_current_bitrate = QtWidgets.QLabel(self.centralwidget)
        self.lbl_current_bitrate.setObjectName("lbl_current_bitrate")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lbl_current_bitrate)
        self.prgb_current = QtWidgets.QProgressBar(self.centralwidget)
        self.prgb_current.setProperty("value", 0)
        self.prgb_current.setObjectName("prgb_current")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.prgb_current)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(5, QtWidgets.QFormLayout.SpanningRole, spacerItem3)
        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1126, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.cbb_input_fps.setCurrentIndex(6)
        self.cbb_bitrate_a.setCurrentIndex(2)
        self.cbb_encoder.setCurrentIndex(1)
        self.cbb_fps.setCurrentIndex(6)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "视频压制助手"))
        self.groupBox_6.setTitle(_translate("MainWindow", "输入/输出"))
        self.btn_input.setText(_translate("MainWindow", "添加.."))
        self.btn_delete.setText(_translate("MainWindow", "删除"))
        self.gpb_file.setTitle(_translate("MainWindow", "参数"))
        self.label_18.setText(_translate("MainWindow", "输入："))
        self.label_19.setText(_translate("MainWindow", "输出："))
        self.time_from.setDisplayFormat(_translate("MainWindow", "H:mm:ss"))
        self.label_20.setText(_translate("MainWindow", "—"))
        self.time_to.setDisplayFormat(_translate("MainWindow", "H:mm:ss"))
        self.chk_cut.setText(_translate("MainWindow", "裁剪："))
        self.chk_force_ext.setText(_translate("MainWindow", "强制使用指定扩展名"))
        self.chk_input_fps.setText(_translate("MainWindow", "输入帧率："))
        self.cbb_input_fps.setItemText(0, _translate("MainWindow", "10"))
        self.cbb_input_fps.setItemText(1, _translate("MainWindow", "20"))
        self.cbb_input_fps.setItemText(2, _translate("MainWindow", "23.976"))
        self.cbb_input_fps.setItemText(3, _translate("MainWindow", "24"))
        self.cbb_input_fps.setItemText(4, _translate("MainWindow", "25"))
        self.cbb_input_fps.setItemText(5, _translate("MainWindow", "29.97"))
        self.cbb_input_fps.setItemText(6, _translate("MainWindow", "30"))
        self.cbb_input_fps.setItemText(7, _translate("MainWindow", "48"))
        self.cbb_input_fps.setItemText(8, _translate("MainWindow", "59.94"))
        self.cbb_input_fps.setItemText(9, _translate("MainWindow", "60"))
        self.cbb_input_fps.setItemText(10, _translate("MainWindow", "72"))
        self.cbb_input_fps.setItemText(11, _translate("MainWindow", "90"))
        self.cbb_input_fps.setItemText(12, _translate("MainWindow", "144"))
        self.chk_image_seq.setText(_translate("MainWindow", "图像序列"))
        self.btn_io_reset.setText(_translate("MainWindow", "重置"))
        self.btn_io_save.setText(_translate("MainWindow", "保存"))
        self.groupBox.setTitle(_translate("MainWindow", "视频编码"))
        self.grpb_audio.setTitle(_translate("MainWindow", "重编码音频"))
        self.label_25.setText(_translate("MainWindow", "平均码率:"))
        self.cbb_bitrate_a.setItemText(0, _translate("MainWindow", "64"))
        self.cbb_bitrate_a.setItemText(1, _translate("MainWindow", "96"))
        self.cbb_bitrate_a.setItemText(2, _translate("MainWindow", "128"))
        self.cbb_bitrate_a.setItemText(3, _translate("MainWindow", "196"))
        self.cbb_bitrate_a.setItemText(4, _translate("MainWindow", "256"))
        self.cbb_bitrate_a.setItemText(5, _translate("MainWindow", "320"))
        self.label_26.setText(_translate("MainWindow", "Kbps"))
        self.grpb_video.setTitle(_translate("MainWindow", "重编码视频"))
        self.label_6.setText(_translate("MainWindow", "CRF："))
        self.label_2.setText(_translate("MainWindow", "最大码率"))
        self.label.setText(_translate("MainWindow", "预设："))
        self.label_5.setText(_translate("MainWindow", "Mbps"))
        self.cbb_encoder.setItemText(0, _translate("MainWindow", "H.264"))
        self.cbb_encoder.setItemText(1, _translate("MainWindow", "H.265"))
        self.cbb_encoder.setItemText(2, _translate("MainWindow", "VP9"))
        self.cbb_fps.setItemText(0, _translate("MainWindow", "10"))
        self.cbb_fps.setItemText(1, _translate("MainWindow", "20"))
        self.cbb_fps.setItemText(2, _translate("MainWindow", "23.976"))
        self.cbb_fps.setItemText(3, _translate("MainWindow", "24"))
        self.cbb_fps.setItemText(4, _translate("MainWindow", "25"))
        self.cbb_fps.setItemText(5, _translate("MainWindow", "29.97"))
        self.cbb_fps.setItemText(6, _translate("MainWindow", "30"))
        self.cbb_fps.setItemText(7, _translate("MainWindow", "48"))
        self.cbb_fps.setItemText(8, _translate("MainWindow", "59.94"))
        self.cbb_fps.setItemText(9, _translate("MainWindow", "60"))
        self.cbb_fps.setItemText(10, _translate("MainWindow", "72"))
        self.cbb_fps.setItemText(11, _translate("MainWindow", "90"))
        self.cbb_fps.setItemText(12, _translate("MainWindow", "144"))
        self.label_7.setText(_translate("MainWindow", "Fps"))
        self.label_4.setText(_translate("MainWindow", "帧率："))
        self.label_3.setText(_translate("MainWindow", "分辨率："))
        self.lbl_preset.setText(_translate("MainWindow", "平衡"))
        self.label_24.setText(_translate("MainWindow", "平均码率:"))
        self.label_23.setText(_translate("MainWindow", "编码："))
        self.lbl_crf.setText(_translate("MainWindow", "28"))
        self.label_8.setText(_translate("MainWindow", "Mbps"))
        self.label_16.setText(_translate("MainWindow", "最小码率"))
        self.label_17.setText(_translate("MainWindow", "Mbps"))
        self.gridGroupBox.setTitle(_translate("MainWindow", "执行"))
        self.rbtn_convert.setText(_translate("MainWindow", "视频转换"))
        self.rbtn_compare.setText(_translate("MainWindow", "视频比较"))
        self.rbtn_sub.setText(_translate("MainWindow", "提取字幕"))
        self.btn_start.setText(_translate("MainWindow", "开始"))
        self.label_11.setText(_translate("MainWindow", "当前文件："))
        self.lbl_current_file.setText(_translate("MainWindow", "TextLabel"))
        self.label_13.setText(_translate("MainWindow", "帧/时间："))
        self.lbl_current_frame_time.setText(_translate("MainWindow", "TextLabel"))
        self.label_14.setText(_translate("MainWindow", "速度："))
        self.lbl_current_speed.setText(_translate("MainWindow", "TextLabel"))
        self.label_15.setText(_translate("MainWindow", "时间："))
        self.lbl_current_time.setText(_translate("MainWindow", "TextLabel"))
        self.label_12.setText(_translate("MainWindow", "码率："))
        self.lbl_current_bitrate.setText(_translate("MainWindow", "TextLabel"))
