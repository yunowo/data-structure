# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'encode.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_encode_dialog(object):
    def setupUi(self, encode_dialog):
        encode_dialog.setObjectName("encode_dialog")
        encode_dialog.resize(400, 300)
        encode_dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(encode_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(100, 250, 251, 23))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tableWidget = QtWidgets.QTableWidget(encode_dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 121, 351, 101))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.textview = QtWidgets.QTextBrowser(encode_dialog)
        self.textview.setGeometry(QtCore.QRect(20, 20, 351, 81))
        self.textview.setObjectName("textview")

        self.retranslateUi(encode_dialog)
        self.buttonBox.accepted.connect(encode_dialog.accept)
        self.buttonBox.rejected.connect(encode_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(encode_dialog)

    def retranslateUi(self, encode_dialog):
        _translate = QtCore.QCoreApplication.translate
        encode_dialog.setWindowTitle(_translate("encode_dialog", "编码"))

