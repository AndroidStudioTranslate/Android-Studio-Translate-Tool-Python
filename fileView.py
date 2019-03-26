# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fileView.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 292)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit_view = QtWidgets.QTextEdit(Dialog)
        self.textEdit_view.setObjectName("textEdit_view")
        self.gridLayout.addWidget(self.textEdit_view, 0, 0, 1, 1)
        self.pushButton_update = QtWidgets.QPushButton(Dialog)
        self.pushButton_update.setObjectName("pushButton_update")
        self.gridLayout.addWidget(self.pushButton_update, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "查看文件"))
        self.pushButton_update.setText(_translate("Dialog", "修改"))


