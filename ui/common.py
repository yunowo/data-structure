from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog

dialog_flags = Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint


def font():
    f = QtGui.QFont()
    f.setFamily("微软雅黑")
    return f


def input_dialog():
    dialog = QInputDialog(None, dialog_flags)
    dialog.setInputMode(QInputDialog.TextInput)
    dialog.setWindowTitle('新文件')
    dialog.setLabelText('输入新文件名:')
    dialog.setFont(font())
    ok = dialog.exec_()
    filename = dialog.textValue()
    return ok, filename
