from PyQt5.QtCore import *
from PyQt5 import *
import os


class FileModel(QAbstractListModel):

    InputRole = Qt.UserRole + 1
    OutputRole = Qt.UserRole + 2
    CutRole = Qt.UserRole + 3
    CutFromRole = Qt.UserRole + 4
    CutToRole = Qt.UserRole + 5
    ImageSeqRole = Qt.UserRole +6
    ForceExtRole = Qt.UserRole +7

    def file_args_list_to_dict(list):
        return {'input': list[0],'output': list[1],
            "cut": list[2], "cut_from": list[3], "cut_to": list[4],
            "image_seq":list[5],"force_ext":list[6]}

    fileChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.files =[FileModel.file_args_list_to_dict( [r'J:\临时\0123\DJI_0131%04d.bmp',
             r'J:\临时\0123\DJI_0131.mp4',
              False,  0,  0,True,False])]

    def data(self, index, role=Qt.DisplayRole):
        if isinstance(index , QModelIndex):
            row = index.row()
        else:
            row=index
        if role == FileModel.InputRole:
            return self.files[row]["input"]
        elif role == FileModel.OutputRole:
            return self.files[row]["output"]
        elif role == Qt.DisplayRole:
            return os.path.basename(self.files[row]["input"])
        elif role == FileModel.CutRole:
            return self.files[row]["cut"]
        elif role == FileModel.CutFromRole:
            return self.files[row]["cut_from"]
        elif role == FileModel.CutToRole:
            return self.files[row]["cut_to"]
        elif role == FileModel.ImageSeqRole:
            return self.files[row]["image_seq"]
        elif role == FileModel.ForceExtRole:
            return self.files[row]["force_ext"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.files)

    def roleNames(self):
        return {
            FileModel.InputRole: b'input',
            FileModel.OutputRole: b'output',
            FileModel.CutRole: b'cut',
            FileModel.CutToRole: b'cut_to',
            FileModel.CutFromRole: b'cut_from',
            FileModel.ImageSeqRole:b"image_seq",
            FileModel.ForceExtRole:b"force_ext"
        }

    @pyqtSlot(str, int)
    def addFile(self, item):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.files.append(item)
        self.endInsertRows()

    @pyqtSlot(int, str, int)
    def editFile(self, row, item):
        ix = self.index(row, 0)
        self.files[row] = item
        self.dataChanged.emit(ix, ix, self.roleNames())

    @pyqtSlot(int)
    def removeFile(self, row):
        self.beginRemoveColumns(QModelIndex(), row, row)
        del self.files[row]
        self.endRemoveRows()
