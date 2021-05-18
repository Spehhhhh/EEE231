from PySide6.QtCore import Qt, QPointF, QRectF, QEvent
from PySide6.QtGui import QAction
import math
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
        return [scenePosition.x(), scenePosition.y()]

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
        colouraction.triggered.connect(self.on_colour_action)

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
        boundingRect.adjust(0, 20, 0, 20)
        painter.drawText(boundingRect, Qt.AlignCenter, self.node.name)
        boundingRect.adjust(0, -50, 0, -40)
        painter.drawText(boundingRect, Qt.AlignCenter, self.node.uid)
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
        # deleteaction.triggered.conn ect()

        # Excute at node Position, so it won't collide with Main windows pop-up menu
        popmenu.exec_(event.screenPos())


class ArcItem(QGraphicsEllipseItem):
    def __init__(self, arc_instance, graph=None):
        self.arc_instance = arc_instance
        self.graph = graph
        # 根据两端的uid获取查询所在图中两个node对象
        self.node1 = self.arc_instance.nodes[0]
        self.node2 = self.arc_instance.nodes[1]

        # 再根据两个node对象得到两个node对象的位置
        self.node1_position = self.node1.get_position()
        self.node2_position = self.node2.get_position()

        self.arc_fill_brush = QBrush(Qt.black, Qt.SolidPattern)
        bounding_shape = QRectF(
            self.node1_position[0] - (self.node2_position[0] - self.node1_position[0]),
            self.node1_position[1],
            2 * (abs(self.node1_position[0] - self.node2_position[0])),
            2 * (abs(self.node1_position[1] - self.node2_position[1])),
        )
        print("bounding_shape:", bounding_shape.center())
        super().__init__(bounding_shape)

        self.setZValue(0)
        self.setBrush(self.arc_fill_brush)

        # Set node attributes
        self.ItemIsSelectable = True
        self.ItemIsMovable = True
        self.ItemSendsGeometryChanges = True
        self.setAcceptHoverEvents(True)  # Make the Node accpect the Hover Event

        # Create selection rectangle shown when node is selected
        self.selectionRectangle = QGraphicsRectItem(self.boundingRect())
        self.selectionRectangle.setVisible(False)

    def paint(self, painter, option, parent):
        boundingRect = self.boundingRect()

        if self.selectionRectangle.isVisible():
            # Paint selection rectangle
            painter.setPen(Qt.DashLine)
            painter.setBrush(Qt.NoBrush)
            self.selectionRectangle.setRect(boundingRect)
            painter.drawRect(boundingRect)

        # Paint node circle
        painter.setBrush(self.arc_fill_brush)

        degree1 = (
            math.atan(self.node1_position[1] / self.node1_position[0]) / math.pi
        ) * 180
        degree2 = (
            math.atan(self.node2_position[1] / self.node2_position[0]) / math.pi
        ) * 180
        painter.drawArc(boundingRect, 0, 90 * 16)

        return

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

    def mouseMoveEvent(self, event):

        self.prepareGeometryChange()
        scenePosition = event.scenePos()
        self.setPos(scenePosition)
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
        return

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

        self.init_graph()

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

    def on_save_action(self):
        pass

    def on_save_as_action(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, "Save File")
        file = open(name[0], "w")
        # 传输xml格式，使用filemanager
        text = "sasd"
        file.write(text)
        file.close()
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

    def on_node_action(self):
        self.scene.addItem(NodeItem(Node(None, None, "I", None, [500, 300]), self))
        # #TODO

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

    def on_sourcenode_action(self):
        form = InputFormSourceNode()
        form.show()
        form.exec_()
        value = str(form.confirm())
        print("value:", value)
        self.scene.addItem(
            SourceNodeItem(SourceNode(None, None, value, None, [250, 300]))
        )

    def on_arc_action(self):
        input_arc = Arc_Input()
        input_arc.show()
        input_arc.exec_()
        uid1 = input_arc.confirm()[0]
        uid2 = input_arc.confirm()[1]
        graph1 = graph.Graph()
        node1 = graph1.create_component(
            {
                "type": "Node",
                "name": "n1",
                "uid": uid1,
                "position_x": "200",
                "position_y": "300",
            }
        )
        node2 = graph1.create_component(
            {
                "type": "Node",
                "name": "n2",
                "uid": uid2,
                "position_x": "300",
                "position_y": "400",
            }
        )
        arc1 = Arc(graph1, None, "arc1", None, node1, node2, None, None)

        # print(arc1.nodes[0])
        print(node2.get_position())
        self.scene.addItem(ArcItem(arc1, graph1))
        self.scene.addItem(NodeItem(node1, None))
        self.scene.addItem(NodeItem(node2, None))

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
