from os import path, getcwd

from algorithm.inverse_index import InverseIndex
from ui.search_highlighter import SearchHighlighter


class MainSearchTab:
    def __init__(self, main_window):
        self.w = main_window

        self.w.button_search.clicked.connect(self.search_keyword)
        self.w.button_refresh_index.clicked.connect(self.refresh_index)
        self.w.button_index.clicked.connect(self.search_index)
        self.highlighter_index = SearchHighlighter(self.w.browse_text.document())

        self.current_file = None

    def search_keyword(self):
        q = self.w.edit_search.text()
        self.w.highlighter.update_patterns(f"\\b{q}\\b")

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
        self.load_file(curr.text().split()[0])

    def search_index(self):
        self.w.list_results.clear()
        self.w.browse_text.clear()
        result = InverseIndex.search(self.w.edit_index.text())
        result.sort(key=lambda p: int(p[0].split('_')[0]))
        for r in result:
            self.w.list_results.addItem(f'{r[0]}\t#{r[1]}')
        self.w.list_results.currentItemChanged.connect(self.on_file_change)
        self.w.list_results.show()
        self.highlighter_index.update_patterns(f"\\b{self.w.edit_index.text()}\\b")
