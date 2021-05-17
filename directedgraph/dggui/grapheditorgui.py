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

from directedgraph.dgcore import Node, GroundNode, SourceNode, Arc, graph
from directedgraph.dgcore import GroundNodeNumberError
from directedgraph.dgutils import FileManager


class NodeItem(QGraphicsEllipseItem):
    # Global Config

    def __init__(self, node_instance, main_window_instance):
        self.node = node_instance
        self.connected_window = main_window_instance

        self.node_radius = 40.0

        self.node_fill_colour = QColor(
            int(self.node.colour[1:3], 16),
            int(self.node.colour[3:5], 16),
            int(self.node.colour[5:7], 16),
        )

        self.node_fill_brush = QBrush(Qt.black, Qt.SolidPattern)
        self.node_fill_brush.setColor(self.node_fill_colour)

        bounding_shape = QRectF(
            self.node.position[0] - self.node_radius,
            self.node.position[1] - self.node_radius,
            2.0 * self.node_radius,
            2.0 * self.node_radius,
        )
        # Bounding rectangle of node 'ellipse' i.e. circle
        super().__init__(bounding_shape)

        self.setZValue(0)
        self.setBrush(self.node_fill_brush)

        # Set node attributes
        self.ItemIsSelectable = True
        self.ItemIsMovable = True
        self.ItemSendsGeometryChanges = True
        self.setAcceptHoverEvents(True)  # Make the Node accpect the Hover Event

        # Create selection rectangle shown when node is selected
        self.selectionRectangle = QGraphicsRectItem(self.boundingRect())
        self.selectionRectangle.setVisible(False)

    # ------------------------- paint -------------------------

    def paint(self, painter, option, parent):
        # Paint the node instance - called by QGraphicView instance
        boundingRect = self.boundingRect()

        if self.selectionRectangle.isVisible():
            # Paint selection rectangle
            painter.setPen(Qt.DashLine)
            painter.setBrush(Qt.NoBrush)
            self.selectionRectangle.setRect(boundingRect)
            painter.drawRect(boundingRect)

        # Paint node circle
        self.node_fill_colour = QColor(
            int(self.node.colour[1:3], 16),
            int(self.node.colour[3:5], 16),
            int(self.node.colour[5:7], 16),
        )
        self.node_fill_brush = QBrush(Qt.black, Qt.SolidPattern)
        self.node_fill_brush.setColor(self.node_fill_colour)
        painter.setBrush(self.node_fill_brush)
        painter.drawEllipse(boundingRect)

        # Paint node text
        painter.setPen(Qt.black)
        boundingRect.adjust(0, 20, 0, 20)
        painter.drawText(boundingRect, Qt.AlignCenter, self.node.name)
        boundingRect.adjust(0, -40, 0, -40)
        painter.drawText(boundingRect, Qt.AlignCenter, self.node.uid)

        print("paint called")
        return

    def setPos(self, pos):
        bounding = self.boundingRect()
        offset = bounding.center()
        super().setPos(pos - offset)

    # ------------------------- Mouse Event -------------------------

    # Override cursor shape into Openhand to indicate that drag is allowed
    # also indicate that you have selected a node (read to move)
    # 如果鼠标变成一个手说明可以准备移动 , 也可以表示你选中了一个节点，可以准备有动作
    def hoverEnterEvent(self, event):
        app = QApplication.instance()  # Obtain the Q application instance
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    # This Method is used to change back the cursor when mouse is not point to the node
    def hoverLeaveEvent(self, event):
        app = QApplication.instance()  # Obtain the Q application instance
        app.instance().restoreOverrideCursor()

    # Handler for mousePressEvent
    def mousePressEvent(self, event):
        self.prepareGeometryChange()
        mousePos = event.pos()
        # self.selectionRectangle.setVisible(True)
        print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
        return

    # Handler for mouseReleaseEvent
    def mouseReleaseEvent(self, event):
        self.prepareGeometryChange()
        mousePos = event.pos()
        # self.selectionRectangle.setVisible(False)
        print("mouseReleaseEvent at ", mousePos.x(), ", ", mousePos.y())
        return

    # Handler for mouseMoveEvent
    def mouseMoveEvent(self, event):

        self.prepareGeometryChange()
        scenePosition = event.scenePos()
        self.setPos(scenePosition)

        self.node.position[0] = scenePosition.x()
        self.node.position[1] = scenePosition.y()

        print("mouseMoveEvent to", scenePosition.x(), ", ", scenePosition.y())
        return

    # Handler for mouseDoubleClickEvent
    def mouseDoubleClickEvent(self, event):
        self.prepareGeometryChange()
        # self.setVisible(False)
        print("mouseDoubleClickEvent")
        return

    # ------------------------- Pop -------------------------

    # Pop Menu
    def contextMenuEvent(self, event):
        # Pop up menu for Node
        popmenu = QMenu()

        # Name
        nameAction = QAction("Name")
        popmenu.addAction(nameAction)
        nameAction.triggered.connect(self.on_name_action)

        # Colour
        colourAction = QAction("Colour")
        popmenu.addAction(colourAction)
        colourAction.triggered.connect(self.on_colour_action)

        popmenu.addSeparator()

        # Duplicate
        duplicateAction = QAction("Duplicate")
        popmenu.addAction(duplicateAction)
        duplicateAction.triggered.connect(self.on_duplicate_action)

        # Delete
        deleteAction = QAction("Delete")
        popmenu.addAction(deleteAction)
        deleteAction.triggered.connect(self.on_delete_action)

        # Excute at node Position, so it won't collide with Main windows pop-up menu
        popmenu.exec_(event.screenPos())

    # ------------------------- Action -------------------------

    def on_name_action(self):
        text, result = QInputDialog.getText(
            self.connected_window,
            "Input",
            "Enter Name",
            QtWidgets.QLineEdit.Normal,
        )
        if result == True:
            self.node.name = str(text)

    def on_colour_action(self):
        color = QColorDialog.getColor()
        print(color.getRgb())
        self.node.colour = (
            "#"
            + str(hex(color.getRgb()[0])[2:4]).zfill(2)
            + str(hex(color.getRgb()[1])[2:4]).zfill(2)
            + str(hex(color.getRgb()[2])[2:4]).zfill(2)
        )
        print(self.node.colour)

    def on_duplicate_action(self):
        pass  # #TODO

    def on_delete_action(self):
        self.node.connected_graph.delete_component(self.node.uid)  # #TODO
        self.connected_window.scene.removeItem(self)


class SourceNodeItem(QGraphicsEllipseItem):
    # Global Config

    def __init__(self, node_instance):
        self.node = node_instance
        self.node_radius = 40.0
        self.node_fill_colour = QColor(
            int(self.node.colour[1:3], 16),
            int(self.node.colour[3:5], 16),
            int(self.node.colour[5:7], 16),
        )
        self.node_fill_brush = QBrush(Qt.black, Qt.SolidPattern)
        self.node_fill_brush.setColor(self.node_fill_colour)

        bounding_shape = QRectF(
            self.node.position[0] - self.node_radius,
            self.node.position[1] - self.node_radius,
            2.0 * self.node_radius,
            2.0 * self.node_radius,
        )

        # Bounding rectangle of node 'ellipse' i.e. circle
        super().__init__(bounding_shape)

        self.setZValue(0)
        self.setBrush(self.node_fill_brush)

        # Set node attributes
        self.ItemIsSelectable = True
        self.ItemIsMovable = True
        self.ItemSendsGeometryChanges = True
        self.setAcceptHoverEvents(True)  # Make the Node accpect the Hover Event

        # Create selection rectangle shown when node is selected
        self.selectionRectangle = QGraphicsRectItem(self.boundingRect())
        self.selectionRectangle.setVisible(False)

    def paint(self, painter, option, parent):
        # Paint the node instance - called by QGraphicView instance
        boundingRect = self.boundingRect()

        if self.selectionRectangle.isVisible():
            # Paint selection rectangle
            painter.setPen(Qt.DashLine)
            painter.setBrush(Qt.NoBrush)
            self.selectionRectangle.setRect(boundingRect)
            painter.drawRect(boundingRect)

        # Paint node circle
        painter.setBrush(self.node_fill_brush)
        painter.drawEllipse(boundingRect)

        # Paint node text
        painter.setPen(Qt.black)
        painter.drawText(boundingRect, Qt.AlignCenter, self.node.name)

        print("paint called")
        return

    # Mouse Event===================================================================
    def hoverEnterEvent(self, event):
        # 如果鼠标变成一个手说明可以准备移动 , 也可以表示你选中了一个节点，可以准备有动作
        app = QtWidgets.QApplication.instance()  # Obtain the Qapplication instance
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        # Change back the cursor when mouse is not point to the node
        app = QtWidgets.QApplication.instance()  # Obtain the Qapplication instance
        app.instance().restoreOverrideCursor()

    def mousePressEvent(self, event):
        # Handler for mousePressEvent
        self.prepareGeometryChange()
        mousePos = event.pos()
        self.selectionRectangle.setVisible(True)
        print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
        # self.update()
        return

    def mouseReleaseEvent(self, event):
        # Handler for mouseReleaseEvent
        self.prepareGeometryChange()
        mousePos = event.pos()
        self.selectionRectangle.setVisible(False)
        print("mouseReleaseEvent at ", mousePos.x(), ", ", mousePos.y())
        # self.update()
        return

    def mouseMoveEvent(self, event):
        # Handler for mouseMoveEvent
        self.prepareGeometryChange()
        scenePosition = event.scenePos()
        self.node.position[0] = scenePosition.x()
        self.node.position[1] = scenePosition.y()
        self.setPos(scenePosition)
        print("mouseMoveEvent to", scenePosition.x(), ", ", scenePosition.y())
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
        bounding = self.boundingRect()
        offset = bounding.center()
        super().setPos(pos - offset)

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
        # deleteaction.triggered.connect()

        # Excute at node Position, so it won't collide with Main windows pop-up menu
        popmenu.exec_(event.screenPos())


class GroundNodeTestItem(NodeItem):
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.node_radius = 10.0


class GroundNodeItem(QGraphicsEllipseItem):
    # Global Config

    def __init__(self, node_instance):
        self.node = node_instance
        self.node_radius = 40.0
        self.node_fill_colour = QColor(255, 215, 0)
        self.node_fill_brush = QBrush(Qt.black, Qt.SolidPattern)
        self.node_fill_brush.setColor(self.node_fill_colour)

        bounding_shape = QRectF(
            self.node.position[0] - self.node_radius,
            self.node.position[1] - self.node_radius,
            2.0 * self.node_radius,
            2.0 * self.node_radius,
        )

        # Bounding rectangle of node 'ellipse' i.e. circle
        super().__init__(bounding_shape)

        self.setZValue(0)
        self.setBrush(self.node_fill_brush)

        # Set node attributes
        self.ItemIsSelectable = True
        self.ItemIsMovable = True
        self.ItemSendsGeometryChanges = True
        self.setAcceptHoverEvents(True)  # Make the Node accpect the Hover Event

        # Create selection rectangle shown when node is selected
        self.selectionRectangle = QGraphicsRectItem(self.boundingRect())
        self.selectionRectangle.setVisible(False)

    def paint(self, painter, option, parent):
        # Paint the node instance - called by QGraphicView instance
        boundingRect = self.boundingRect()

        if self.selectionRectangle.isVisible():
            # Paint selection rectangle
            painter.setPen(Qt.DashLine)
            painter.setBrush(Qt.NoBrush)
            self.selectionRectangle.setRect(boundingRect)
            painter.drawRect(boundingRect)

        # Paint node circle
        painter.setBrush(self.node_fill_brush)
        painter.drawEllipse(boundingRect)

        # Paint node text
        painter.setPen(Qt.black)
        painter.drawText(boundingRect, Qt.AlignCenter, self.node.name)

        print("paint called")
        return

    # Mouse Event ===============================================================

    # Override cursor shape into Openhand to indicate that drag is allowed,
    # also indicate that you have selected a node (read to move)
    def hoverEnterEvent(self, event):
        # 如果鼠标变成一个手说明可以准备移动 , 也可以表示你选中了一个节点，可以准备有动作
        app = QtWidgets.QApplication.instance()  # Obtain the Qapplication instance
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        # Change back the cursor when mouse is not point to the node
        app = QtWidgets.QApplication.instance()  # Obtain the Qapplication instance
        app.instance().restoreOverrideCursor()

    def mousePressEvent(self, event):
        # Handler for mousePressEvent
        self.prepareGeometryChange()
        mousePos = event.pos()
        self.selectionRectangle.setVisible(True)
        print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
        # self.update()
        return

    def mouseReleaseEvent(self, event):
        # Handler for mouseReleaseEvent
        self.prepareGeometryChange()
        mousePos = event.pos()
        self.selectionRectangle.setVisible(False)
        print("mouseReleaseEvent at ", mousePos.x(), ", ", mousePos.y())
        # self.update()
        return

    def mouseMoveEvent(self, event):
        # Handler for mouseMoveEvent
        self.prepareGeometryChange()
        scenePosition = event.scenePos()
        self.node.position[0] = scenePosition.x()
        self.node.position[1] = scenePosition.y()
        self.setPos(scenePosition)
        print("mouseMoveEvent to", scenePosition.x(), ", ", scenePosition.y())
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
        bounding = self.boundingRect()
        offset = bounding.center()
        super().setPos(pos - offset)

    # Pop Menu ==================================================================
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
        # deleteaction.triggered.connect()

        # Excute at node Position, so it won't collide with Main windows pop-up menu
        popmenu.exec_(event.screenPos())


class ArcItem:
    def __init__(self, arc_instance):
        pass


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
        self.scene.addItem(NodeItem(Node(None, None, "I", None, [500, 300])))  # #TODO

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
                GroundNodeItem(GroundNode(None, None, "groundnode1", None, [500, 300]))
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

        for compoment in graph1.components.values():
            if isinstance(compoment, Node):  # #TODO 要用 Type 改造
                self.scene.addItem(NodeItem(compoment, self))

        # self.scene.addItem(NodeItem(Node(None, None, "N1", "#FF0000", [200, 200])))
        # self.scene.addItem(NodeItem(Node(None, None, "N2", "#FF0000", [100, 100])))
        # test = NodeItem(Node(None, None, "N3", "#FF0000", [300, 300]))
        # self.scene.addItem(
        #     GroundNodeTestItem(Node(None, None, "Test", "#FF0000", [400, 400]))
        # )
        # self.scene.addItem(test)

        # menu = QMenu()
        # menu.addAction("Action 1")
        # menu.addAction("Action 2")
        # menu.addAction("Action 3")
        # menu.exec_()
        # self.scene.addItem(menu)


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
