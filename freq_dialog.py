import collections
from os import walk, path

import re
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from common import dialog_flags
from ui.freq import Ui_freq_dialog


class FreqDialog(QDialog, Ui_freq_dialog):
    def __init__(self):
        super(FreqDialog, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(dialog_flags)

        self.index_word()

    def index_word(self):
        d = {}
        paths = [fn for fn in next(walk('docs'))[2]]
        for file in paths:
            with open(path.join('docs', file)) as f:
                text = f.read().lower()
                text = re.sub("[\",./<>]", "", text)
                for word in text.split():
                    if word not in d:
                        d[word] = 0
                    d[word] += 1
        d = collections.OrderedDict(sorted(d.items(), key=lambda t: -t[1]))

        self.word_table.setRowCount(20)
        self.word_table.setColumnCount(2)
        for i,k in enumerate(d):
            self.word_table.setItem(i, 0, QTableWidgetItem(str(k)))
            self.word_table.setItem(i, 1, QTableWidgetItem(str(d[k])))
        self.word_table.resizeColumnsToContents()
