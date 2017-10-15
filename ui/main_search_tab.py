from os import path, getcwd

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidgetItem, QHeaderView, QLineEdit

from algorithm.inverse_index import InverseIndex
from ui.search_highlighter import SearchHighlighter


class MainSearchTab:
    def __init__(self, main_window):
        self.w = main_window

        self.w.edit_index.textChanged.connect(self.search_index)
        self.w.edit_index.addAction(QIcon(':/icon/img/index.png'), QLineEdit.LeadingPosition)
        self.w.checkbox_match_case_index.stateChanged.connect(self.search_index)
        self.highlighter_index = SearchHighlighter(self.w.browse_text.document(), self.w.matches_counter_1)

        self.current_file = None
        self.setup()

    def load_file(self, file):
        with open(path.join('docs', file), 'r+', encoding='utf-8') as f:
            text = f.readlines()
            if text:
                self.w.browse_text.setText(text[0])
            else:
                self.w.browse_text.setText('')
        self.w.statusbar.showMessage(path.join(getcwd(), 'docs', file))

    def on_file_change(self, curr, prev):
        if not curr:
            return
        self.load_file(curr.data(0, 0))

    def setup(self):
        self.w.list_results.setColumnCount(3)
        self.w.list_results.setHeaderLabels(['     名称', '频度', '位置'])
        for i in range(0, 2):
            self.w.list_results.header().setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def search_index(self):
        self.w.list_results.clear()
        self.w.browse_text.clear()
        match_case = self.w.checkbox_match_case_index.isChecked()
        result = self.w.inverse_index.search(self.w.edit_index.text(), match_case)
        icon_2 = QIcon(':/icon/img/file_2.png')
        for r in result:
            item = SearchResultItem()
            item.setText(0, r[0])
            item.setText(1, str(len(r[1])))
            item.setText(2, ', '.join(str(n) for n in r[1]))
            item.setIcon(0, icon_2)
            self.w.list_results.invisibleRootItem().addChild(item)
        self.w.list_results.sortByColumn(1, Qt.DescendingOrder)
        self.w.list_results.currentItemChanged.connect(self.on_file_change)
        self.highlighter_index.match_case = match_case
        self.highlighter_index.update_patterns(f'\\b{self.w.edit_index.text()}\\b')


class SearchResultItem(QTreeWidgetItem):
    def __lt__(self, other):
        def name_to_int(t):
            return int(t.split('_')[0])

        def list_to_count(t):
            return len(t.split(','))

        column = self.treeWidget().sortColumn()
        if column == 0 or column == 1:
            return name_to_int(self.text(column)) < name_to_int(other.text(column))
        if column == 2:
            return list_to_count(self.text(column)) < list_to_count(other.text(column))
        return super(SearchResultItem, self).__lt__(other)
