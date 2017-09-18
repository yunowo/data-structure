# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_about_dialog(object):
    def setupUi(self, about_dialog):
        about_dialog.setObjectName("about_dialog")
        about_dialog.resize(380, 175)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        about_dialog.setFont(font)
        self.buttonbox = QtWidgets.QDialogButtonBox(about_dialog)
        self.buttonbox.setGeometry(QtCore.QRect(150, 130, 211, 32))
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonbox.setObjectName("buttonbox")
        self.header = QtWidgets.QLabel(about_dialog)
        self.header.setGeometry(QtCore.QRect(150, 20, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setObjectName("header")
        self.info = QtWidgets.QLabel(about_dialog)
        self.info.setGeometry(QtCore.QRect(150, 50, 201, 71))
        self.info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.info.setObjectName("info")
        self.logo = QtWidgets.QLabel(about_dialog)
        self.logo.setGeometry(QtCore.QRect(20, 20, 100, 100))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/icon/img/logo.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")

        self.retranslateUi(about_dialog)
        self.buttonbox.accepted.connect(about_dialog.accept)
        self.buttonbox.rejected.connect(about_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(about_dialog)

    def retranslateUi(self, about_dialog):
        _translate = QtCore.QCoreApplication.translate
        about_dialog.setWindowTitle(_translate("about_dialog", "关于"))
        self.header.setText(_translate("about_dialog", "面向英文文献的编辑与检索系统"))
        self.info.setText(_translate("about_dialog", "<html><head/><body><p>Version 0.1<br/></p><p>Copyright (C) 2017 Yun Liu</p></body></html>"))

from . import res_rc
