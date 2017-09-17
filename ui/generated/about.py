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
        about_dialog.resize(388, 202)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        about_dialog.setFont(font)
        self.buttonBox = QtWidgets.QDialogButtonBox(about_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(240, 160, 121, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.header = QtWidgets.QLabel(about_dialog)
        self.header.setGeometry(QtCore.QRect(150, 30, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setObjectName("header")
        self.info = QtWidgets.QLabel(about_dialog)
        self.info.setGeometry(QtCore.QRect(150, 60, 201, 71))
        self.info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.info.setObjectName("info")
        self.logo = QtWidgets.QLabel(about_dialog)
        self.logo.setGeometry(QtCore.QRect(20, 30, 100, 100))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/icon/img/logo.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")

        self.retranslateUi(about_dialog)
        self.buttonBox.accepted.connect(about_dialog.accept)
        self.buttonBox.rejected.connect(about_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(about_dialog)

    def retranslateUi(self, about_dialog):
        _translate = QtCore.QCoreApplication.translate
        about_dialog.setWindowTitle(_translate("about_dialog", "关于"))
        self.header.setText(_translate("about_dialog", "面向英文文献的编辑与检索系统"))
        self.info.setText(_translate("about_dialog", "<html><head/><body><p>Version 0.1<br/></p><p>Copyright (C) 2017 Yun Liu</p></body></html>"))

from . import res_rc
