from os import path, walk

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from common import input_dialog
from encode_dialog import EncodeDialog
from freq_dialog import FreqDialog
from inverse_index import create_inverted_index
from ui.generated.main import Ui_main_window


class MainWindow(QMainWindow, Ui_main_window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.action_freq.triggered.connect(self.freq_dialog)
        self.action_search.triggered.connect(self.search_dialog)
        self.button_encode.clicked.connect(self.encode_dialog)
        self.button_add.clicked.connect(self.yesno)
        self.load_files()
        self.highlighter = Highlighter(self.edit_text.document())
        self.button_search.clicked.connect(self.search)

    def freq_dialog(self):
        w = FreqDialog()
        w.show()
        w.exec_()

    def search_dialog(self):
        create_inverted_index()

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
        self.statusbar.showMessage(curr.text())

    def load_files(self):
        paths = [fn for fn in next(walk('docs'))[2]]
        paths.sort(key=lambda p: int(p.split('_')[0]))
        for f in paths:
            self.list_files.addItem(f)
        self.list_files.currentItemChanged.connect(self.on_file_change)
        self.list_files.show()

    def search(self):
        q = self.edit_search.text()
        self.highlighter.update_patterns(f"\\b{q}\\b")

    def yesno(self):
        ok, filename = input_dialog()
        if ok:
            reply = QMessageBox.information(self, "ok", filename, QMessageBox.Yes | QMessageBox.No)


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        hf = QTextCharFormat()
        hf.setBackground(Qt.yellow)
        self.highlight_format = hf
        self.patterns = []
        self.highlighting_rules = []

    def update_patterns(self, p):
        self.patterns = [p]
        self.highlighting_rules = [QRegExp(p)]
        self.rehighlight()

    def highlightBlock(self, text):
        for pattern in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, self.highlight_format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)
