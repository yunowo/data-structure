from os import path, walk

from PyQt5.QtWidgets import QMainWindow, QMessageBox

from common import input_dialog
from encode_dialog import EncodeDialog
from freq_dialog import FreqDialog
from ui.main import Ui_main_window


class MainWindow(QMainWindow, Ui_main_window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.action_freq.triggered.connect(self.freq_dialog)
        self.button_encode.clicked.connect(self.encode_dialog)
        self.button_add.clicked.connect(self.yesno)
        self.load_files()

    def freq_dialog(self):
        w = FreqDialog()
        w.show()
        w.exec_()

    def encode_dialog(self):
        w = EncodeDialog(self.edit_text.toPlainText())
        w.show()
        w.exec_()

    def on_file_change(self, curr, prev):
        with open(path.join('docs', curr.text()), 'r+', encoding='utf-8') as f:
            text = f.readlines()
            if text:
                self.edit_text.setText(text[0])
            else:
                self.edit_text.setText('')

    def load_files(self):
        paths = [fn for fn in next(walk('docs'))[2]]
        for f in paths:
            self.list_files.addItem(f)
        self.list_files.currentItemChanged.connect(self.on_file_change)
        self.list_files.show()

    def yesno(self):
        ok, filename = input_dialog()
        if ok:
            reply = QMessageBox.information(self, "ok", filename, QMessageBox.Yes | QMessageBox.No)
