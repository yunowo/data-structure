import ast
import re
from os import walk, path
from PyQt5.QtWidgets import QProgressDialog, QApplication, QMessageBox

from ui.common import dialog_flags, font


class InverseIndex:
    def progress_dialog(self):
        d = QProgressDialog(None, dialog_flags)
        d.setWindowTitle("索引中...")
        d.setFont(font())
        d.show()
        self.create(d)

    @staticmethod
    def create(dialog):
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
                filtered = re.sub("[\",.?!:;/<>()]", "", original)
                words = list(set(filtered.split()))

                for i, w in enumerate(words):
                    index = []
                    for ii, ww in enumerate(words):
                        if ww == w:
                            index.append((p, ii))
                    if w in result:
                        result[w].append(*index)
                    else:
                        result[w] = index

        with open(path.join('docs', '.inverse_index.txt'), 'w', encoding='utf-8') as f:
            f.writelines(str(result))
        dialog.close()
        QMessageBox.information(dialog, "检索", "检索已完成")

    @staticmethod
    def search(query):
        with open(path.join('docs', '.inverse_index.txt'), 'r', encoding='utf-8') as f:
            index = ast.literal_eval(f.readlines()[0])
            result = []
            for k in index.keys():
                if query == k:
                    result = [*result, *index[k]]
            return result
