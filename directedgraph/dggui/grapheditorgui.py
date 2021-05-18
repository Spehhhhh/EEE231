from PySide6.QtCore import Qt, QPointF, QRectF, QEvent
from PySide6.QtGui import QAction
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QBrush, QFontMetrics
from PySide6.QtWidgets import (
    QApplication,
    QInputDialog,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QDialog,
    QLabel,
    QColorDialog,
)
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtWidgets import QToolBar, QStatusBar
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QGraphicsEllipseItem,
    QGraphicsPathItem,
    QGraphicsSimpleTextItem,
    QGraphicsRectItem,
    QGraphicsItemGroup,
)

import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import Node, SourceNode, GroundNode, Arc, Graph
from directedgraph.dggui import NodeItem, SourceNodeItem, GroundNodeItem
from directedgraph.dgutils import FileManager


class InputDialogNode(QDialog, QMainWindow):
    def __init__(self, parent=None):
        super(InputDialogNode, self).__init__(parent)
        self.setWindowTitle("Please Input Source Node Value")
        self.edit = QLineEdit(self)
        self.edit.placeholderText()
        self.button = QPushButton("Confirm")
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.confirm)

    def confirm(self):
        try:
            return float(self.edit.text())
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("You have to enter a number!!")
            msg.show()
            msg.exec_()
            return


class InputDialogArc(QDialog, QMainWindow):
    def __init__(self, parent=None):
        super(InputDialogArc, self).__init__(parent)
        self.setWindowTitle("Please Input Linked Nodes UID")
        self.edit1 = QLineEdit(self)
        self.edit1.placeholderText()
        self.edit2 = QLineEdit(self)
        self.edit2.placeholderText()
        self.button = QPushButton("Confirm")
        layout = QVBoxLayout()
        layout.addWidget(self.edit1)
        layout.addWidget(self.edit2)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.resize(300, 100)
        self.button.clicked.connect(self.confirm)

    def confirm(self):
        return (self.edit1.text(), self.edit2.text())


class DirectedGraphMainWindow(QMainWindow, QDialog):
    def __init__(self):
        super().__init__()
        # Title of the Windows
        self.setWindowTitle("Graph Editor")

        # Initialise the QGraphicScene
        self.scene = QGraphicsScene(0, 0, 1980, 1080, self)
        self.view = QGraphicsView(self.scene)

        self.view.setRenderHints(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Set up the Menu Bar
        self.fileMenu = self.menuBar().addMenu("&File")

        self.openMenuAction = self.fileMenu.addAction("&Open...")
        self.openMenuAction.triggered.connect(self.on_open_action)

        self.saveMenuAction = self.fileMenu.addAction("&Save")
        self.saveMenuAction.triggered.connect(self.on_save_action)

        self.saveAsMenuAction = self.fileMenu.addAction("&Save As...")
        self.saveAsMenuAction.triggered.connect(self.on_save_as_action)

        # Setup Graph Component menu
        self.GraphComponentMenu = self.menuBar().addMenu("&Edit")

        self.NodeAction = self.GraphComponentMenu.addAction("&Add Node")
        self.NodeAction.triggered.connect(self.on_node_action)

        self.SourceNodeAction = self.GraphComponentMenu.addAction("&Add Source Node")
        self.SourceNodeAction.triggered.connect(self.on_sourcenode_action)

        self.GroundNodeAction = self.GraphComponentMenu.addAction("&Add Ground Node")
        self.GroundNodeAction.triggered.connect(self.on_groundnode_action)

        self.ArcAction = self.GraphComponentMenu.addAction("&Add Arc")
        self.ArcAction.triggered.connect(self.on_arc_action)

        self.graph = Graph()
        self.file_path = ""

    # Menu
    def contextMenuEvent(self, event):
        contextmenu = QMenu(self)

        newaction = QAction("New Component")
        contextmenu.addAction(newaction)
        # newaction.triggered.connect()

        contextmenu.addSeparator()

        openaction = QAction("Open...")
        contextmenu.addAction(openaction)
        openaction.triggered.connect(self.on_open_action)

        saveaction = QAction("Save")
        contextmenu.addAction(saveaction)
        saveaction.triggered.connect(self.on_save_action)

        saveasaction = QAction("Save As...")
        contextmenu.addAction(saveasaction)
        saveasaction.triggered.connect(self.on_save_as_action)

        contextmenu.addSeparator()

        helpaction = QAction("Help...")
        contextmenu.addAction(helpaction)
        helpaction.triggered.connect(self.on_about_action)

        # Excute the pop menu at all the graph area, but won't conflit with node pop meun
        action = contextmenu.exec_(self.mapToGlobal(event.pos()))

    # Trigger Function
    def on_open_action(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", ".", ("*.xml"))
        self.file_path = str(file_name[0])

        self.reset_scene()

        fm = FileManager()
        graph1 = fm.read_graph(str(file_name[0]))

        for component in graph1.components.values():
            if type(component) == Node:
                self.scene.addItem(NodeItem(component, self))
            if type(component) == SourceNode:
                self.scene.addItem(SourceNodeItem(component, self))
            if type(component) == GroundNode:
                self.scene.addItem(GroundNodeItem(component, self))

        self.graph = graph1

        return

    def on_save_action(self):
        fm = FileManager()
        fm.export_graph(self.file_path, self.graph)
        return

    def on_save_as_action(self):
        fm = FileManager()
        file_name = QtWidgets.QFileDialog.getSaveFileName(self, "Save File")
        print(self.graph)
        fm.export_graph(file_name[0], self.graph)
        return

    def on_preferences_action(self):
        return

    def on_about_action(self):
        QMessageBox.about(
            self,
            "About this program",
            "https://github.com/pirlite2/EEE231-group-B",
        )
        return

    def on_node_action(self):
        # self.scene.addItem(NodeItem())
        return

    def on_sourcenode_action(self):
        input_dialog_node = InputDialogNode()
        input_dialog_node.show()
        input_dialog_node.exec_()
        value = str(input_dialog_node.confirm())
        print("value:", value)

        # text, result = QInputDialog.getText(
        #     self,
        #     "Input",
        #     "Enter Name",
        #     QtWidgets.QLineEdit.Normal,
        # )

        # if result == True:
        #     self.node.name = str(text)
        # self.scene.addItem(
        #     SourceNodeItem(SourceNode(None, None, value, None, [250, 300]))
        # )
        return

    def on_groundnode_action(self):
        return

    def on_arc_action(self):
        input_dialog_arc = InputDialogArc()
        input_dialog_arc.show()
        input_dialog_arc.exec_()
        print(input_dialog_arc.confirm())
        return

    # Other Function
    def reset_scene(self):
        for item in self.scene.items():
            item.on_delete_action()
        return


class DirectedGraphApplication:
    def __init__(self):
        app = QApplication([])
        mainwindow = DirectedGraphMainWindow()
        mainwindow.showMaximized()
        sys.exit(app.exec_())

    def main(self):
        pass

    def quit(self):
        pass


if __name__ == "__main__":
    app = DirectedGraphApplication()
