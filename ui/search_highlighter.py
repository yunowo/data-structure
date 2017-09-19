from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat


class SearchHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(SearchHighlighter, self).__init__(parent)

        hf = QTextCharFormat()
        hf.setBackground(Qt.yellow)
        self.highlight_format = hf
        self.patterns = []
        self.highlighting_rules = []

    def update_patterns(self, p):
        self.patterns = [p]
        self.highlighting_rules = [QRegExp(p)]
        self.rehighlight()

    def highlightBlock(self, text):
        for pattern in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, self.highlight_format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)
