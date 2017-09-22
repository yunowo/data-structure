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
        freq_dialog.resize(265, 406)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        freq_dialog.setFont(font)
        freq_dialog.setModal(True)
        self.buttonbox = QtWidgets.QDialogButtonBox(freq_dialog)
        self.buttonbox.setGeometry(QtCore.QRect(10, 360, 241, 32))
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonbox.setObjectName("buttonbox")
        self.word_table = QtWidgets.QTableWidget(freq_dialog)
        self.word_table.setGeometry(QtCore.QRect(10, 10, 241, 341))
        self.word_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.word_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.word_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.word_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.word_table.setObjectName("word_table")
        self.word_table.setColumnCount(0)
        self.word_table.setRowCount(0)
        self.word_table.horizontalHeader().setVisible(False)
        self.word_table.verticalHeader().setVisible(False)

        self.retranslateUi(freq_dialog)
        self.buttonbox.accepted.connect(freq_dialog.accept)
        self.buttonbox.rejected.connect(freq_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(freq_dialog)

    def retranslateUi(self, freq_dialog):
        _translate = QtCore.QCoreApplication.translate
        freq_dialog.setWindowTitle(_translate("freq_dialog", "词汇出现频率"))

