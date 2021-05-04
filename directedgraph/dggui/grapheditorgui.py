from PySide6.QtGui import QAction
from PySide6 import QtGui, QtWidgets
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
from PySide6.QtCore import Qt, QPointF, QRectF, QEvent
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

import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import Node, GroundNode, SourceNode, Arc
from directedgraph.dgcore.excp import GroundNodeNumberException


class NodeItem(QGraphicsEllipseItem, QWidget):
    # Global Config

    def __init__(self, node_instance):
        self.node = node_instance
        self.node_radius = 25.0
        self.node_fill_colour = QColor(231, 84, 128)
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

    def mousePressEvent(self, event):
        # Handler for mousePressEvent
        self.prepareGeometryChange()
        mousePos = event.pos()
        self.selectionRectangle.setVisible(True)
        print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
        # self.update()
        return

    # def eventFilter(self, source, event):

    #     if event.type() == QEvent.MouseButtonPress:
    #         print(source)
    #     # if QMouseEvent.button() == Qt.LeftButton:
    #     #     mousePos = QMouseEvent.pos()
    #     #     self.selectionRectangle.setVisible(True)
    #     #     print("Left Button Clicked")
    #     #     print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
    #     #     # self.update()
    #     #     return
    #     # elif QMouseEvent.button() == Qt.RightButton:
    #     #     print("Right Button Clicked")
    #     #     QMenu
    #     #     return
    #     return super().eventFilter(source, event)

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

    def mousePressEvent(self, event):
        # Handler for mousePressEvent
        self.prepareGeometryChange()
        mousePos = event.pos()
        self.selectionRectangle.setVisible(True)
        print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
        # self.update()
        return

    # def eventFilter(self, source, event):

    #     if event.type() == QEvent.MouseButtonPress:
    #         print(source)
    #     # if QMouseEvent.button() == Qt.LeftButton:
    #     #     mousePos = QMouseEvent.pos()
    #     #     self.selectionRectangle.setVisible(True)
    #     #     print("Left Button Clicked")
    #     #     print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
    #     #     # self.update()
    #     #     return
    #     # elif QMouseEvent.button() == Qt.RightButton:
    #     #     print("Right Button Clicked")
    #     #     QMenu
    #     #     return
    #     return super().eventFilter(source, event)

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

class SourceNodeItem(QGraphicsEllipseItem):
    # Global Config

    def __init__(self, node_instance):
        self.node = node_instance
        self.node_radius = 40.0
        self.node_fill_colour = QColor(0, 128, 128)
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

    def mousePressEvent(self, event):
        # Handler for mousePressEvent
        self.prepareGeometryChange()
        mousePos = event.pos()
        self.selectionRectangle.setVisible(True)
        print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
        # self.update()
        return

    # def eventFilter(self, source, event):

    #     if event.type() == QEvent.MouseButtonPress:
    #         print(source)
    #     # if QMouseEvent.button() == Qt.LeftButton:
    #     #     mousePos = QMouseEvent.pos()
    #     #     self.selectionRectangle.setVisible(True)
    #     #     print("Left Button Clicked")
    #     #     print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
    #     #     # self.update()
    #     #     return
    #     # elif QMouseEvent.button() == Qt.RightButton:
    #     #     print("Right Button Clicked")
    #     #     QMenu
    #     #     return
    #     return super().eventFilter(source, event)

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
class DirectedGraphMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI editor")
        self.ground_node_count = 0
        self.scene = QGraphicsScene(0, 0, 500, 500, self)
        self.view = QGraphicsView(self.scene)
        self.view.resize(1000, 1000)
        self.view.setRenderHints(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
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

        # Setup About menu
        self.aboutMenu = self.menuBar().addMenu("&About")
        self.aboutMenuAction = self.aboutMenu.addAction("&About")
        self.aboutMenuAction.triggered.connect(self.on_about_action)
        self.setCentralWidget(self.widget)

        # Setup GraphComponent menu
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
        self.saveToolButton.triggered.connect(self.file_save)
        self.saveAsToolButton = self.mainToolBar.addAction("Save As")
        self.addToolBar(self.mainToolBar)
        self.layout.addWidget(self.mainToolBar)
        self.init_graph()

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

    def on_node(self):
        self.scene.addItem(NodeItem(Node(None, None, None, None, [500, 300])))

    def on_groundnode(self):
        self.ground_node_count += 1
        if self.ground_node_count > 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Only one ground_node is allowed!!!")
            msg.show()
            msg.exec_()
            raise GroundNodeNumberException("oops!!")
        else:
            self.scene.addItem(
                GroundNodeItem(GroundNode(None, None, "groundnode1", None, [500, 300]))
            )
    def on_sourcenode(self):
        self.scene.addItem(
            SourceNodeItem(SourceNode(None, None, "sourcenode1", None, [250, 300]))
        )

    def init_graph(self):
        self.scene.addItem(NodeItem(Node(None, None, "node1", None, [200, 200])))
        self.scene.addItem(NodeItem(Node(None, None, None, None, [100, 100])))
        test = NodeItem(Node(None, None, None, None, [300, 300]))
        self.scene.addItem(test)

        # menu = QMenu()
        # menu.addAction("Action 1")
        # menu.addAction("Action 2")
        # menu.addAction("Action 3")
        # menu.exec_()
        # self.scene.addItem(menu)

    def event_filter(self, source, event):
        pass

    def file_save(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, "Save File")
        file = open(name[0], "w")
        # 传输xml格式，使用filemanager
        text = "sasd"
        file.write(text)
        file.close()


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
