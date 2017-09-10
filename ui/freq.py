# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'freq.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_freq_dialog(object):
    def setupUi(self, freq_dialog):
        freq_dialog.setObjectName("freq_dialog")
        freq_dialog.resize(400, 300)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        freq_dialog.setFont(font)
        freq_dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(freq_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tableWidget = QtWidgets.QTableWidget(freq_dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 40, 361, 201))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(freq_dialog)
        self.buttonBox.accepted.connect(freq_dialog.accept)
        self.buttonBox.rejected.connect(freq_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(freq_dialog)

    def retranslateUi(self, freq_dialog):
        _translate = QtCore.QCoreApplication.translate
        freq_dialog.setWindowTitle(_translate("freq_dialog", "词汇出现频率"))

