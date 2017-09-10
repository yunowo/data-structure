from PyQt5.QtWidgets import QDialog

from common import dialog_flags
from ui.freq import Ui_freq_dialog


class FreqDialog(QDialog, Ui_freq_dialog):
    def __init__(self):
        super(FreqDialog, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(dialog_flags)

