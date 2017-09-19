import ast
from os import walk, path, getcwd

from PyQt5.QtWidgets import QTableWidgetItem


class MainDecodeTab:
    def __init__(self, main_window):
        self.w = main_window

        self.load_files()
        self.current_file = None

    def load_file(self, file):
        with open(path.join('docs', file), 'r+', encoding='utf-8') as f:
            text = f.readlines()
            if text:
                self.w.browse_encoded.setText(text[0])
            else:
                self.w.browse_encoded.setText('')
            if 'encoded' in file:
                f.seek(0)
                data = f.readlines()[0].split('<br />')
                codes = ast.literal_eval(data[1].split('=')[1])
                encoded = data[2].split('=')[1]
                self.w.code_table.setColumnCount(len(codes))
                self.w.code_table.setRowCount(2)
                i = 0
                for k, v in codes.items():
                    self.w.code_table.setItem(0, i, QTableWidgetItem(k))
                    self.w.code_table.setItem(1, i, QTableWidgetItem(v))
                    i += 1
                self.w.code_table.resizeColumnsToContents()
                self.w.browse_decoded.setText(encoded)
        self.w.statusbar.showMessage(path.join(getcwd(), 'docs', file))

    def on_file_change(self, curr, prev):
        if not curr:
            return
        self.load_file(curr.text())
        self.current_file = curr.text()

    def load_files(self):
        paths = [fn for fn in next(walk('docs'))[2]]
        paths.sort(key=lambda p: int(p.split('_')[0]))
        paths = filter(lambda p: 'encoded' in p, paths)
        for f in paths:
            self.w.list_encoded.addItem(f)
        self.w.list_encoded.currentItemChanged.connect(self.on_file_change)
        self.w.list_encoded.show()
