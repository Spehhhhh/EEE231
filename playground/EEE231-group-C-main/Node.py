#! /usr/bin/env python3

# Example PySide6 program -- pir -- 22.3.2021; 6.4.2021

# ******************************************************************************
# Insert licence here!


# ******************************************************************************

from sys import exit
from typing import Union

from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtWidgets import QToolBar, QStatusBar
from PySide6.QtWidgets import QFileDialog, QMessageBox

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QBrush
from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QGraphicsEllipseItem,
    QGraphicsPathItem,
    QGraphicsSimpleTextItem,
    QGraphicsRectItem,
    QGraphicsItemGroup,
)

from PySide6.QtGui import QFontMetrics


# ******************************************************************************


class NodeItem(QGraphicsEllipseItem):
    """
    Node class
    """

    # Global node colours, brushes, etc. fro all nodes
    # I increase this value beccause the old one is too small so that cannot show "ground node"
    nodeRadius = 50
    nodeFillColour = QColor(0, 0, 0)  # Naughty! Should not embed magic constants
    nodeFillBrush = QBrush(Qt.black, Qt.SolidPattern)
    nodeFillBrush.setColor(nodeFillColour)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        boundingRect = QRectF(
            x - self.nodeRadius,
            y - self.nodeRadius,
            2.0 * self.nodeRadius,
            2.0 * self.nodeRadius,
        )  # Bounding rectangle of node 'ellipse' i.e. circle
        super().__init__(boundingRect)  # Invoke __init__ of base class
        self.setZValue(0)
        self.setBrush(self.nodeFillBrush)
        self.toolTip = "this is a node"
        self.setToolTip(self.toolTip)

        # Add node text
        self.nodeText = ""

        # Set node attributes
        self.ItemIsSelectable = True
        self.ItemIsMovable = True
        self.ItemSendsGeometryChanges = True

        # Create selection rectangle shown when node is selected
        self.selectionRectangle = QGraphicsRectItem(self.boundingRect())
        self.selectionRectangle.setVisible(False)

        return

    # -------------------------------------------------------------------

    def setNodeRadius(self, radius):
        # Set global node drawing radius
        self.prepareGeometryChange()
        self.nodeRadius = radius
        return

    # -------------------------------------------------------------------

    def setNodeText(self, new_text):
        # Set node text
        self.prepareGeometryChange()
        self.nodeText = new_text
        return

    # -------------------------------------------------------------------

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
        painter.setBrush(self.nodeFillBrush)
        painter.drawEllipse(boundingRect)

        # Paint node text
        painter.setPen(Qt.black)
        painter.drawText(
            boundingRect, Qt.AlignCenter, self.nodeText
        )  # Clips nodeText. TODO - generate more accurate bounding rectangle for text

        # fm = painter.fontMetrics()
        # textBoundingRect = fm.boundingRect(self.nodeText)
        # boundingRectOffset = QPoint(boundingRect.x() + (boundingRect.width()) / 2.0, boundingRect.y() + (boundingRect.height()) / 2.0)
        # textBoundingRect.moveCenter(boundingRectOffset)
        # textBoundingRect.adjust(-10,-10, 10, 10)
        # painter.drawText(textBoundingRect, Qt.AlignCenter, self.nodeText)

        print("paint called @ ", self.x, ", ", self.y)

        return

    # -------------------------------------------------------------------

    def itemChange(self, change, value):
        # Called by scene when item changes

        # if change == self.ItemPositionHasChanged:
        # Redraw all  arcs  connected to node

        return super().itemChange(change, value)

    # -------------------------------------------------------------------

    def mousePressEvent(self, event):
        # Handler for mouse press event
        mousePos = event.pos()
        print("mouse press event at", mousePos.x(), ", ", mousePos.y())

        self.selectionRectangle.setVisible(True)

        return

    # -------------------------------------------------------------------

    def mouseReleaseEvent(self, event):
        # Handler for mouse release event
        mousePos = event.pos()
        # Select an area
        self.selectionRectangle.setVisible(True)
        print("mouse release event at ", mousePos.x(), ", ", mousePos.y())

        return

    # -------------------------------------------------------------------

    def mouseMoveEvent(self, event):
        # Handler for mouse move event

        # last recorded mouse cursor position
        Mouse_point = event.lastScenePos()

        # The original component position
        original_position = self.scenePos()

        # Current mouse cursor position
        scenePosition = event.scenePos()
        self.x = scenePosition.x() + original_position.x() - Mouse_point.x()
        self.y = scenePosition.y() + original_position.y() - Mouse_point.y()

        self.prepareGeometryChange()
        # Fix this one to update the current parameter
        self.setPos(QPointF(self.x, self.y))
        print("move to", scenePosition.x(), ", ", scenePosition.y())
        self.update()

        return

    # -------------------------------------------------------------------

    def mouseDoubleClickEvent(self, event):
        # Handler for mouse double click event

        print("node item double clicked")

        # self.scene.update()

        return

    # Fill colour
    def Fill_colour(self, x, y, z):
        self.nodeFillColour = QColor(
            x, y, z
        )  # Naughty! Should not embed magic constants
        self.nodeFillBrush = QBrush(Qt.black, Qt.SolidPattern)
        self.nodeFillBrush.setColor(self.nodeFillColour)
        return


# ******************************************************************************


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Invoke __init__ of QMainWindow base class

        # Count for ground node
        self.count_GN = 0
        # Count for internal node
        self.count_IN = 0
        # Count for current source node
        self.count_CS = 0

        self.setWindowTitle("EEE231 Group C Program")
        self.mainLayout = QVBoxLayout()

        # Setup menu bar & File menu
        self.fileMenu = self.menuBar().addMenu("&File")
        self.openMenuAction = self.fileMenu.addAction("&Open")
        self.openMenuAction.triggered.connect(self.on_open_action)  # New-style connect!
        self.fileMenu.addSeparator()
        self.quitMenuAction = self.fileMenu.addAction("&Quit")
        self.quitMenuAction.triggered.connect(self.on_quit_action)

        # Setup Tools menu
        self.toolsMenu = self.menuBar().addMenu("&Tools")
        self.preferencesMenuAction = self.toolsMenu.addAction("&Preferences")
        self.preferencesMenuAction.triggered.connect(self.on_preferences_action)

        # Setup new component menu
        self.NewcomponentMenu = self.menuBar().addMenu("&New Component")
        self.NewcomponentAction = self.NewcomponentMenu.addAction("&Ground Node")
        self.NewcomponentAction.triggered.connect(self.Ground_Node_action)

        self.NewcomponentAction = self.NewcomponentMenu.addAction("&Internal Node")
        self.NewcomponentAction.triggered.connect(self.Internal_Node_action)

        self.NewcomponentAction = self.NewcomponentMenu.addAction("&Current Source")
        self.NewcomponentAction.triggered.connect(self.Current_Source_action)

        self.NewcomponentAction = self.NewcomponentMenu.addAction("&Arc")

        # Setup About menu
        self.aboutMenu = self.menuBar().addMenu("&About")
        self.aboutMenuAction = self.aboutMenu.addAction("&About")
        self.aboutMenuAction.triggered.connect(self.on_about_action)

        # Create main toolbar
        self.mainToolBar = QToolBar()
        self.mainToolBar.setMovable(False)
        self.newToolButton = self.mainToolBar.addAction("New")
        self.openToolButton = self.mainToolBar.addAction("Open")
        self.openToolButton.triggered.connect(self.on_open_action)
        self.saveToolButton = self.mainToolBar.addAction("Save")
        self.saveAsToolButton = self.mainToolBar.addAction("Save As")
        self.addToolBar(self.mainToolBar)
        self.mainLayout.addWidget(self.mainToolBar)

        # Create graphics scene
        self.graphicsScene = QGraphicsScene(
            0, 0, 511, 511, self
        )  # Naughty! Should not be embedding 'magic' constants in a program!!!

        # nodeA = NodeItem(250, 250)
        # self.graphicsScene.addItem(nodeA)
        # nodeA.setNodeText("new node")
        #
        # # Set node fill colour
        # nodeFillColour = QColor(0, 170, 243)  # Ditto!
        # nodeFillBrush = QBrush(Qt.black, Qt.SolidPattern)
        # nodeFillBrush.setColor(nodeFillColour)

        # # Create example node graphics item (1)
        # x1 = 100.0
        # y1 = 100.0
        # self.nodeRadius = 25.0
        # nodeCentre_1 = QPointF(x1, y1)
        # rect_1 = QRectF(x1 - self.nodeRadius, y1 - self.nodeRadius, 2.0 * self.nodeRadius,
        #                 2.0 * self.nodeRadius)  # Bounding rectangle of node 'ellipse'
        # nodeGraphicsItem_1 = QGraphicsEllipseItem(
        #     rect_1)  # NB. Parameter defines the bounding rectangle of the ellipse!
        # nodeGraphicsItem_1.setZValue(0)
        # nodeGraphicsItem_1.setBrush(nodeFillBrush)
        # nodeGraphicsItem_1.setToolTip("this is node 1")
        #
        # nodeTextItem_1 = QGraphicsSimpleTextItem("Node 1")
        # boundingRect_1 = nodeTextItem_1.boundingRect()
        # nodeTextItem_1.setPos(nodeCentre_1.x() - boundingRect_1.width() / 2,
        #                       nodeCentre_1.y() - boundingRect_1.height() / 2)
        # nodeGraphicsGroup_1 = QGraphicsItemGroup()
        # nodeGraphicsGroup_1.addToGroup(nodeGraphicsItem_1)
        # nodeGraphicsGroup_1.addToGroup(nodeTextItem_1)
        # self.graphicsScene.addItem(nodeGraphicsGroup_1)
        #
        # # Create example node graphics item (1)
        # x2 = 100.0
        # y2 = 200.0
        # nodeCentre_2 = QPointF(x2, y2)
        # rect_2 = QRectF(x2 - self.nodeRadius, y2 - self.nodeRadius, 2.0 * self.nodeRadius, 2.0 * self.nodeRadius)
        # nodeGraphicsItem_2 = QGraphicsEllipseItem(rect_2)
        # nodeGraphicsItem_2.setZValue(0)
        # nodeGraphicsItem_2.setBrush(nodeFillBrush)
        # nodeGraphicsItem_2.setToolTip("this is node 2")
        #
        # nodeTextItem_2 = QGraphicsSimpleTextItem("Node 2")
        # boundingRect_2 = nodeTextItem_1.boundingRect()
        # nodeTextItem_2.setPos(nodeCentre_2.x() - boundingRect_2.width() / 2,
        #                       nodeCentre_2.y() - boundingRect_2.height() / 2)
        # nodeGraphicsGroup_2 = QGraphicsItemGroup()
        # nodeGraphicsGroup_2.addToGroup(nodeGraphicsItem_2)
        # nodeGraphicsGroup_2.addToGroup(nodeTextItem_2)
        # self.graphicsScene.addItem(nodeGraphicsGroup_2)
        #
        # # Create example arc (1)
        # arc_PainterPath_1 = QPainterPath(nodeCentre_1)
        # ctrlX_1 = 50.0
        # ctrlY_1 = 150.0
        # arc_PainterPath_1.quadTo(ctrlX_1, ctrlY_1, nodeCentre_2.x(), nodeCentre_2.y())
        # arcGraphicItem_1 = QGraphicsPathItem(arc_PainterPath_1)
        # arcGraphicItem_1.setZValue(-1)  # Hides path below nodes
        # arcGraphicItem_1.setToolTip("arc 1")
        # self.graphicsScene.addItem(arcGraphicItem_1)
        #
        # # Create example arc (2)
        # arc_PainterPath_2 = QPainterPath(nodeCentre_1)
        # ctrlX_2 = 150.0
        # ctrlY_2 = 150.0
        # arc_PainterPath_2.quadTo(ctrlX_2, ctrlY_2, nodeCentre_2.x(), nodeCentre_2.y())
        # arcGraphicItem_2 = QGraphicsPathItem(arc_PainterPath_2)
        # arcGraphicItem_2.setZValue(-1)  # Hides path below nodes
        # arcGraphicItem_2.setToolTip("arc 2")
        # self.graphicsScene.addItem(arcGraphicItem_2)

        # Create graphics view
        self.graphicsView = QGraphicsView(self.graphicsScene)
        self.graphicsView.setDragMode(QGraphicsView.RubberBandDrag)
        self.graphicsView.setRubberBandSelectionMode(Qt.ContainsItemBoundingRect)
        self.graphicsView.setRenderHints(QPainter.Antialiasing)
        self.mainLayout.addWidget(self.graphicsView)

        # Is a status bar needed in this application?
        self.statusBar = QStatusBar()
        self.mainLayout.addWidget(self.statusBar)

        # Set mainLayout as the central widget
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

    # --------------------------------------------------------------------------

    def on_open_action(self):
        """Handler for 'Open' action"""
        fileName = QFileDialog.getOpenFileName(self, "Open File", ".", ("*.md"))
        print("opening ", fileName[0])
        return

    # --------------------------------------------------------------------------

    def on_quit_action(self):
        """Handler for 'Quit' action"""
        print("quitting application")
        self.close()
        return

    # --------------------------------------------------------------------------

    def on_preferences_action(self):
        """Handler for 'Preferences' action"""
        print("preferences")
        return

    # --------------------------------------------------------------------------

    def on_about_action(self):
        """Handler for 'About' action"""
        QMessageBox.about(
            self,
            "About this program",
            "some about text crediting the people who wrote this",
        )
        return

    # Ground node
    def Ground_Node_action(self):
        if self.count_GN == 0:
            Ground_Node = NodeItem(250, 250)
            # Fill gold colour
            Ground_Node.Fill_colour(255, 215, 0)  # Ditto!
            Ground_Node.setBrush(Ground_Node.nodeFillColour)
            self.graphicsScene.addItem(Ground_Node)
            Ground_Node.setNodeText("Ground node")
            self.count_GN = 1
        else:
            # Create a warning message for user
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Only one ground node is allowed")
            msg.show()
            msg.exec_()

    # Internal node
    def Internal_Node_action(self):
        self.count_IN = self.count_IN + 1
        Internal_Node = NodeItem(250, 250)
        self.graphicsScene.addItem(Internal_Node)
        Internal_Node.setNodeText("Internal node " + str(self.count_IN))
        # Fill pink colour
        Internal_Node.Fill_colour(255, 192, 203)  # Ditto!
        Internal_Node.setBrush(Internal_Node.nodeFillColour)
        # Ask for internal node value

    # Current source node
    def Current_Source_action(self):
        self.count_CS = self.count_CS + 1
        Current_Source = NodeItem(250, 250)
        self.graphicsScene.addItem(Current_Source)
        Current_Source.setNodeText("Current Source " + str(self.count_CS))
        # Fill teal colour
        Current_Source.Fill_colour(0, 128, 128)  # Ditto!
        Current_Source.setBrush(Current_Source.nodeFillColour)
        # Ask for current source value


# ******************************************************************************

# Main program
if __name__ == "__main__":
    application = QApplication([])

    mainWindow = MainWindow()
    mainWindow.show()

    exit(
        application.exec_()
    )  # Not sure why this still has to be `exec_` with a trailing underscore? Despite what the documentation says...

# ******************************************************************************
