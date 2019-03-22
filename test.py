# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(657, 492)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 0, 7, 1, 1)
        self.checkBox_translate = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_translate.setObjectName("checkBox_translate")
        self.gridLayout.addWidget(self.checkBox_translate, 0, 6, 1, 1)
        self.pushButton_watch = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_watch.setObjectName("pushButton_watch")
        self.gridLayout.addWidget(self.pushButton_watch, 0, 5, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 1)
        self.lineEdit_watch = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_watch.setToolTip("")
        self.lineEdit_watch.setObjectName("lineEdit_watch")
        self.gridLayout.addWidget(self.lineEdit_watch, 0, 3, 1, 2)
        self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save.setObjectName("pushButton_save")
        self.gridLayout.addWidget(self.pushButton_save, 3, 7, 1, 1)
        self.lineEdit_browser = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_browser.setToolTip("")
        self.lineEdit_browser.setObjectName("lineEdit_browser")
        self.gridLayout.addWidget(self.lineEdit_browser, 0, 0, 1, 1)
        self.listView_file = QtWidgets.QListView(self.centralwidget)
        self.listView_file.setObjectName("listView_file")
        self.gridLayout.addWidget(self.listView_file, 1, 6, 1, 2)
        self.pushButton_browser = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_browser.setObjectName("pushButton_browser")
        self.gridLayout.addWidget(self.pushButton_browser, 0, 2, 1, 1)
        self.tableView_kv = QtWidgets.QTableView(self.centralwidget)
        self.tableView_kv.setObjectName("tableView_kv")
        self.gridLayout.addWidget(self.tableView_kv, 1, 0, 1, 6)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 8)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 657, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox.setItemText(0, _translate("MainWindow", "中文"))
        self.checkBox_translate.setText(_translate("MainWindow", "翻译"))
        self.pushButton_watch.setText(_translate("MainWindow", "查看"))
        self.lineEdit_watch.setPlaceholderText(_translate("MainWindow", "压缩包内文件路径"))
        self.pushButton_save.setText(_translate("MainWindow", "保存当前文件"))
        self.lineEdit_browser.setPlaceholderText(_translate("MainWindow", "选择汉化文件"))
        self.pushButton_browser.setText(_translate("MainWindow", "浏览"))


