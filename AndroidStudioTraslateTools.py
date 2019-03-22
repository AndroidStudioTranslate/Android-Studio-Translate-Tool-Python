import hashlib
import time
import zipfile
from concurrent.futures import thread
import _thread

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QStringListModel, QThread, pyqtSignal, QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QStandardItemModel, QCursor
from PyQt5.QtWidgets import QFileDialog, QAbstractItemView, QItemDelegate, QToolTip, QMenu

import BaiDuTranslate
from test import Ui_MainWindow
import property


class MyThread(QThread):
    _signal = pyqtSignal(int)

    def __init__(self, fz, filePath):
        super(MyThread, self).__init__()
        self.fz = fz
        self.fileNameList = fz.namelist()
        self.filePath = filePath

    def run(self):
        index = 0
        # self.progressBar.setMinimum(0)
        # self.progressBar.setMaximum(lens)
        for file in self.fileNameList:
            self.fz.extract(file, self.filePath)
            index = index + 1
            self._signal.emit(index)
        self._signal.emit(-1)


class TranslateThread(QThread):
    _signal = pyqtSignal(int, str)

    def __init__(self, values):
        super(TranslateThread, self).__init__()
        self.values = values
        self.isStop = False

    def run(self):
        valueLens = len(self.values)
        for index in range(valueLens):
            if self.isStop:
                break
            dst = BaiDuTranslate.getTranslateValue(self.values[index])
            self._signal.emit(index, dst)
        self._signal.emit(-1, '')

    def stop(self):
        self.isStop = True


class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


class KVModel(QAbstractTableModel):
    def __init__(self, keys, values, translateValues, headers=None):
        super().__init__()
        if headers is None:
            headers = ['键名', '键值', '翻译']
        self.datas = []  # 用来持有为View提供的数据，此类中用列表中嵌套列表来实现
        self.headers = headers
        self.keys = keys
        self.values = values
        self.translateValues = translateValues
        self.load()  # 初始化时，自动载入数据

    def load(self):
        self.beginResetModel()
        keyLens = len(self.keys)
        for index in range(keyLens):
            self.datas.append([self.keys[index], self.values[index], self.translateValues[index]])
        self.endResetModel()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.datas)):  # 无效的数据请求
            return None

        row, col = index.row(), index.column()
        data = self.datas[row]
        if role == Qt.DisplayRole:
            item = data[col]
            # if col == AGE:  # 还可以实现数据的转换显示或显示处理后的数据
            #     item = int(item)
            return item
        return None

    def rowCount(self, index=QModelIndex()):  # 必须实现的接口方法（返回数据行数）
        return len(self.datas)

    def columnCount(self, index=QModelIndex()):  # 必须实现的接口方法（返回数据列数）
        return len(self.headers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        # 实现标题行的定义
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.headers[section]
        return int(section + 1)

    # 以下为编辑功能所必须实现的方法
    def setData(self, index, value, role=Qt.EditRole):
        # 编辑后更新模型中的数据 View中编辑后，View会调用这个方法修改Model中的数据
        if index.isValid() and 0 <= index.row() < len(self.datas) and value:
            col = index.column()
            if col == len(self.headers) - 1:
                self.beginResetModel()
                self.datas[index.row()][col] = value
                self.endResetModel()
                return True
        return False

    def flags(self, index):  # 必须实现的接口方法，不实现，则View中数据不可编辑
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(
            QAbstractTableModel.flags(self, index) |
            Qt.ItemIsEditable | Qt.ItemIsSelectable)

    def insertRows(self, position, rows=1, index=QModelIndex()):
        # position 插入位置；rows 插入行数
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        pass  # 对self.datas进行操作
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=QModelIndex):
        # position 删除位置；rows 删除行数
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        pass  # 对self.datas进行操作
        self.endRemoveRows()
        return True


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.fileName = ''
        self.fileType = ''
        self.filePath = ''
        self.keys = []
        self.values = []
        self.translateValues = []
        self.fileNameList = []
        self.propertiesFileNameList = []
        self.isExtractDone = False
        self.isTranslateDone = False
        self.threadTranslate = None
        self.setupUi(self)
        self.pushButton.clicked.connect(self.selectLanguagePack)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁用双击编辑
        self.listView.clicked.connect(self.itemClick)  # 单击事件
        self.listView.doubleClicked.connect(self.itemDoubleClick)  # 双击事件
        self.msgLabel = QtWidgets.QLabel(self.statusbar)
        self.statusbar.addWidget(self.msgLabel)
        self.tableView.horizontalHeader().setStretchLastSection(True)  # 设置最后一列填满表格剩余空间
        self.tableView.setItemDelegateForColumn(0, EmptyDelegate(self))  # 设置第一列不可编辑
        self.tableView.setItemDelegateForColumn(1, EmptyDelegate(self))  # 设置第二列不可编辑
        self.tableView.doubleClicked['QModelIndex'].connect(self.tableViewDoubleClick)
        self.tableView.clicked['QModelIndex'].connect(self.tableViewClick)
        self.tableView.setContextMenuPolicy(
            Qt.CustomContextMenu)  # 右键菜单，如果不设为CustomContextMenu,无法使用customContextMenuRequested
        self.tableView.customContextMenuRequested.connect(self.showContextMenu)

    # 选择语言包
    def selectLanguagePack(self):
        self.fileName, self.fileType = QFileDialog.getOpenFileName(self,
                                                                   "选择语言包文件",
                                                                   "./",
                                                                   "语言包 (*.jar)")
        self.lineEdit.setText(self.fileName)
        self.lineEdit.setToolTip(self.fileName)
        self.filePath = self.fileName.replace('.jar', '')
        fileNameLens = len(self.fileName)
        if fileNameLens == 0:
            return
        fz = zipfile.ZipFile(self.fileName, 'r')
        self.fileNameList = fz.namelist()
        self.propertiesFileNameList = [element for element in self.fileNameList if element.endswith('.properties')]
        slm = QStringListModel()
        slm.setStringList(self.propertiesFileNameList)
        self.listView.setModel(slm)
        self.isExtractDone = False
        self.setMsg("读取文件中...")
        lens = len(self.fileNameList)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(lens)
        # _thread.start_new_thread(self.extractFile, (fz,))
        # 创建线程
        self.thread = MyThread(fz, self.filePath)
        # 连接信号
        self.thread._signal.connect(self.callBack)
        # 开始线程
        self.thread.start()

    def extractFile(self, fz):
        index = 0
        lens = len(self.fileNameList)
        # self.progressBar.setMinimum(0)
        # self.progressBar.setMaximum(lens)
        for file in self.fileNameList:
            fz.extract(file, self.filePath)
            index = index + 1
            # self.progressBar.setValue(index)
        self.isExtractDone = True
        self.setMsg("读取文件完成", 1)
        print("读取文件完成")

    def itemClick(self, qModelIndex):
        if self.isExtractDone:
            fileName = self.propertiesFileNameList[qModelIndex.row()]
            self.lineEdit_2.setText(fileName)
            self.lineEdit_2.setToolTip(fileName)
        else:
            self.setMsg("读取文件未完成")

    def itemDoubleClick(self, qModelIndex):
        if self.isExtractDone:
            fileName = self.propertiesFileNameList[qModelIndex.row()]
            self.lineEdit_2.setText(fileName)
            self.lineEdit_2.setToolTip(fileName)
            self.keys.clear()
            self.values.clear()
            filePath = self.filePath + '\\' + fileName
            print(filePath)
            props = property.parse(filePath)
            self.keys = props.keys
            self.values = props.values
            self.translateValues = self.values.copy()
            keyLens = len(self.keys)
            print(keyLens)
            self.tableView.setModel(KVModel(self.keys, self.values, self.translateValues))
            self.progressBar.setMinimum(0)
            self.progressBar.setMaximum(keyLens)
            if self.checkBox.isChecked():
                if self.threadTranslate is not None:
                    self.threadTranslate.stop()
                    self.threadTranslate.quit()
                    self.threadTranslate.wait()
                    self.threadTranslate = None
                self.setMsg("正在翻译...")
                # 创建线程
                self.threadTranslate = TranslateThread(self.values)
                # 连接信号
                self.threadTranslate._signal.connect(self.callBackTranslate)
                # 开始线程
                self.threadTranslate.start()
        else:
            self.setMsg("读取文件未完成")

    def tableViewClick(self, qModelIndex):
        self.tableViewDoubleClick(qModelIndex)

    def tableViewDoubleClick(self, qModelIndex):
        self.tableView.edit(qModelIndex)
        row = qModelIndex.row()
        self.label.setText(self.values[row])

    def showContextMenu(self):
        self.tableView.contextMenu = QMenu(self)
        actionTranslate = self.tableView.contextMenu.addAction(u'翻译')
        actionReset = self.tableView.contextMenu.addAction(u'重置')
        self.tableView.contextMenu.popup(QCursor.pos())  # 2菜单显示的位置
        actionTranslate.triggered.connect(self.actionTranslateHandler)
        actionReset.triggered.connect(self.actionResetHandler)
        self.tableView.contextMenu.show()

    def actionTranslateHandler(self):
        qModelIndex = self.tableView.currentIndex()
        row = qModelIndex.row()
        dst = BaiDuTranslate.getTranslateValue(self.values[row])
        self.translateValues[row] = dst
        # self.tableView.setModel(KVModel(self.keys, self.values, self.translateValues))
        self.updateTableViewData(qModelIndex, dst)

    def actionResetHandler(self):
        qModelIndex = self.tableView.currentIndex()
        row = qModelIndex.row()
        self.updateTableViewData(qModelIndex, self.values[row])

    def updateTableViewData(self, qModelIndex, value):
        self.tableView.model().setData(qModelIndex, value)

    def setMsg(self, msg, index=0):
        msgColor = 'black'
        if index == 0:
            msgColor = 'red'
        elif index == 1:
            msgColor = 'green'
        else:
            msgColor = 'black'
        self.msgLabel.setStyleSheet(" QLabel{ color: " + msgColor + " }")
        self.msgLabel.setText(msg)

    def callBack(self, index):
        if index == -1:
            self.isExtractDone = True
            self.setMsg("读取文件完成", 1)
            print("读取文件完成")
        else:
            self.progressBar.setValue(index)

    def callBackTranslate(self, index, value):
        if index == -1:
            self.isTranslateDone = True
            self.setMsg("翻译完成", 1)
            print("翻译完成")
        else:
            self.progressBar.setValue(index + 1)
            qModelIndex = self.tableView.model().index(index, 2, QModelIndex())
            print(index, end='', flush=True)
            print('>' + value)
            self.updateTableViewData(qModelIndex, value)
            self.tableView.scrollTo(qModelIndex)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
