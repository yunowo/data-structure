import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(':/icon/img/logo.png'))
    r = QDesktopWidget().availableGeometry()
    w = MainWindow()
    w.move((r.width() / 2) - (w.frameSize().width() / 2), (r.height() / 2) - (w.frameSize().height() / 2))
    w.show()
    w.tabs_container.setCurrentIndex(0)

    sys.exit(app.exec_())
