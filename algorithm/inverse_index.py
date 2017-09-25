import ast
import re
from os import walk, path
from PyQt5.QtWidgets import QProgressDialog, QApplication, QMessageBox

from ui.common import dialog_flags, font


class InverseIndex:
    def __init__(self):
        self.index = None

    def progress_dialog(self):
        d = QProgressDialog(None, dialog_flags)
        d.setWindowTitle('索引中...')
        d.setFont(font())
        d.show()
        self.create(d)

    def create(self, dialog):
        result = {}
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

                index = {}
                for i, w in enumerate(words):
                    if w not in index:
                        index[w] = (i,)
                    else:
                        index[w] = (*index[w], i)
                    if w not in result:
                        result[w] = {p: index[w]}
                    else:
                        result[w][p] = index[w]

        with open(path.join('docs', '.inverse_index.txt'), 'w', encoding='utf-8') as f:
            f.writelines(str(result))
        self.index = result
        dialog.close()
        QMessageBox.information(dialog, '检索', '检索已完成')

    def search(self, query, match_case):
        if self.index is None:
            with open(path.join('docs', '.inverse_index.txt'), 'r', encoding='utf-8') as f:
                self.index = ast.literal_eval(f.readlines()[0])
        if match_case:
            if query in self.index:
                return list(self.index[query].items())
            else:
                return []
        else:
            result = []
            for k, v in self.index.items():
                if query.lower() == k.lower():
                    result.extend(list(v.items()))
            return result
