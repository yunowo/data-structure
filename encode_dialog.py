from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from common import dialog_flags
from huffman import Huffman
from ui.generated.encode import Ui_encode_dialog


class EncodeDialog(QDialog, Ui_encode_dialog):
    def __init__(self, text):
        super(EncodeDialog, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(dialog_flags)

        self.text_to_encode = text
        if text == "":
            return
        self.show_table()

    def show_table(self):
        freq_map, encoded_str, decode_str = Huffman().huffman(self.text_to_encode)
        freq_map.sort(key=lambda t: -t[1])
        self.freq_table.setRowCount(2)
        self.freq_table.setColumnCount(len(freq_map))
        for i, f in enumerate(freq_map):
            char, num = f
            self.freq_table.setItem(0, i, QTableWidgetItem(char))
            self.freq_table.setItem(1, i, QTableWidgetItem(str(num)))
        self.freq_table.resizeColumnsToContents()

        self.encoded.setText(encoded_str)
        self.decoded.setText(decode_str)
