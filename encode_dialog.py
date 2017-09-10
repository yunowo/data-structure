from PyQt5.QtWidgets import QDialog

from common import dialog_flags
from huffman import Huffman
from ui.encode import Ui_encode_dialog


class EncodeDialog(QDialog, Ui_encode_dialog):
    def __init__(self):
        super(EncodeDialog, self).__init__()
        self.setupUi(self)

        # self.textview.setText()
        self.setWindowFlags(dialog_flags)
        Huffman().test()
