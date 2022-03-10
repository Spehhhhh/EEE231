import sys

from PySide6.QtWidgets import QApplication

from directedgraph.dggui import GraphEditorMainWindow


class GraphEditor:
    """
    Run
    """

    def __init__(self):
        self.auto_save_interval = "300s"
        self.application = QApplication([])
        self.mainwindow = GraphEditorMainWindow()

    def run(self):
        """
        Run
        """

        self._run("Running")

    def run_debug(self):
        """
        Debug
        """
        self._run("Running Debug Mode")

    def _run(self, arg0):
        print(arg0)
        self.mainwindow.show()
        sys.exit(self.application.exec_())
