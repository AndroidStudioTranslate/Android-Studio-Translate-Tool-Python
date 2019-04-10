import hashlib
import os
import time
import zipfile
from concurrent.futures import thread
import _thread

import pyperclip
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QStringListModel, QThread, pyqtSignal, QAbstractTableModel, QModelIndex, Qt, QCoreApplication
from PyQt5.QtGui import QStandardItemModel, QCursor
from PyQt5.QtWidgets import QFileDialog, QAbstractItemView, QItemDelegate, QToolTip, QMenu, QDialog, QPushButton, \
    QLabel, QMessageBox

import BaiDuTranslate
import fileView
from BaiduConfigDialog import Ui_Dialog
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

    def __init__(self, values, toLanguage):
        super(TranslateThread, self).__init__()
        self.values = values
        self.toLanguage = toLanguage
        self.isStop = False

    def run(self):
        valueLens = len(self.values)
        print("将翻译" + str(valueLens) + "条")
        errorCode = -1
        errorMsg = '翻译完成'
        for index in range(valueLens):
            if self.isStop:
                errorCode = -2
                errorMsg = '翻译中断'
                break
            print(index)
            dst = BaiDuTranslate.getTranslateValue(self.values[index], toLanguage=self.toLanguage)
            self._signal.emit(index, dst)
        self._signal.emit(errorCode, errorMsg)

    def stop(self):
        self.isStop = True


class PackageThread(QThread):
    _signal = pyqtSignal(int, int)

    def __init__(self, filePath):
        super(PackageThread, self).__init__()
        self.filePath = filePath
        self.isStop = False

    def run(self):
        file_new = self.filePath + "_new.jar"
        zNew = zipfile.ZipFile(file_new, 'w', zipfile.ZIP_DEFLATED)
        count = 0
        for dirpath, dirnames, filenames in os.walk(self.filePath):  # os.walk 遍历目录
            for filename in filenames:
                count = count + 1
        indexFile = 0
        for dirpath, dirnames, filenames in os.walk(self.filePath):  # os.walk 遍历目录
            fpath = dirpath.replace(self.filePath, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''  # os.sep路径分隔符
            for filename in filenames:
                if self.isStop:
                    break
                zNew.write(os.path.join(dirpath, filename), fpath + filename)
                self._signal.emit(indexFile, count)
                indexFile = indexFile + 1
        self._signal.emit(-1, count)

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
                self.translateValues[index.row()] = value
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


class FielViewDialog(QtWidgets.QDialog, fileView.Ui_Dialog):
    def __init__(self, fileName):
        super(FielViewDialog, self).__init__()
        self.fileName = fileName
        self.setupUi(self)
        self.pushButton_update.clicked.connect(self.updateClick)
        fopen = open(self.fileName, 'r')
        self.textEdit_view.setText(fopen.read())

    def updateClick(self):
        s_open = open(self.fileName, 'w')
        s_open.write(self.textEdit_view.text())  # 将内容写入原文件
        s_open.close()


class BaiduTranslateDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(BaiduTranslateDialog, self).__init__()
        self.setupUi(self)
        self.pushButton_ok.clicked.connect(self.okClick)
        self.pushButton_cancel.clicked.connect(self.cancelClick)
        self.setFixedSize(203, 130)

    def okClick(self):
        appid = self.lineEdit_appid.text()
        sk = self.lineEdit_sk.text()
        if appid.strip() == '' and sk.strip() == '':
            self.label_tip.setText("请正确输入APP_ID和SECURITY_KEY")
            return
        propsConfig = property.parse("config.properties")
        propsConfig.set("APP_ID")
        propsConfig.set("SECURITY_KEY")
        propsConfig.saveKV()

    def cancelClick(self):
        self.close()


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
        self.isPackageDone = False
        self.isSaveProperties = False
        self.threadTranslate = None
        self.baiduConfigDialog = None
        self.fileViewDialog = None
        self.props = None
        self.language = [
            "zh",
            "cht",
            "en",
            "yue",
            "wyw",
            "jp",
            "kor",
            "fra",
            "spa",
            "th",
            "ara",
            "ru",
            "pt",
            "de",
            "it",
            "el",
            "nl",
            "pl",
            "bul",
            "est",
            "dan",
            "fin",
            "cs",
            "rom",
            "slo",
            "swe",
            "hu",
            "vie"
        ]
        self.setupUi(self)
        self.pushButton_browser.clicked.connect(self.selectLanguagePack)
        self.pushButton_watch.clicked.connect(self.openFile)
        self.listView_file.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁用双击编辑
        self.listView_file.clicked.connect(self.itemClick)  # 单击事件
        self.listView_file.doubleClicked.connect(self.itemDoubleClick)  # 双击事件
        self.msgLabel = QtWidgets.QLabel(self.statusbar)
        self.statusbar.addWidget(self.msgLabel)
        self.tableView_kv.horizontalHeader().setStretchLastSection(True)  # 设置最后一列填满表格剩余空间
        self.tableView_kv.setItemDelegateForColumn(0, EmptyDelegate(self))  # 设置第一列不可编辑
        self.tableView_kv.setItemDelegateForColumn(1, EmptyDelegate(self))  # 设置第二列不可编辑
        self.tableView_kv.doubleClicked['QModelIndex'].connect(self.tableViewDoubleClick)
        self.tableView_kv.clicked['QModelIndex'].connect(self.tableViewClick)
        self.tableView_kv.setContextMenuPolicy(
            Qt.CustomContextMenu)  # 右键菜单，如果不设为CustomContextMenu,无法使用customContextMenuRequested
        self.tableView_kv.customContextMenuRequested.connect(self.showContextMenu)
        self.pushButton_save.clicked.connect(self.saveProperties)
        self.action_exit.triggered.connect(QCoreApplication.quit)
        self.action_package.triggered.connect(self.actionPackageHandler)
        self.action_git.triggered.connect(self.actionGitHandler)
        self.action_about.triggered.connect(self.actionAboutHandler)
        self.lineEdit_browser.returnPressed.connect(self.readJar)
        self.lineEdit_watch.returnPressed.connect(self.openFile)
        self.isBaiduTranslateConfigValid = False
        self.checkBaiduConfig()

    def checkBaiduConfig(self):
        if self.isBaiduTranslateConfigValid:
            return
        self.isBaiduConfigExist = os.path.exists("config.properties")
        if self.isBaiduConfigExist:
            propBaidu = property.parse("config.properties")
            appid = propBaidu.get("APP_ID")
            sk = propBaidu.get('SECURITY_KEY')
            if appid.strip() == '' or sk.strip() == '':
                self.isBaiduTranslateConfigValid = False
            else:
                self.isBaiduTranslateConfigValid = True

    def showConfigBaiduTranslate(self):
        if self.baiduConfigDialog == None:
            self.baiduConfigDialog = BaiduTranslateDialog()
            self.baiduConfigDialog.setWindowModality(Qt.ApplicationModal)
        self.baiduConfigDialog.show()

    def closeEvent(self, QCloseEvent):
        if not self.isPackageDone and self.isSaveProperties:
            res = QMessageBox.question(self, "消息", "还没有打包,是否关闭", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if res == QMessageBox.Yes:
                QCloseEvent.accept()
            else:
                QCloseEvent.ignore()

    def openFile(self):
        watchFileName = self.lineEdit_watch.text()
        if watchFileName.strip() == '':
            return
        if self.fileViewDialog == None:
            self.fileViewDialog = FielViewDialog(self.filePath + "/" + watchFileName)
            self.fileViewDialog.setWindowModality(Qt.ApplicationModal)
        self.fileViewDialog.show()

    # 选择语言包
    def selectLanguagePack(self):
        self.fileName, self.fileType = QFileDialog.getOpenFileName(self,
                                                                   "选择语言包文件",
                                                                   "./",
                                                                   "语言包 (*.jar)")
        self.lineEdit_browser.setText(self.fileName)
        self.readJar()

    def readJar(self):
        self.fileName = self.lineEdit_browser.text()
        self.lineEdit_browser.setToolTip(self.fileName)
        self.filePath = self.fileName.replace('.jar', '')
        fileNameLens = len(self.fileName)
        if fileNameLens == 0:
            return
        fz = zipfile.ZipFile(self.fileName, 'r')
        self.fileNameList = fz.namelist()
        self.propertiesFileNameList = [element for element in self.fileNameList if element.endswith('.properties')]
        slm = QStringListModel()
        slm.setStringList(self.propertiesFileNameList)
        self.listView_file.setModel(slm)
        self.isExtractDone = False
        self.setMsg("读取文件中...")
        lens = len(self.fileNameList)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(lens)
        # 创建线程
        self.thread = MyThread(fz, self.filePath)
        # 连接信号
        self.thread._signal.connect(self.callBack)
        # 开始线程
        self.thread.start()

    def itemClick(self, qModelIndex):
        if self.isExtractDone:
            fileName = self.propertiesFileNameList[qModelIndex.row()]
            self.lineEdit_watch.setText(fileName)
            self.lineEdit_watch.setToolTip(fileName)
        else:
            self.setMsg("读取文件未完成")

    def itemDoubleClick(self, qModelIndex):
        self.isSaveProperties = False
        self.isPackageDone = False
        if self.isExtractDone:
            fileName = self.propertiesFileNameList[qModelIndex.row()]
            self.lineEdit_watch.setText(fileName)
            self.lineEdit_watch.setToolTip(fileName)
            self.keys.clear()
            self.values.clear()
            filePath = self.filePath + '\\' + fileName
            print(filePath)
            if self.props is not None:
                self.props.keys.clear()
                self.props.values.clear()
                self.props = None
            self.props = property.parse(filePath, True)
            self.keys = self.props.keys.copy()
            self.values = self.props.values.copy()
            self.translateValues = self.values.copy()
            self.tableView_kv.setModel(KVModel(self.keys, self.values, self.translateValues))
            keyLens = len(self.keys)
            print(keyLens)
            self.checkBaiduConfig()
            if self.checkBox_translate.isChecked():
                if self.isBaiduTranslateConfigValid:
                    self.progressBar.setMinimum(0)
                    self.progressBar.setMaximum(keyLens)
                    if self.threadTranslate is not None:
                        self.threadTranslate.stop()
                        self.threadTranslate.quit()
                        self.threadTranslate.wait()
                        self.threadTranslate = None
                    self.setMsg("正在翻译...")
                    # 创建线程
                    self.threadTranslate = TranslateThread(self.values, self.getToLanguage())
                    # 连接信号
                    self.threadTranslate._signal.connect(self.callBackTranslate)
                    # 开始线程
                    self.threadTranslate.start()
                else:
                    self.showConfigBaiduTranslate()
        else:
            self.setMsg("读取文件未完成")

    def getToLanguage(self):
        return self.language[self.comboBox_translate.currentIndex()]

    def tableViewClick(self, qModelIndex):
        self.tableViewDoubleClick(qModelIndex)

    def tableViewDoubleClick(self, qModelIndex):
        self.tableView_kv.edit(qModelIndex)
        row = qModelIndex.row()
        self.label.setText(self.values[row])
        copyStr = self.translateValues[row]
        pyperclip.copy(copyStr)

    def showContextMenu(self):
        self.tableView_kv.contextMenu = QMenu(self)
        actionTranslate = self.tableView_kv.contextMenu.addAction(u'翻译')
        actionCopy = self.tableView_kv.contextMenu.addAction(u'复制')
        actionReset = self.tableView_kv.contextMenu.addAction(u'重置')
        self.tableView_kv.contextMenu.popup(QCursor.pos())  # 2菜单显示的位置
        actionTranslate.triggered.connect(self.actionTranslateHandler)
        actionCopy.triggered.connect(self.actionCopyHandler)
        actionReset.triggered.connect(self.actionResetHandler)
        self.tableView_kv.contextMenu.show()

    def actionCopyHandler(self):
        qModelIndex = self.tableView_kv.currentIndex()
        row = qModelIndex.row()
        col = qModelIndex.column()
        if col < 2:
            copyStr = self.values[row]
        else:
            copyStr = self.translateValues[row]
        pyperclip.copy(copyStr)

    def actionPackageHandler(self):
        if bool(1 - (self.isExtractDone & self.isTranslateDone & self.isSaveProperties)):
            self.setMsg('未做修改')
            return
        self.setMsg('打包中...')
        self.progressBar.setMinimum(0)
        # 创建线程
        self.threadPackage = PackageThread(self.filePath)
        # 连接信号
        self.threadPackage._signal.connect(self.callBackPackage)
        # 开始线程
        self.threadPackage.start()

    def actionGitHandler(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl('https://github.com/AndroidStudioTranslate/Android-Studio-Translate-Tool-Python'))

    def actionAboutHandler(self):
        aboutDialog = QDialog()
        aboutDialog.setWindowTitle("关于")
        # 设置窗口的属性为ApplicationModal模态，用户只有关闭弹窗后，才能关闭主界面
        aboutDialog.setWindowModality(Qt.ApplicationModal)
        aboutDialog.setFixedSize(500, 100)
        aboutMsg = '本软件用于对Android Studio进行语言包翻译\nBy Wellchang\nhttps://github.com/AndroidStudioTranslate/Android-Studio-Translate-Tool-Python\n2019/03/25'
        aboutLabel = QLabel(aboutMsg, aboutDialog)
        aboutDialog.exec()

    def actionTranslateHandler(self):
        qModelIndex = self.tableView_kv.currentIndex()
        row = qModelIndex.row()
        self.checkBaiduConfig()
        if self.isBaiduTranslateConfigValid:
            dst = BaiDuTranslate.getTranslateValue(self.values[row], toLanguage=self.getToLanguage())
            if '{\'error_code\':' in dst:
                self.setMsg(dst)
            self.translateValues[row] = dst
            self.updateTableViewData(qModelIndex, dst)
        else:
            self.showConfigBaiduTranslate()

    def actionResetHandler(self):
        qModelIndex = self.tableView_kv.currentIndex()
        row = qModelIndex.row()
        self.updateTableViewData(qModelIndex, self.values[row])

    def updateTableViewData(self, qModelIndex, value):
        self.tableView_kv.model().setData(qModelIndex, value)

    def saveProperties(self):
        self.props.keys.clear()
        self.props.values.clear()
        self.props.keys = self.tableView_kv.model().keys
        self.props.values = self.tableView_kv.model().translateValues
        self.props.saveKV(True)
        self.setMsg('保存完毕!', 1)
        self.isSaveProperties = True

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
            self.setMsg(value, 1)
            print(value)
        elif index == -2:
            print(value)
        else:
            self.progressBar.setValue(index + 1)
            qModelIndex = self.tableView_kv.model().index(index, 2, QModelIndex())
            self.updateTableViewData(qModelIndex, value)
            self.tableView_kv.scrollTo(qModelIndex)
            if '{\'error_code\':' in value:
                self.setMsg(value)
                # self.threadTranslate.stop()

    def callBackPackage(self, index, total):
        if index == -1:
            self.isPackageDone = True
            self.setMsg("打包完成", 1)
            print("打包完成")
        else:
            self.progressBar.setMaximum(total)
            self.progressBar.setValue(index + 1)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
