# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BaiduConfigDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(221, 124)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_appid = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_appid.setObjectName("lineEdit_appid")
        self.gridLayout.addWidget(self.lineEdit_appid, 0, 0, 1, 2)
        self.lineEdit_sk = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_sk.setObjectName("lineEdit_sk")
        self.gridLayout.addWidget(self.lineEdit_sk, 1, 0, 1, 2)
        self.label_tip = QtWidgets.QLabel(Dialog)
        self.label_tip.setMaximumSize(QtCore.QSize(203, 25))
        self.label_tip.setText("")
        self.label_tip.setObjectName("label_tip")
        self.gridLayout.addWidget(self.label_tip, 2, 0, 1, 2)
        self.pushButton_ok = QtWidgets.QPushButton(Dialog)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.gridLayout.addWidget(self.pushButton_ok, 3, 0, 1, 1)
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.gridLayout.addWidget(self.pushButton_cancel, 3, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "配置百度翻译"))
        self.lineEdit_appid.setPlaceholderText(_translate("Dialog", "请输入百度翻译APP_ID"))
        self.lineEdit_sk.setPlaceholderText(_translate("Dialog", "请输入百度翻译SECURITY_KEY"))
        self.pushButton_ok.setText(_translate("Dialog", "保存"))
        self.pushButton_cancel.setText(_translate("Dialog", "取消"))


