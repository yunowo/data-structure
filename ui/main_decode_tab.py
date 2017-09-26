import ast
from os import path, getcwd

from PyQt5.QtWidgets import QTableWidgetItem

from algorithm.huffman import huffman_decode
from ui.file_sort_filter import setup_file_view


class MainDecodeTab:
    def __init__(self, main_window):
        self.w = main_window

        self.model = None
        self.filtered_model = None
        self.current_file = None
        self.load_files()

    def load_file(self, file):
        with open(path.join('docs', file), 'r+', encoding='utf-8') as f:
            text = f.readlines()
            if text:
                self.w.browse_encoded.setText(text[0])
            else:
                self.w.browse_encoded.setText('')

            f.seek(0)
            data = f.readlines()[0].split('<br />')
            codes = ast.literal_eval(data[1].split('=')[1])
            encoded = data[2].split('=')[1]

            sorted_codes = sorted(codes.items(), key=lambda t: len(t[1]))
            self.w.code_table.setColumnCount(len(sorted_codes))
            self.w.code_table.setRowCount(2)
            self.w.code_table.setVerticalHeaderLabels(['字符', '编码'])
            for i, t in enumerate(sorted_codes):
                self.w.code_table.setItem(0, i, QTableWidgetItem(t[0]))
                self.w.code_table.setItem(1, i, QTableWidgetItem(t[1]))
            self.w.code_table.resizeColumnsToContents()
            self.w.browse_decoded.setText(huffman_decode(encoded, codes))
        self.w.statusbar.showMessage(path.join(getcwd(), 'docs', file))

    def on_file_change(self, curr):
        if not curr:
            return
        name = self.model.fileName(curr.indexes()[0])
        self.load_file(name)
        self.current_file = name

    def load_files(self):
        self.model, self.filtered_model = setup_file_view(self.w.list_encoded, True)
        self.w.list_encoded.selectionModel().selectionChanged.connect(self.on_file_change)
