import sys

from PySide6.QtWidgets import QApplication

from directedgraph.dggui import DirectedGraphMainWindow


class DirectedGraphApplication:
    """
    Run
    """

    def __init__(self):
        self.auto_save_interval = "300s"
        self.application = QApplication([])
        self.mainwindow = DirectedGraphMainWindow()

    def run(self):
        """
        Run
        """

        print("Running")
        self.mainwindow.show()  # .showMaximized()
        sys.exit(self.application.exec_())

    def run_debug(self):
        """
        Debug
        """
        print("Running Debug Mode")
        self.mainwindow.show()
        sys.exit(self.application.exec_())
