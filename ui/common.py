from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QItemSelectionModel, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QInputDialog

dialog_flags = Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint
selection_flags = QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows


def font():
    f = QtGui.QFont()
    f.setFamily('微软雅黑')
    return f


def input_dialog(title, label):
    dialog = QInputDialog(None, dialog_flags)
    dialog.setInputMode(QInputDialog.TextInput)
    dialog.setWindowTitle(title)
    dialog.setLabelText(label)
    dialog.setFont(font())
    ok = dialog.exec_()
    filename = dialog.textValue()
    return ok, filename


def search_validator():
    return QRegExpValidator(QRegExp('\w+'))
