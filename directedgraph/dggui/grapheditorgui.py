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
import os
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import GroundNodeNumberError
from directedgraph.dgcore import Node, SourceNode, GroundNode, Arc, Graph
from directedgraph.dggui import NodeItem, SourceNodeItem, GroundNodeItem
from directedgraph.dgutils import FileManager


class ArcItem(QGraphicsPathItem):
    def __init__(self, arc_instance, graph=None):
        self.ar_instance = arc_instance

    def paint(self, painter, option, parent):
        pass

    def hoverEnterEvent(self, event):
        # 如果鼠标变成一个手说明可以准备移动 , 也可以表示你选中了一个节点，可以准备有动作
        app = QtWidgets.QApplication.instance()  # Obtain the Qapplication instance
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        # Change back the cursor when mouse is not point to the node
        app = QtWidgets.QApplication.instance()  # Obtain the Qapplication instance
        app.instance().restoreOverrideCursor()

    def mouseReleaseEvent(self, event):
        self.prepareGeometryChange()
        mousePos = event.pos()
        self.selectionRectangle.setVisible(False)
        print("mouseReleaseEvent at ", mousePos.x(), ", ", mousePos.y())
        # self.update()
        return

    def mousePressEvent(self, event):
        # Handler for mousePressEvent
        self.prepareGeometryChange()
        mousePos = event.pos()
        self.selectionRectangle.setVisible(True)
        print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
        # self.update()
        return

    def mouseDoubleClickEvent(self, event):
        # Handler for mouseDoubleClickEvent
        self.prepareGeometryChange()
        # self.setVisible(False)
        print("mouseDoubleClickEvent")
        # self.update()
        return

    def setPos(self, pos):

        pass

    def contextMenuEvent(self, event):
        # Pop up menu for Node
        popmenu = QMenu()

        # Name
        nameaction = QAction("Name")
        popmenu.addAction(nameaction)
        # nameaction.triggered.connect()

        # Colour
        colouraction = QAction("Colour")
        popmenu.addAction(colouraction)
        # colouraction.triggered.connect()

        # Value
        valueaction = QAction("Value")
        popmenu.addAction(valueaction)
        # valueaction.triggered.connect()

        popmenu.addSeparator()

        # Delete
        deleteaction = QAction("Delete")
        popmenu.addAction(deleteaction)
        # deleteaction.triggered.conn ect()

        # Excute at node Position, so it won't collide with Main windows pop-up menu
        popmenu.exec_(event.screenPos())


class InputFormSourceNode(QDialog, QMainWindow):
    def __init__(self, parent=None):
        super(InputFormSourceNode, self).__init__(parent)
        self.setWindowTitle("Input source node value")
        self.edit = QLineEdit(self)
        self.edit.placeholderText()
        self.button = QPushButton("confirm")
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


class Arc_Input(QDialog, QMainWindow):
    def __init__(self, parent=None):
        super(Arc_Input, self).__init__(parent)
        self.setWindowTitle("Input two linked nodes' uid")
        self.edit1 = QLineEdit(self)
        self.edit1.placeholderText()
        self.edit2 = QLineEdit(self)
        self.edit2.placeholderText()
        self.button = QPushButton("confirm")
        layout = QVBoxLayout()
        layout.addWidget(self.edit1)
        layout.addWidget(self.edit2)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.confirm)

    def confirm(self):
        print(self.edit1.text())
        print(self.edit2.text())
        return [self.edit1.text(), self.edit2.text()]


class DirectedGraphMainWindow(QMainWindow, QDialog):
    def __init__(self):
        super().__init__()
        # Title of the Windows
        self.setWindowTitle("Graph Editor")
        self.ground_node_count = 0

        # Initialise the QGraphicScene
        self.scene = QGraphicsScene(0, 0, 1980, 1080, self)
        self.view = QGraphicsView(self.scene)

        # self.view.resize(1000, 1000)
        self.view.setRenderHints(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Set up the Menu Bar
        self.fileMenu = self.menuBar().addMenu("&File")

        self.openMenuAction = self.fileMenu.addAction("&Open")
        self.openMenuAction.triggered.connect(self.on_open_action)

        self.saveMenuAction = self.fileMenu.addAction("&Save")
        self.saveMenuAction.triggered.connect(self.on_save_action)

        self.saveAsMenuAction = self.fileMenu.addAction("&Save As...")
        self.saveAsMenuAction.triggered.connect(self.on_save_as_action)

        # Setup Graph Component menu
        self.GraphComponentMenu = self.menuBar().addMenu("&Add")

        self.NodeAction = self.GraphComponentMenu.addAction("&Node")
        self.NodeAction.triggered.connect(self.on_node_action)

        self.SourceNodeAction = self.GraphComponentMenu.addAction("&Source Node")
        self.SourceNodeAction.triggered.connect(self.on_sourcenode_action)

        self.GroundNodeAction = self.GraphComponentMenu.addAction("&Ground Node")
        self.GroundNodeAction.triggered.connect(self.on_groundnode_action)

        self.ArcAction = self.GraphComponentMenu.addAction("&Arc")
        self.ArcAction.triggered.connect(self.on_arc_action)

        # #TODO
        self.file_path = ""
        self.graph = Graph()

    # Menu =========================================================
    def contextMenuEvent(self, event):
        contextmenu = QMenu(self)

        newaction = QAction("New")
        contextmenu.addAction(newaction)
        # newaction.triggered.connect()

        openaction = QAction("Open")
        contextmenu.addAction(openaction)
        # openaction.triggered.connect()

        saveaction = QAction("Save")
        contextmenu.addAction(saveaction)
        # saveaction.triggered.connect()

        copyaction = QAction("Copy")
        contextmenu.addAction(copyaction)
        # copyaction.triggered.connect()

        pastaction = contextmenu.addAction("Past")
        contextmenu.addAction(pastaction)
        # copyaction.triggered.connect()

        helpaction = QAction("Help...")
        contextmenu.addAction(helpaction)
        # copyaction.triggered.connect()

        # Excute the pop menu at all the graph area, but won't conflit with node pop meun
        action = contextmenu.exec_(self.mapToGlobal(event.pos()))

    # Trigger Fcuntions =========================================================
    def on_open_action(self):
        """Handler for 'Open' action"""
        file_name = QFileDialog.getOpenFileName(self, "Open File", ".", ("*.xml"))

        self.file_path = str(file_name[0])
        print("opening ", file_name[0])

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
        print("save", self.file_path)
        pass

    def on_save_as_action(self):
        fm = FileManager()
        file_name = QtWidgets.QFileDialog.getSaveFileName(self, "Save File")
        print(self.graph)
        fm.export_graph(file_name[0], self.graph)
        return

    def on_preferences_action(self):
        print("preferences")
        return

    def on_about_action(self):
        QMessageBox.about(
            self,
            "About this program",
            "some about text crediting the people who wrote this",
        )
        return

    def on_node_action(self):
        self.scene.addItem(NodeItem(Node(None, None, "I", None, [500, 300]), self))
        # #TODO

    def on_sourcenode_action(self):
        form = InputFormSourceNode()
        form.show()
        form.exec_()
        value = str(form.confirm())
        print("value:", value)
        self.scene.addItem(
            SourceNodeItem(SourceNode(None, None, value, None, [250, 300]))
        )

    def on_groundnode_action(self):
        self.ground_node_count += 1
        if self.ground_node_count > 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Only one ground_node is allowed!!!")
            msg.show()
            msg.exec_()
            raise GroundNodeNumberError("oops!!")
        else:
            self.scene.addItem(
                GroundNodeItem(GroundNode(None, None, "G1", None, [500, 300]))
            )

    def on_arc_action(self):
        input_arc = Arc_Input()
        input_arc.show()
        input_arc.exec_()
        print(input_arc.confirm())


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
