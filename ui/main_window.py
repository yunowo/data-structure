from PyQt5.QtWidgets import QMainWindow, QMessageBox

from ui.main_decode_tab import MainDecodeTab
from ui.main_search_tab import MainSearchTab
from ui.main_edit_tab import MainEditTab
from ui.about_dialog import AboutDialog
from ui.freq_dialog import FreqDialog
from ui.generated.main import Ui_main_window


class MainWindow(QMainWindow, Ui_main_window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.edit_tab = MainEditTab(self)
        self.search_tab = MainSearchTab(self)
        self.decode_tab = MainDecodeTab(self)
        self.tabs_container.currentChanged.connect(self.on_tab_change)

        self.action_freq.triggered.connect(self.freq_dialog)
        self.action_about.triggered.connect(self.about_dialog)

        self.current_file = None

    def on_tab_change(self, i):
        {0: lambda: self.edit_tab.load_files(),
         1: lambda: self.search_tab,  # Do nothing for now
         2: lambda: self.decode_tab.load_files()
         }[i]()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '确认', "真的要退出？", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def freq_dialog(self):
        w = FreqDialog()
        w.show()
        w.exec_()

    def about_dialog(self):
        w = AboutDialog()
        w.show()
        w.exec_()
