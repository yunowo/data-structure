import ast
from os import path, walk, getcwd

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem

from about_dialog import AboutDialog
from common import input_dialog
from encode_dialog import EncodeDialog
from freq_dialog import FreqDialog
from inverse_index import InverseIndex
from search_highlighter import SearchHighlighter
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
        self.load_files_encoded()
        self.current_file = None
        self.highlighter = SearchHighlighter(self.edit_text.document())
        self.highlighter_index = SearchHighlighter(self.browse_text.document())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '确认', "真的要退出？", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def freq_dialog(self):
        w = FreqDialog()
        w.show()
        w.exec_()

    def about_dialog(self):
        w = AboutDialog()
        w.show()
        w.exec_()

    def encode_dialog(self):
        w = EncodeDialog(self.current_file, self.edit_text.toPlainText())
        w.show()
        w.exec_()

    def load_file_into_view(self, file, view):
        with open(path.join('docs', file), 'r+', encoding='utf-8') as f:
            text = f.readlines()
            if text:
                view.setText(text[0])
            else:
                view.setText('')
            if 'encoded' in file:
                f.seek(0)
                data = f.readlines()[0].split('<br />')
                codes = ast.literal_eval(data[1].split('=')[1])
                encoded = data[2].split('=')[1]
                self.code_table.setColumnCount(len(codes))
                self.code_table.setRowCount(2)
                i = 0
                for k, v in codes.items():
                    self.code_table.setItem(0, i, QTableWidgetItem(k))
                    self.code_table.setItem(1, i, QTableWidgetItem(v))
                    i += 1
                self.code_table.resizeColumnsToContents()
                self.browse_decoded.setText(encoded)

        self.statusbar.showMessage(path.join(getcwd(), 'docs', file))

    def on_file_change(self, curr, prev):
        if not curr:
            return
        self.load_file_into_view(curr.text(), self.edit_text)
        self.current_file = curr.text()

    def load_files(self):
        paths = [fn for fn in next(walk('docs'))[2]]
        paths.sort(key=lambda p: int(p.split('_')[0]))
        paths = filter(lambda p: 'encoded' not in p, paths)
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
            self.list_results.addItem(f'{r[0]}\t#{r[1]}')
        self.list_results.currentItemChanged.connect(self.on_result_change)
        self.list_results.show()
        self.highlighter_index.update_patterns(f"\\b{self.edit_index.text()}\\b")

    def create_new_file(self):
        ok, filename = input_dialog()
        if ok:
            with open(path.join('docs', filename), 'w+', encoding='utf-8') as f:
                f.writelines('')
            reply = QMessageBox.information(self, "ok", filename, QMessageBox.Yes | QMessageBox.No)

    def on_file_encoded_change(self, curr, prev):
        if not curr:
            return
        self.load_file_into_view(curr.text(), self.browse_encoded)
        self.current_file = curr.text()

    def load_files_encoded(self):
        paths = [fn for fn in next(walk('docs'))[2]]
        paths.sort(key=lambda p: int(p.split('_')[0]))
        paths = filter(lambda p: 'encoded' in p, paths)
        for f in paths:
            self.list_encoded.addItem(f)
        self.list_encoded.currentItemChanged.connect(self.on_file_encoded_change)
        self.list_encoded.show()
