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
        encode_dialog.setWindowModality(QtCore.Qt.WindowModal)
        encode_dialog.resize(521, 481)
        encode_dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(encode_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.freq_table = QtWidgets.QTableWidget(encode_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.freq_table.sizePolicy().hasHeightForWidth())
        self.freq_table.setSizePolicy(sizePolicy)
        self.freq_table.setMinimumSize(QtCore.QSize(0, 80))
        self.freq_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.freq_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.freq_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.freq_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)
        self.freq_table.setObjectName("freq_table")
        self.freq_table.setColumnCount(0)
        self.freq_table.setRowCount(0)
        self.freq_table.horizontalHeader().setVisible(False)
        self.freq_table.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.freq_table)
        self.button_graph = QtWidgets.QPushButton(encode_dialog)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.button_graph.setFont(font)
        self.button_graph.setObjectName("button_graph")
        self.verticalLayout.addWidget(self.button_graph)
        self.encoded = QtWidgets.QTextBrowser(encode_dialog)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.encoded.setFont(font)
        self.encoded.setObjectName("encoded")
        self.verticalLayout.addWidget(self.encoded)
        self.buttonbox = QtWidgets.QDialogButtonBox(encode_dialog)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.buttonbox.setFont(font)
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Save)
        self.buttonbox.setCenterButtons(True)
        self.buttonbox.setObjectName("buttonbox")
        self.verticalLayout.addWidget(self.buttonbox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(encode_dialog)
        QtCore.QMetaObject.connectSlotsByName(encode_dialog)

    def retranslateUi(self, encode_dialog):
        _translate = QtCore.QCoreApplication.translate
        encode_dialog.setWindowTitle(_translate("encode_dialog", "编码"))
        self.button_graph.setText(_translate("encode_dialog", "哈夫曼树"))

from . import res_rc
