from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog

from common import dialog_flags
from ui.generated.about import Ui_about_dialog


class AboutDialog(QDialog, Ui_about_dialog):
    def __init__(self):
        super(AboutDialog, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(dialog_flags)