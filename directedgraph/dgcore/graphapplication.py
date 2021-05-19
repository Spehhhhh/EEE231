import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dggui import DirectedGraphMainWindow


class DirectedGraphApplication:
    def __init__(self):
        self.auto_save_interval = 300  # Seconds

        app = QApplication([])
        mainwindow = DirectedGraphMainWindow()
        # mainwindow.showMaximized()

        mainwindow.show()
        sys.exit(app.exec_())

    def main(self):
        pass

    def quit(self):
        pass


if __name__ == "__main__":
    # import unittest
    # from tests.test_dgcore_graphapplication import TestDirectedGraphApplication

    # unittest.main()
    app = DirectedGraphApplication()
