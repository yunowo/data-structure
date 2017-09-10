# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.setWindowModality(QtCore.Qt.NonModal)
        main_window.resize(703, 515)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        main_window.setFont(font)
        main_window.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.container = QtWidgets.QHBoxLayout()
        self.container.setObjectName("container")
        self.left = QtWidgets.QVBoxLayout()
        self.left.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.left.setObjectName("left")
        self.list_files = QtWidgets.QListWidget(self.centralwidget)
        self.list_files.setMaximumSize(QtCore.QSize(200, 16777215))
        self.list_files.setObjectName("list_files")
        self.left.addWidget(self.list_files)
        self.button_add = QtWidgets.QPushButton(self.centralwidget)
        self.button_add.setObjectName("button_add")
        self.left.addWidget(self.button_add)
        self.container.addLayout(self.left)
        self.right = QtWidgets.QVBoxLayout()
        self.right.setObjectName("right")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.right.addWidget(self.checkBox)
        self.container_5 = QtWidgets.QHBoxLayout()
        self.container_5.setContentsMargins(-1, -1, -1, 0)
        self.container_5.setObjectName("container_5")
        self.button_save = QtWidgets.QPushButton(self.centralwidget)
        self.button_save.setObjectName("button_save")
        self.container_5.addWidget(self.button_save)
        self.button_encode = QtWidgets.QPushButton(self.centralwidget)
        self.button_encode.setObjectName("button_encode")
        self.container_5.addWidget(self.button_encode)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.container_5.addWidget(self.pushButton)
        self.right.addLayout(self.container_5)
        self.container_2 = QtWidgets.QHBoxLayout()
        self.container_2.setContentsMargins(0, -1, -1, 0)
        self.container_2.setObjectName("container_2")
        self.edit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_search.setObjectName("edit_search")
        self.container_2.addWidget(self.edit_search)
        self.button_search = QtWidgets.QPushButton(self.centralwidget)
        self.button_search.setObjectName("button_search")
        self.container_2.addWidget(self.button_search)
        self.right.addLayout(self.container_2)
        self.container_3 = QtWidgets.QHBoxLayout()
        self.container_3.setContentsMargins(0, -1, -1, 0)
        self.container_3.setObjectName("container_3")
        self.edit_replace = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_replace.setObjectName("edit_replace")
        self.container_3.addWidget(self.edit_replace)
        self.button_replace = QtWidgets.QPushButton(self.centralwidget)
        self.button_replace.setObjectName("button_replace")
        self.container_3.addWidget(self.button_replace)
        self.right.addLayout(self.container_3)
        self.edit_text = QtWidgets.QTextBrowser(self.centralwidget)
        self.edit_text.setObjectName("edit_text")
        self.right.addWidget(self.edit_text)
        self.container.addLayout(self.right)
        self.gridLayout_2.addLayout(self.container, 0, 0, 1, 1)
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 703, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(main_window)
        self.toolBar.setObjectName("toolBar")
        main_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_freq = QtWidgets.QAction(main_window)
        self.action_freq.setObjectName("action_freq")
        self.menu.addAction(self.action_freq)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "面向英文文献的编辑与检索系统"))
        self.button_add.setText(_translate("main_window", "添加"))
        self.checkBox.setText(_translate("main_window", "CheckBox"))
        self.button_save.setText(_translate("main_window", "保存"))
        self.button_encode.setText(_translate("main_window", "编码"))
        self.pushButton.setText(_translate("main_window", "PushButton"))
        self.button_search.setText(_translate("main_window", "查找"))
        self.button_replace.setText(_translate("main_window", "替换"))
        self.menu.setTitle(_translate("main_window", "词汇出现频率"))
        self.menu_2.setTitle(_translate("main_window", "关键词检索"))
        self.toolBar.setWindowTitle(_translate("main_window", "toolBar"))
        self.action_freq.setText(_translate("main_window", "???"))

