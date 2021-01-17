from PyQt5.QtCore import *
from PyQt5 import *
from vca.model.file_model import FileModel
import os


class FileListModel(QAbstractListModel):

    InputRole = Qt.UserRole + 1
    OutputRole = Qt.UserRole + 2
    CutRole = Qt.UserRole + 3
    CutFromRole = Qt.UserRole + 4
    CutToRole = Qt.UserRole + 5
    ImageSeqRole = Qt.UserRole + 6
    ForceExtRole = Qt.UserRole + 7
    InputFpsRole = Qt.UserRole+8

    def file_args_list_to_dict(list):
        return {'input': list[0], 'output': list[1],
                "cut": list[2], "cut_from": list[3], "cut_to": list[4],
                "image_seq": list[5], "force_ext": list[6], "input_fps": list[7]}

    fileChanged = pyqtSignal()

    @property
    def files(self):
        return self._files

    def __init__(self, files=[]):
        super().__init__(None)
        self._files = files

    def data(self, index, role=Qt.DisplayRole):
        if isinstance(index, QModelIndex):
            row = index.row()
        else:
            row = index

        if role == Qt.DisplayRole:
            return os.path.basename(self._files[row].input)
        else:
            return None
            # if role in self.roleNames():
            #     return self.files[row][self.roleNames()[role].decode("utf8")]
        # if role == FileModel.InputRole:
        #     return self.files[row]["input"]
        # elif role == FileModel.OutputRole:
        #     return self.files[row]["output"]
        # elif role == Qt.DisplayRole:
        #     return os.path.basename(self.files[row]["input"])
        # elif role == FileModel.CutRole:
        #     return self.files[row]["cut"]
        # elif role == FileModel.CutFromRole:
        #     return self.files[row]["cut_from"]
        # elif role == FileModel.CutToRole:
        #     return self.files[row]["cut_to"]
        # elif role == FileModel.ImageSeqRole:
        #     return self.files[row]["image_seq"]
        # elif role == FileModel.ForceExtRole:
        #     return self.files[row]["force_ext"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.files)

    # def roleNames(self):
    #     return {
    #         FileListModel.InputRole: b'input',
    #         FileListModel.OutputRole: b'output',
    #         FileListModel.CutRole: b'cut',
    #         FileListModel.CutToRole: b'cut_to',
    #         FileListModel.CutFromRole: b'cut_from',
    #         FileListModel.ImageSeqRole:b"image_seq",
    #         FileListModel.ForceExtRole:b"force_ext",
    #         FileListModel.InputFpsRole:b"input_fps"
    #     }

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
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.files[row]
        self.endRemoveRows()

    @pyqtSlot()
    def removeAllFiles(self):
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount()-1)
        self.files.clear()
        self.endRemoveRows()
