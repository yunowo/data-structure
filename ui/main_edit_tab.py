from os import path, getcwd, remove

from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from algorithm.kmp import replace
from ui.common import input_dialog
from ui.encode_dialog import EncodeDialog
from ui.file_sort_filter import setup_file_view
from ui.search_highlighter import SearchHighlighter


class MainEditTab:
    def __init__(self, main_window):
        self.w = main_window

        self.w.button_save.clicked.connect(self.save)
        self.w.button_encode.clicked.connect(self.encode_dialog)
        self.w.button_delete.clicked.connect(self.delete)
        self.w.button_add.clicked.connect(self.create_new_file)
        self.w.button_open.clicked.connect(self.import_file)
        self.w.edit_search.textChanged.connect(self.search)
        self.w.checkbox_match_case.stateChanged.connect(self.search)
        self.w.checkbox_words.stateChanged.connect(self.search)
        self.w.button_search.clicked.connect(self.search)
        self.w.button_replace.clicked.connect(self.replace)
        self.w.button_replace_all.clicked.connect(self.replace_all)
        self.highlighter = SearchHighlighter(self.w.edit_text.document())

        self.model = None
        self.filtered_model = None
        self.current_file = None
        self.current_row = 0
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

    def on_file_change(self, curr):
        if not curr:
            return
        name = self.model.fileName(curr.indexes()[0])
        self.load_file(name)
        self.current_file = name

    def docs_root(self):
        def find_model(root):
            if root.data() == 'docs':
                return root
            else:
                return find_model(root.child(0, 0))

        return find_model(self.filtered_model.index(0, 0))

    def select_current_row(self, row):
        index = self.docs_root().child(row, 0)
        self.w.list_files.selectionModel().select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        self.w.list_files.scrollTo(index)

    def folder_loaded(self):
        self.file_num = self.filtered_model.rowCount(self.docs_root())
        if self.current_file is None:
            self.select_current_row(0)
        self.select_current_row(self.current_row)

    def load_files(self):
        self.model, self.filtered_model = setup_file_view(self.w.list_files, False)
        self.model.directoryLoaded.connect(self.folder_loaded)
        self.w.list_files.selectionModel().selectionChanged.connect(self.on_file_change)

    def get_next(self):
        index = self.docs_root().child(self.file_num - 1, 0)
        data = self.filtered_model.data(index)
        return int(data.split('_')[0]) + 1

    def import_file(self):
        files = QFileDialog.getOpenFileName(self.w, '导入文件', '')
        if files[0]:
            new_file = f'{self.get_next()}_{files[0].split("/")[-1].split(".")[-2]}.txt'
            with open(files[0], 'r+', encoding='utf-8') as f:
                data = f.read().replace('\n', '<br />')
                with open(path.join('docs', new_file), 'w+', encoding='utf-8') as n:
                    n.writelines(data)
            self.current_row = self.file_num
            self.load_files()
            QMessageBox.information(self.w, "导入文件", f'已导入 {new_file}')

    def create_new_file(self):
        ok, name = input_dialog('新建文件', '输入文件名, 序号和扩展名将自动添加:')
        if ok:
            filename = f'{self.get_next()}_{name}.txt'
            with open(path.join('docs', filename), 'w+', encoding='utf-8') as f:
                f.writelines('')
            self.current_row = self.file_num
            self.load_files()
            QMessageBox.information(self.w, '新建文件', f'已创建 {filename}')

    def save(self):
        with open(path.join('docs', self.current_file), 'w+', encoding='utf-8') as f:
            text = self.w.edit_text.toPlainText().replace('\n', '<br />')
            f.write(text)
        QMessageBox.information(self.w, '保存', '文件已保存')

    def delete(self):
        reply = QMessageBox.question(self.w, '确认', '真的要删除?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            remove(path.join('docs', self.current_file))
            row = self.w.list_files.selectedIndexes()[0].row() - 1
            self.load_files()
            self.current_row = row

    def search(self):
        self.highlighter.match_case = self.w.checkbox_match_case.isChecked()
        self.highlighter.only_words = self.w.checkbox_words.isChecked()
        q = self.w.edit_search.text()
        self.highlighter.update_patterns(q)

    def replace(self):
        self.do_replace(1)

    def replace_all(self):
        self.do_replace(-1)

    def do_replace(self, c):
        s = self.w.edit_search.text()
        r = self.w.edit_replace.text()
        t = self.w.edit_text.toPlainText()
        t = replace(c, t, r, s, self.highlighter.results)
        self.w.edit_text.setText(t.replace('\n', '<br />'))
