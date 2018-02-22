import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from ui.main_window import MainWindow


def setup_hook():
    _excepthook = sys.excepthook

    def hook(exctype, value, traceback):
        print(exctype, value, traceback)
        _excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = hook


if __name__ == '__main__':
    setup_hook()

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(':/icon/img/logo.png'))
    w = MainWindow()
    cp = QDesktopWidget().availableGeometry().center()
    qr = w.frameGeometry()
    qr.moveCenter(cp)
    w.move(qr.topLeft())
    w.show()
    w.tabs_container.setCurrentIndex(0)

    try:
        sys.exit(app.exec_())
    except:
        pass
