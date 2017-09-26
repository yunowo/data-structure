import ast
import re
from os import walk, path
from PyQt5.QtWidgets import QProgressDialog, QApplication, QMessageBox

from ui.common import dialog_flags, font


class InverseIndex:
    def __init__(self):
        self.index = None
        self.index_lower = None

    def progress_dialog(self):
        d = QProgressDialog(None, dialog_flags)
        d.setWindowTitle('索引中...')
        d.setFont(font())
        d.show()
        self.create(d)

    def create(self, dialog):
        result, result_lower = {}, {}
        paths = [fn for fn in next(walk('docs'))[2]]
        paths = list(filter(lambda p: not p.startswith('.'), paths))
        paths = list(filter(lambda p: 'encoded' not in p, paths))
        dialog.setRange(0, len(paths))
        for j, p in enumerate(paths):
            dialog.setValue(j)
            dialog.setLabelText(p)
            QApplication.processEvents()
            if dialog.wasCanceled():
                break

            with open(path.join('docs', p), 'r', encoding='utf-8') as f:
                original = f.read()
                replaced = original.replace('<br />', '')
                filtered = re.sub('[",.?!:;/<>()]', ' ', replaced)
                words = list(filtered.split())
                words_lower = map(lambda w: w.lower(), words)

                def run(ws, r):
                    index = {}
                    for i, w in enumerate(ws):
                        if w not in index:
                            index[w] = (i,)
                        else:
                            index[w] = (*index[w], i)
                        if w not in r:
                            r[w] = {p: index[w]}
                        else:
                            r[w][p] = index[w]

                run(words, result)
                run(words_lower, result_lower)

        with open(path.join('docs', '.inverse_index.txt'), 'w', encoding='utf-8') as f:
            f.writelines(str(result))
        with open(path.join('docs', '.inverse_index_lower.txt'), 'w', encoding='utf-8') as f:
            f.writelines(str(result_lower))
        self.index, self.index_lower = result, result_lower
        dialog.close()
        QMessageBox.information(dialog, '检索', '检索已完成')

    def load_index(self):
        if self.index is None or self.index_lower is None:
            with open(path.join('docs', '.inverse_index.txt'), 'r', encoding='utf-8') as f:
                self.index = ast.literal_eval(f.readlines()[0])
            with open(path.join('docs', '.inverse_index_lower.txt'), 'r', encoding='utf-8') as f:
                self.index_lower = ast.literal_eval(f.readlines()[0])

    def search(self, query, match_case):
        self.load_index()
        if match_case:
            if query in self.index:
                return list(self.index[query].items())
        else:
            query = query.lower()
            if query in self.index_lower:
                return list(self.index_lower[query].items())
        return []
