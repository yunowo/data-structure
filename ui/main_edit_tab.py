from os import path, getcwd, remove

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLineEdit, QWidget, QGridLayout, QTextEdit

from algorithm.kmp import replace
from ui.common import input_dialog, selection_flags, search_validator
from ui.encode_dialog import EncodeDialog
from ui.file_sort_filter import setup_file_view
from ui.search_highlighter import SearchHighlighter


class MainEditTab:
    def __init__(self, main_window):
        self.w = main_window

        self.w.button_save.clicked.connect(self.save)
        self.w.button_save_as.clicked.connect(self.save_as)
        self.w.button_encode.clicked.connect(self.encode_dialog)
        self.w.button_delete.clicked.connect(self.delete)
        self.w.button_add.clicked.connect(self.create_new_file)
        self.w.button_open.clicked.connect(self.import_file)
        self.w.edit_search.textChanged.connect(self.search)
        self.w.checkbox_match_case.stateChanged.connect(self.search)
        self.w.checkbox_words.stateChanged.connect(self.search)
        self.w.button_replace.clicked.connect(self.replace)
        self.w.button_replace_all.clicked.connect(self.replace_all)
        self.w.edit_search.setValidator(search_validator())
        self.w.edit_search.addAction(QIcon(':/icon/img/search.png'), QLineEdit.LeadingPosition)
        self.w.edit_replace.addAction(QIcon(':/icon/img/replace.png'), QLineEdit.LeadingPosition)

        fs_model, self.model = setup_file_view(self.w.list_files, False)
        fs_model.directoryLoaded.connect(self.folder_loaded)
        self.w.list_files.selectionModel().selectionChanged.connect(self.on_file_change)
        self.next_row = 0
        self.tab_adapter = TabAdapter(self.w, self)
        self.w.tab_widget.currentChanged.connect(self.tab_adapter.current_changed)
        self.w.tab_widget.tabCloseRequested.connect(self.tab_adapter.close_tab)
        self.w.tab_widget.tabBarDoubleClicked.connect(self.tab_adapter.double_clicked)

    def encode_dialog(self):
        w = EncodeDialog(self.tab_adapter.current_name(), self.tab_adapter.current_edit().toPlainText())
        w.show()
        w.exec_()

    def on_file_change(self, curr):
        if not curr:
            return
        name = self.model.data(curr.indexes()[0])
        self.tab_adapter.file_change(name)

    def folder_loaded(self):
        index = self.model.docs_root().child(self.next_row, 0)
        self.w.list_files.selectionModel().select(index, selection_flags)
        self.w.list_files.scrollTo(index)

    def get_next(self):
        index = self.model.docs_root().child(self.model.file_num() - 1, 0)
        data = self.model.data(index)
        return int(data.split('_')[0]) + 1

    def import_file(self):
        files = QFileDialog.getOpenFileName(self.w, '导入文件', '')
        if files[0]:
            new_file = f'{self.get_next()}_{files[0].split("/")[-1].split(".")[-2]}.txt'
            with open(files[0], 'r+', encoding='utf-8') as f:
                data = f.read().replace('\n', '<br />')
                with open(path.join('docs', new_file), 'w+', encoding='utf-8') as n:
                    n.writelines(data)
            self.next_row = self.model.file_num()
            self.tab_adapter.need_persistence = True

    def create_new_file(self):
        ok, name = input_dialog('新建文件', '输入文件名, 序号和扩展名将自动添加:')
        if ok:
            filename = f'{self.get_next()}_{name}.txt'
            with open(path.join('docs', filename), 'w+', encoding='utf-8') as f:
                f.writelines('')
            self.next_row = self.model.file_num()
            self.tab_adapter.need_persistence = True

    def save(self):
        with open(path.join('docs', self.tab_adapter.current_name()), 'w+', encoding='utf-8') as f:
            text = self.tab_adapter.current_edit().toPlainText().replace('\n', '<br />')
            f.write(text)
        QMessageBox.information(self.w, '保存', '文件已保存')

    def save_as(self):
        ok, name = input_dialog('另存为', '输入文件名, 序号和扩展名将自动添加:')
        if ok:
            filename = f'{self.get_next()}_{name}.txt'
            with open(path.join('docs', filename), 'w+', encoding='utf-8') as f:
                text = self.tab_adapter.current_edit().toPlainText().replace('\n', '<br />')
                f.write(text)
            self.next_row = self.model.file_num()
            self.tab_adapter.need_persistence = True

    def delete(self):
        reply = QMessageBox.question(self.w, '确认', '真的要删除?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            remove(path.join('docs', self.tab_adapter.current_name()))
            self.next_row = self.w.list_files.selectedIndexes()[0].row() - 1
            self.tab_adapter.close_tab(self.tab_adapter.current_index)

    def search(self):
        hl = self.tab_adapter.current_highlighter()
        hl.match_case = self.w.checkbox_match_case.isChecked()
        hl.only_words = self.w.checkbox_words.isChecked()
        q = self.w.edit_search.text()
        hl.update_patterns(q)

    def replace(self):
        self.do_replace(1)

    def replace_all(self):
        self.do_replace(-1)

    def do_replace(self, c):
        s = self.w.edit_search.text()
        r = self.w.edit_replace.text()
        t = self.tab_adapter.current_edit().toPlainText()
        t = replace(c, t, r, s, self.tab_adapter.current_highlighter().results)
        self.tab_adapter.current_edit().setText(t.replace('\n', '<br />'))


class TabAdapter:
    def __init__(self, w, host):
        self.w = w
        self.tab_widget = w.tab_widget
        self.host = host
        self.files = []
        self.tabs = []
        self.edits = []
        self.highlighters = []
        self.current_index = 0
        self.last_is_temp = True
        self.need_persistence = False
        self.new_tab('0_3.txt')

    def count(self):
        return len(self.files) - 1

    def load_file(self, file, edit):
        with open(path.join('docs', file), 'r+', encoding='utf-8') as f:
            text = f.readlines()
            if text:
                edit.setText(text[0])
            else:
                edit.setText('')
        self.w.status_bar.showMessage(path.join(getcwd(), 'docs', file))

    def file_change(self, name):
        if name in self.files:
            self.tab_widget.setCurrentIndex(self.files.index(name))
            return
        if self.last_is_temp:
            self.files[self.count()] = name
            self.load_file(name, self.edits[self.count()])
            self.tab_widget.tabBar().setTabText(self.count(), name)
            self.tab_widget.setCurrentIndex(self.count())
        else:
            self.new_tab(name)
        if self.need_persistence:
            self.persistence()
            self.need_persistence = False

    def new_tab(self, name):
        self.last_is_temp = True
        tab = QWidget()
        grid = QGridLayout(tab)
        edit = QTextEdit(tab)
        grid.addWidget(edit, 0, 0, 1, 1)
        highlighter = SearchHighlighter(edit.document(), self.w.matches_counter)
        self.load_file(name, edit)
        self.files.append(name)
        self.tabs.append(tab)
        self.edits.append(edit)
        self.highlighters.append(highlighter)
        self.tab_widget.addTab(tab, name)
        self.tab_widget.setCurrentWidget(tab)
        self.tab_widget.tabBar().setTabTextColor(self.current_index, Qt.gray)

    def current_changed(self, index):
        self.current_index = index
        self.host.search()

    def double_clicked(self, index):
        if self.last_is_temp and index == self.current_index:
            self.persistence()

    def persistence(self):
        self.last_is_temp = False
        self.tab_widget.tabBar().setTabTextColor(self.current_index, Qt.black)

    def close_tab(self, index):
        self.tab_widget.removeTab(index)
        del self.files[index]
        del self.tabs[index]
        del self.edits[index]
        del self.highlighters[index]
        if self.last_is_temp and index != self.current_index:
            self.last_is_temp = False

    def current_name(self):
        return self.files[self.current_index]

    def current_edit(self):
        return self.edits[self.current_index]

    def current_highlighter(self):
        return self.highlighters[self.current_index]
