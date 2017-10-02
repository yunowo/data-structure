from PyQt5.QtWidgets import QMainWindow, QMessageBox

from algorithm.inverse_index import InverseIndex
from ui.main_decode_tab import MainDecodeTab
from ui.main_search_tab import MainSearchTab
from ui.main_edit_tab import MainEditTab
from ui.main_stats_tab import MainStatsTab
from ui.about_dialog import AboutDialog
from ui.generated.main import Ui_main_window


class MainWindow(QMainWindow, Ui_main_window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.inverse_index = InverseIndex()
        self.inverse_index.load_indexes()

        self.edit_tab = MainEditTab(self)
        self.search_tab = MainSearchTab(self)
        self.decode_tab = MainDecodeTab(self)
        self.stats_tab = MainStatsTab(self)

        self.action_new.triggered.connect(lambda: self.to_edit(self.edit_tab.create_new_file))
        self.action_import.triggered.connect(lambda: self.to_edit(self.edit_tab.import_file))
        self.action_save.triggered.connect(lambda: self.to_edit(self.edit_tab.save))
        self.action_save_as.triggered.connect(lambda: self.to_edit(self.edit_tab.save_as))
        self.action_encode.triggered.connect(lambda: self.to_edit(self.edit_tab.encode_dialog))
        self.action_delete.triggered.connect(lambda: self.to_edit(self.edit_tab.delete))
        self.action_exit.triggered.connect(self.close)
        self.action_refresh_index.triggered.connect(self.refresh_index)
        self.action_about.triggered.connect(self.about_dialog)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '确认', '真的要退出?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def about_dialog(self):
        w = AboutDialog()
        w.show()
        w.exec_()

    def refresh_index(self):
        self.inverse_index.progress_dialog()

    def to_edit(self, action):
        self.tabs_container.setCurrentIndex(0)
        action()
