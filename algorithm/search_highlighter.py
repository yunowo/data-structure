import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat

from algorithm.kmp import search


class SearchHighlighter(QSyntaxHighlighter):
    def __init__(self, parent, counter):
        super(SearchHighlighter, self).__init__(parent)
        self.counter = counter

        hf = QTextCharFormat()
        hf.setBackground(Qt.yellow)
        self.highlight_format = hf
        self.match_case = True
        self.only_words = True
        self.regex = False
        self.patterns = []
        self.results = []

    def update_patterns(self, p):
        if type(p) is list:
            self.patterns = p
            self.rehighlight()
            return
        if p is '':
            self.patterns = []
            self.rehighlight()
            return
        if not self.match_case:
            p = p.lower()
        if self.only_words:
            p = re.sub('[\",.?!:;/<>()]', '', p)
            self.patterns = [f'\\b{p}\\b'] if p else []
        elif self.regex:
            self.patterns = [p]
        else:
            self.patterns = [p]
        self.rehighlight()

    def highlightBlock(self, text):
        self.results = []
        if not self.patterns:
            self.setCurrentBlockState(0)
            return
        if not self.match_case:
            text = text.lower()
        if self.only_words or self.regex:
            for pattern in self.patterns:
                p = re.compile(pattern)
                m = p.search(text)
                while m:
                    self.setFormat(m.start(), m.end() - m.start(), self.highlight_format)
                    self.results.append(m.start())
                    m = p.search(text, m.end())
        else:
            for pattern in self.patterns:
                indexes = search(text, pattern)
                for i in indexes:
                    self.setFormat(i, len(pattern), self.highlight_format)
                self.results.extend(indexes)
        self.setCurrentBlockState(0)
        self.counter.setText(f'{len(self.results)} 个匹配')
