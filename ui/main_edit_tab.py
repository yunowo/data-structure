from os import walk, path, getcwd, remove

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from ui.search_highlighter import SearchHighlighter
from ui.common import input_dialog
from ui.encode_dialog import EncodeDialog


class MainEditTab:
    def __init__(self, main_window):
        self.w = main_window

        self.w.button_save.clicked.connect(self.save)
        self.w.button_encode.clicked.connect(self.encode_dialog)
        self.w.button_delete.clicked.connect(self.delete)
        self.w.button_add.clicked.connect(self.create_new_file)
        self.w.button_open.clicked.connect(self.open_file)
        self.highlighter = SearchHighlighter(self.w.edit_text.document())

        self.current_file = None
        self.file_num = 0
        self.load_files()

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
        paths = list(filter(lambda p: not p.startswith('.'), paths))
        paths = list(filter(lambda p: 'encoded' not in p, paths))
        paths.sort(key=lambda p: int(p.split('_')[0]))
        for f in paths:
            self.w.list_files.addItem(f)
        self.w.list_files.currentItemChanged.connect(self.on_file_change)
        self.w.list_files.show()
        self.w.list_files.setCurrentRow(0)
        self.file_num = len(paths)

    def get_next(self):
        return int(self.w.list_files.item(self.file_num - 1).text().split('_')[0]) + 1

    def open_file(self):
        files = QFileDialog.getOpenFileName(self.w, '导入文件', '')
        if files[0]:
            new_file = f'{self.get_next()}_{files[0].split("/")[-1].split(".")[-2]}.txt'
            with open(files[0], 'r') as f:
                data = f.read().replace('\n', '<br />')
                with open(path.join('docs', new_file), 'w+', encoding='utf-8') as n:
                    n.writelines(data)
            self.load_files()
            self.w.list_files.setCurrentRow(self.file_num - 1)
            QMessageBox.information(self.w, "导入文件", f'已导入 {new_file}')

    def create_new_file(self):
        ok, name = input_dialog('新建文件', '输入文件名, 序号和扩展名将自动添加:')
        if ok:
            filename = f'{self.get_next()}_{name}.txt'
            with open(path.join('docs', filename), 'w+', encoding='utf-8') as f:
                f.writelines('')
            self.load_files()
            self.w.list_files.setCurrentRow(self.file_num - 1)
            QMessageBox.information(self.w, "新建文件", f'已创建 {filename}')

    def save(self):
        with open(path.join('docs', self.current_file), 'w+', encoding='utf-8') as f:
            text = self.w.edit_text.toPlainText().replace('\n', '<br />')
            f.write(text)
        QMessageBox.information(self.w, "保存", '文件已保存')

    def delete(self):
        reply = QMessageBox.question(self.w, '确认', "真的要删除?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            remove(path.join('docs', self.current_file))
            row = self.w.list_files.currentRow() - 1
            self.load_files()
            self.w.list_files.setCurrentRow(row)
