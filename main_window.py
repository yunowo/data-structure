from os import path, walk

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog

from about_dialog import AboutDialog
from common import input_dialog
from encode_dialog import EncodeDialog
from freq_dialog import FreqDialog
from inverse_index import InverseIndex
from ui.generated.main import Ui_main_window


class MainWindow(QMainWindow, Ui_main_window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.action_freq.triggered.connect(self.freq_dialog)
        self.action_about.triggered.connect(self.about_dialog)
        self.button_save.clicked.connect(self.save)
        self.button_encode.clicked.connect(self.encode_dialog)
        self.button_add.clicked.connect(self.create_new_file)
        self.button_open.clicked.connect(self.open_file)
        self.button_search.clicked.connect(self.search)
        self.button_refresh_index.clicked.connect(self.refresh_index)
        self.button_index.clicked.connect(self.search_index)
        self.load_files()
        self.current_file = None
        self.highlighter = Highlighter(self.edit_text.document())
        self.highlighter_index = Highlighter(self.browse_text.document())

    def freq_dialog(self):
        w = FreqDialog()
        w.show()
        w.exec_()

    def about_dialog(self):
        w = AboutDialog()
        w.show()
        w.exec_()

    def encode_dialog(self):
        w = EncodeDialog(self.edit_text.toPlainText())
        w.show()
        w.exec_()

    def load_file_into_view(self, file, view):
        with open(path.join('docs', file), 'r+', encoding='utf-8') as f:
            text = f.readlines()
            if text:
                view.setText(text[0])
            else:
                view.setText('')
        self.statusbar.showMessage(file)

    def on_file_change(self, curr, prev):
        if not curr:
            return
        self.load_file_into_view(curr.text(), self.edit_text)
        self.current_file = curr.text()

    def load_files(self):
        paths = [fn for fn in next(walk('docs'))[2]]
        paths.sort(key=lambda p: int(p.split('_')[0]))
        for f in paths:
            self.list_files.addItem(f)
        self.list_files.currentItemChanged.connect(self.on_file_change)
        self.list_files.show()

    def open_file(self):
        files = QFileDialog.getOpenFileName(self, '打开文件', '')
        if files[0]:
            with open(files[0], 'r') as f:
                data = f.read()
                self.edit_text.setText(data)

    def save(self):
        with open(path.join('docs', self.current_file), 'w+', encoding='utf-8') as f:
            text = self.edit_text.toPlainText().replace('\n', '<br />')
            f.write(text)

    def search(self):
        q = self.edit_search.text()
        self.highlighter.update_patterns(f"\\b{q}\\b")

    def refresh_index(self):
        InverseIndex().progress_dialog()

    def on_result_change(self, curr, prev):
        if not curr:
            return
        self.load_file_into_view(curr.text().split()[0], self.browse_text)

    def search_index(self):
        self.list_results.clear()
        self.browse_text.clear()
        result = InverseIndex.search(self.edit_index.text())
        result.sort(key=lambda p: int(p[0].split('_')[0]))
        for r in result:
            self.list_results.addItem(f'{r[0]} #{r[1]}')
        self.list_results.currentItemChanged.connect(self.on_result_change)
        self.list_results.show()
        self.highlighter_index.update_patterns(f"\\b{self.edit_index.text()}\\b")

    def create_new_file(self):
        ok, filename = input_dialog()
        if ok:
            with open(path.join('docs', filename), 'w+', encoding='utf-8') as f:
                f.writelines('')
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
