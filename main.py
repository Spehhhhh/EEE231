from sys import exit
from PySide6.QtWidgets import QApplication

from directedgraph.dggui import DirectedGraphMainWindow


class DirectedGraphApplication:
    def __init__(self):
        self.auto_save_interval = "300s"

    def run(self):
        print("Running")
        self.application = QApplication([])

        self.mainwindow = DirectedGraphMainWindow()
        self.mainwindow.show()  # .showMaximized()

        exit(self.application.exec_())

    def run_debug(self):
        print("Running Debug Mode")


if __name__ == "__main__":
    app = DirectedGraphApplication()
    app.run()
