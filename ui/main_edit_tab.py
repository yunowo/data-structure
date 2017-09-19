from os import walk, path, getcwd

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from ui.search_highlighter import SearchHighlighter
from ui.common import input_dialog
from ui.encode_dialog import EncodeDialog


class MainEditTab:
    def __init__(self, main_window):
        self.w = main_window

        self.w.button_save.clicked.connect(self.save)
        self.w.button_encode.clicked.connect(self.encode_dialog)
        self.w.button_add.clicked.connect(self.create_new_file)
        self.w.button_open.clicked.connect(self.open_file)
        self.highlighter = SearchHighlighter(self.w.edit_text.document())

        self.load_files()
        self.current_file = None

    def encode_dialog(self):
        w = EncodeDialog(self.current_file, self.w.edit_text.toPlainText())
        w.show()
        w.exec_()

    def load_file(self, file):
        with open(path.join('docs', file), 'r+', encoding='utf-8') as f:
            text = f.readlines()
            if text:
                self.w.edit_text.setText(text[0])
            else:
                self.w.edit_text.setText('')
        self.w.statusbar.showMessage(path.join(getcwd(), 'docs', file))

    def on_file_change(self, curr, prev):
        if not curr:
            return
        self.load_file(curr.text())
        self.current_file = curr.text()

    def load_files(self):
        self.w.list_files.clear()
        paths = [fn for fn in next(walk('docs'))[2]]
        paths.sort(key=lambda p: int(p.split('_')[0]))
        paths = filter(lambda p: 'encoded' not in p, paths)
        for f in paths:
            self.w.list_files.addItem(f)
        self.w.list_files.currentItemChanged.connect(self.on_file_change)
        self.w.list_files.show()

    def open_file(self):
        files = QFileDialog.getOpenFileName(self, '打开文件', '')
        if files[0]:
            with open(files[0], 'r') as f:
                data = f.read()
                self.w.edit_text.setText(data)

    def save(self):
        with open(path.join('docs', self.current_file), 'w+', encoding='utf-8') as f:
            text = self.w.edit_text.toPlainText().replace('\n', '<br />')
            f.write(text)

    def create_new_file(self):
        ok, filename = input_dialog()
        if ok:
            with open(path.join('docs', filename), 'w+', encoding='utf-8') as f:
                f.writelines('')
            reply = QMessageBox.information(self, "ok", filename, QMessageBox.Yes | QMessageBox.No)
