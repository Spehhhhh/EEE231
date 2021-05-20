import sys
from PySide6.QtWidgets import QApplication

from directedgraph.dggui import DirectedGraphMainWindow


class DirectedGraphApplication:
    def __init__(self):
        self.auto_save_interval = 300  # Seconds

    def main(self):
        app = QApplication([])
        mainwindow = DirectedGraphMainWindow()  # mainwindow.showMaximized()

        mainwindow.show()
        sys.exit(app.exec_())

    def quit(self):
        pass


if __name__ == "__main__":
    app = DirectedGraphApplication()
    app.main()
