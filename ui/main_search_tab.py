from os import path, getcwd

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

from algorithm.inverse_index import InverseIndex
from ui.search_highlighter import SearchHighlighter


class MainSearchTab:
    def __init__(self, main_window):
        self.w = main_window

        self.w.button_refresh_index.clicked.connect(self.refresh_index)
        self.w.button_index.clicked.connect(self.search_index)
        self.highlighter_index = SearchHighlighter(self.w.browse_text.document())

        self.current_file = None
        self.setup()

    def refresh_index(self):
        InverseIndex().progress_dialog()

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
        self.w.list_results.setColumnCount(2)
        self.w.list_results.setHeaderLabels(["名称", "出现位置"])

    def search_index(self):
        self.w.list_results.clear()
        self.w.browse_text.clear()
        result = InverseIndex.search(self.w.edit_index.text())
        result.sort(key=lambda p: int(p[0].split('_')[0]))
        for r in result:
            item = SearchResultItem()
            item.setText(0, r[0])
            item.setText(1, ", ".join(str(n) for n in r[1]))
            self.w.list_results.invisibleRootItem().addChild(item)
        self.w.list_results.sortByColumn(1, Qt.DescendingOrder)
        self.w.list_results.currentItemChanged.connect(self.on_file_change)
        self.highlighter_index.update_patterns(f"\\b{self.w.edit_index.text()}\\b")


class SearchResultItem(QTreeWidgetItem):
    def __lt__(self, other):
        def name_to_int(t):
            return int(t.split('_')[0])

        def list_to_count(t):
            return len(t.split(','))

        column = self.treeWidget().sortColumn()
        if column == 0:
            return name_to_int(self.text(column)) < name_to_int(other.text(column))
        if column == 1:
            return list_to_count(self.text(column)) < list_to_count(other.text(column))
        return super(SearchResultItem, self).__lt__(other)
