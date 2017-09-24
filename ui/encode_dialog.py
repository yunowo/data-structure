from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QDialogButtonBox, QMessageBox
from os import path

from algorithm.huffman import Huffman
from algorithm.huffman_tree import HuffmanTree
from ui.common import dialog_flags
from ui.generated.encode import Ui_encode_dialog


class EncodeDialog(QDialog, Ui_encode_dialog):
    def __init__(self, filename, text):
        super(EncodeDialog, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(dialog_flags)

        self.button_graph.clicked.connect(self.show_graph)
        self.buttonbox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.buttonbox.button(QDialogButtonBox.Save).clicked.connect(self.save_encoded)
        self.buttonbox.button(QDialogButtonBox.Save).setText('保存')

        self.filename = filename
        self.text_to_encode = text
        if text == '':
            return
        self.freq_map = None
        self.root = None
        self.nodes = None
        self.encoded_str = ''
        self.show_table()

    def show_table(self):
        self.freq_map, self.root, self.nodes, self.encoded_str = Huffman().huffman(self.text_to_encode)
        s = sorted(self.freq_map.items(), key=lambda t: -t[1][0])
        self.freq_table.setRowCount(3)
        self.freq_table.setColumnCount(len(s))
        self.freq_table.setVerticalHeaderLabels(['字符', '频度', '编码'])
        for i, t in enumerate(s):
            num, freq = t[1]
            self.freq_table.setItem(0, i, QTableWidgetItem(t[0]))
            self.freq_table.setItem(1, i, QTableWidgetItem(str(num)))
            self.freq_table.setItem(2, i, QTableWidgetItem(freq))
        self.freq_table.resizeColumnsToContents()

        self.encoded.setText(self.encoded_str)

    def show_graph(self):
        HuffmanTree(self.root, self.nodes)

    def save_encoded(self):
        file = f'{self.filename.split(".")[0]}_encoded.txt'
        with open(path.join('docs', file), 'w+', encoding='utf-8') as f:
            f.writelines('encoding=huffman<br />')
            t = {c: t[1] for c, t in self.freq_map.items()}
            f.writelines(f'codes={t} <br />')
            f.writelines(f'encoded={self.encoded_str}<br />')
        QMessageBox.information(self, '编码', f'编码后的文件已保存到 {file}', QMessageBox.Ok)
