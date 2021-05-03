import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
)


class DirectedGraphMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QApplication([])

    mainwindow = DirectedGraphMainWindow()
    mainwindow.show()

    sys.exit(app.exec_())
