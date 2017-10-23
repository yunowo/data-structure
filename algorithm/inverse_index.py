import ast
import re
from collections import OrderedDict
from os import walk, path
from PyQt5.QtWidgets import QProgressDialog, QApplication, QMessageBox
from wordcloud import STOPWORDS

from ui.common import dialog_flags, font


def save_to(file, src):
    with open(path.join('docs', file), 'w', encoding='utf-8') as f:
        f.writelines(str(src))


def load_from(file):
    with open(path.join('docs', file), 'r', encoding='utf-8') as f:
        return ast.literal_eval(f.readlines()[0])


class InverseIndex:
    def __init__(self):
        self.index = None
        self.index_lower = None
        self.count = None
        self.count_filtered = None

    def progress_dialog(self):
        d = QProgressDialog(None, dialog_flags)
        d.setWindowTitle('索引中...')
        d.setFont(font())
        d.show()
        self.create(d)

    def create(self, dialog):
        result, result_lower, count, count_filtered = {}, {}, {}, {}
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

                words_lower = map(lambda w: w.lower(), words)
                for i, w in enumerate(words_lower):
                    if w not in count:
                        count[w] = 0
                    count[w] += 1
        count = dict(OrderedDict(sorted(count.items(), key=lambda t: -t[1])))
        count_filtered = {k: v for k, v in count.items() if k not in STOPWORDS}

        self.index, self.index_lower, self.count = result, result_lower, count
        save_to('.inverse_index.txt', result)
        save_to('.inverse_index_lower.txt', result_lower)
        save_to('.frequency_count.txt', count)
        save_to('.frequency_count_filtered.txt', count_filtered)
        dialog.close()
        QMessageBox.information(dialog, '检索', '检索已完成')

    def load_indexes(self):
        if self.index is None or self.index_lower is None or self.count is None:
            self.index = load_from('.inverse_index.txt')
            self.index_lower = load_from('.inverse_index_lower.txt')
            self.count = load_from('.frequency_count.txt')
            self.count_filtered = load_from('.frequency_count_filtered.txt')

    def search(self, query, match_case):
        self.load_indexes()
        if match_case:
            return self.multi_search(query, self.index)
        else:
            query = query.lower()
            return self.multi_search(query, self.index_lower)

    def multi_search(self, query, index):
        q = set(query.split())
        r = {}
        for w in q:
            if w in index:
                for li in [(t[0], len(t[1])) for t in list(index[w].items())]:
                    if li[0] in r:
                        r[li[0]][w] = li[1]
                    else:
                        r[li[0]] = {w: li[1]}
        r = {k: v for k, v in r.items() if len(v.items()) == len(q)}
        k = list(r.values())
        return r, list(k[0].keys()) if len(k) > 0 else []
