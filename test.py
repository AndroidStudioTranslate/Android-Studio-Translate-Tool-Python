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
        self.comboBox_translate = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_translate.setObjectName("comboBox_translate")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.comboBox_translate.addItem("")
        self.gridLayout.addWidget(self.comboBox_translate, 0, 7, 1, 1)
        self.checkBox_translate = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_translate.setObjectName("checkBox_translate")
        self.gridLayout.addWidget(self.checkBox_translate, 0, 6, 1, 1)
        self.pushButton_watch = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_watch.setObjectName("pushButton_watch")
        self.gridLayout.addWidget(self.pushButton_watch, 0, 5, 1, 1)
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
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 657, 23))
        self.menubar.setObjectName("menubar")
        self.menu1 = QtWidgets.QMenu(self.menubar)
        self.menu1.setObjectName("menu1")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setStatusTip("")
        self.statusbar.setWhatsThis("")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_package = QtWidgets.QAction(MainWindow)
        self.action_package.setObjectName("action_package")
        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.action_git = QtWidgets.QAction(MainWindow)
        self.action_git.setObjectName("action_git")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.menu1.addAction(self.action_package)
        self.menu1.addSeparator()
        self.menu1.addAction(self.action_exit)
        self.menu.addAction(self.action_git)
        self.menu.addAction(self.action_about)
        self.menubar.addAction(self.menu1.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Android Studio翻译工具 By Wellchang"))
        self.comboBox_translate.setItemText(0, _translate("MainWindow", "中文"))
        self.comboBox_translate.setItemText(1, _translate("MainWindow", "繁体中文"))
        self.comboBox_translate.setItemText(2, _translate("MainWindow", "英语"))
        self.comboBox_translate.setItemText(3, _translate("MainWindow", "粤语"))
        self.comboBox_translate.setItemText(4, _translate("MainWindow", "文言文"))
        self.comboBox_translate.setItemText(5, _translate("MainWindow", "日语"))
        self.comboBox_translate.setItemText(6, _translate("MainWindow", "韩语"))
        self.comboBox_translate.setItemText(7, _translate("MainWindow", "法语"))
        self.comboBox_translate.setItemText(8, _translate("MainWindow", "西班牙语"))
        self.comboBox_translate.setItemText(9, _translate("MainWindow", "泰语"))
        self.comboBox_translate.setItemText(10, _translate("MainWindow", "阿拉伯语"))
        self.comboBox_translate.setItemText(11, _translate("MainWindow", "俄语"))
        self.comboBox_translate.setItemText(12, _translate("MainWindow", "葡萄牙语"))
        self.comboBox_translate.setItemText(13, _translate("MainWindow", "德语"))
        self.comboBox_translate.setItemText(14, _translate("MainWindow", "意大利语"))
        self.comboBox_translate.setItemText(15, _translate("MainWindow", "希腊语"))
        self.comboBox_translate.setItemText(16, _translate("MainWindow", "荷兰语"))
        self.comboBox_translate.setItemText(17, _translate("MainWindow", "波兰语"))
        self.comboBox_translate.setItemText(18, _translate("MainWindow", "保加利亚语"))
        self.comboBox_translate.setItemText(19, _translate("MainWindow", "爱沙尼亚语"))
        self.comboBox_translate.setItemText(20, _translate("MainWindow", "丹麦语"))
        self.comboBox_translate.setItemText(21, _translate("MainWindow", "芬兰语"))
        self.comboBox_translate.setItemText(22, _translate("MainWindow", "捷克语"))
        self.comboBox_translate.setItemText(23, _translate("MainWindow", "罗马尼亚语"))
        self.comboBox_translate.setItemText(24, _translate("MainWindow", "斯洛文尼亚语"))
        self.comboBox_translate.setItemText(25, _translate("MainWindow", "瑞典语"))
        self.comboBox_translate.setItemText(26, _translate("MainWindow", "匈牙利语"))
        self.comboBox_translate.setItemText(27, _translate("MainWindow", "越南语"))
        self.checkBox_translate.setText(_translate("MainWindow", "翻译"))
        self.pushButton_watch.setText(_translate("MainWindow", "查看"))
        self.lineEdit_watch.setPlaceholderText(_translate("MainWindow", "压缩包内文件路径"))
        self.pushButton_save.setText(_translate("MainWindow", "保存当前文件"))
        self.lineEdit_browser.setPlaceholderText(_translate("MainWindow", "选择汉化文件"))
        self.pushButton_browser.setText(_translate("MainWindow", "浏览"))
        self.progressBar.setFormat(_translate("MainWindow", "%v/%m"))
        self.menu1.setTitle(_translate("MainWindow", "文件"))
        self.menu.setTitle(_translate("MainWindow", "帮助"))
        self.action_package.setText(_translate("MainWindow", "打包"))
        self.action_exit.setText(_translate("MainWindow", "退出"))
        self.action_git.setText(_translate("MainWindow", "开源地址"))
        self.action_about.setText(_translate("MainWindow", "关于"))


