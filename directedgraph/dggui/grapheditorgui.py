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
        self.setWindowTitle("GUI editor")
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

        # Set up the Menu Bar============================================================
        self.fileMenu = self.menuBar().addMenu("&File")

        self.openMenuAction = self.fileMenu.addAction("&Open")
        self.openMenuAction.triggered.connect(self.on_open_action)  # New-style connect!

        self.fileMenu.addSeparator()

        self.quitMenuAction = self.fileMenu.addAction("&Quit")
        self.quitMenuAction.triggered.connect(self.on_quit_action)

        # Setup Tools menu==============================================================
        self.toolsMenu = self.menuBar().addMenu("&Tools")
        self.preferencesMenuAction = self.toolsMenu.addAction("&Preferences")
        self.preferencesMenuAction.triggered.connect(self.on_preferences_action)

        # Setup About menu==============================================================
        self.aboutMenu = self.menuBar().addMenu("&About")
        self.aboutMenuAction = self.aboutMenu.addAction("&About")
        self.aboutMenuAction.triggered.connect(self.on_about_action)
        self.setCentralWidget(self.widget)

        # Setup GraphComponent menu====================================================
        self.GraphComponentMenu = self.menuBar().addMenu("&GraphComponent")
        self.NodeAction = self.GraphComponentMenu.addAction("&Node")
        self.NodeAction.triggered.connect(self.on_node)
        self.GroundNodeAction = self.GraphComponentMenu.addAction("&GroundNode")
        self.GroundNodeAction.triggered.connect(self.on_groundnode)
        self.SourceNodeAction = self.GraphComponentMenu.addAction("&SourceNode")
        self.SourceNodeAction.triggered.connect(self.on_sourcenode)
        self.ArcAction = self.GraphComponentMenu.addAction("&Arc")
        self.ArcAction.triggered.connect(self.on_arc)

        self.mainToolBar = QToolBar()
        self.mainToolBar.setMovable(False)
        self.newToolButton = self.mainToolBar.addAction("New")
        self.openToolButton = self.mainToolBar.addAction("Open")
        self.openToolButton.triggered.connect(self.on_open_action)
        self.saveToolButton = self.mainToolBar.addAction("Save")
        self.saveToolButton.setShortcut("Ctrl+S")
        self.saveToolButton.setStatusTip("Save File")
        self.saveToolButton.triggered.connect(self.on_save_file)
        self.saveAsToolButton = self.mainToolBar.addAction("Save As")
        self.addToolBar(self.mainToolBar)
        self.layout.addWidget(self.mainToolBar)
        self.init_graph()

        # Pop out menu for the graph================================================

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
        fileName = QFileDialog.getOpenFileName(self, "Open File", ".", ("*.md"))
        print("opening ", fileName[0])
        return

    def on_quit_action(self):
        """Handler for 'Quit' action"""
        print("quitting application")
        self.close()
        return

    def on_preferences_action(self):
        """Handler for 'Preferences' action"""
        print("preferences")
        return

    def on_about_action(self):
        """Handler for 'About' action"""
        QMessageBox.about(
            self,
            "About this program",
            "some about text crediting the people who wrote this",
        )
        return

    def on_node(self):
        self.scene.addItem(
            NodeItem(Node(None, None, "I", None, [500, 300]), self)
        )  # #TODO

    def on_groundnode(self):
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

    def on_sourcenode(self):
        form = InputFormSourceNode()
        form.show()
        form.exec_()
        value = str(form.confirm())
        print("value:", value)
        self.scene.addItem(
            SourceNodeItem(SourceNode(None, None, value, None, [250, 300]))
        )

    def on_arc(self):
        input_arc = Arc_Input()
        input_arc.show()
        input_arc.exec_()
        print(input_arc.confirm())

    def on_save_file(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, "Save File")
        file = open(name[0], "w")
        # 传输xml格式，使用filemanager
        text = "sasd"
        file.write(text)
        file.close()

    def event_filter(self, source, event):
        pass

    def init_graph(self):
        fm = FileManager()
        path = (
            Path(os.path.dirname(__file__))
            .parent.parent.joinpath("tests")
            .joinpath("test.xml")
        )
        graph1 = fm.read_graph(str(path))

        for component in graph1.components.values():
            if type(component) == Node:
                self.scene.addItem(NodeItem(component, self))
            if type(component) == SourceNode:
                self.scene.addItem(SourceNodeItem(component, self))


class DirectedGraphApplication:
    def __init__(self):
        app = QApplication([])
        mainwindow = DirectedGraphMainWindow()
        mainwindow.show()
        sys.exit(app.exec_())

    def main(self):
        pass

    def quit(self):
        pass


if __name__ == "__main__":
    app = DirectedGraphApplication()
