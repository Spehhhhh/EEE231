from sys import exit
from PySide6.QtWidgets import QApplication

from directedgraph.dggui import DirectedGraphMainWindow


class DirectedGraphApplication:
    def __init__(self):
        self.auto_save_interval = "300s"

    def run(self):
        print("run")
        application = QApplication([])

        mainwindow = DirectedGraphMainWindow()
        mainwindow.show()  # .showMaximized()

        exit(application.exec_())

    def run_debug(self):
        print("run_debug")


if __name__ == "__main__":
    app = DirectedGraphApplication()
    app.run()
