import sys

from PySide6.QtGui import QAction
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

from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import Node


class NodeItem(QGraphicsEllipseItem):
    # Global Config

    def __init__(self, node_instance):
        self.node = node_instance
        # self.x = self.node.position[0] # X
        # self.y = self.node.position[1] # Y

        self.node_radius = 25.0
        self.node_fill_colour = QColor(226, 170, 243)
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

    # def update_node_radius(self, node_radius_new):
    #     self.prepareGeometryChange()
    #     return

    # def update_node_name(self, node_name_new):
    #     self.prepareGeometryChange()
    #     self.node.update("name", node_name_new)
    #     return

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

    def itemChange(self, change, value):
        # Called by scene when item changes

        # if change == self.ItemPositionHasChanged:
        # Redraw all arcs connected to node

        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        # Handler for mousePressEvent
        mousePos = event.pos()
        self.selectionRectangle.setVisible(True)
        print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
        self.update()
        return

    def mouseReleaseEvent(self, event):
        # Handler for mouseReleaseEvent
        mousePos = event.pos()
        self.selectionRectangle.setVisible(False)
        print("mouseReleaseEvent at ", mousePos.x(), ", ", mousePos.y())
        self.update()
        return

    def mouseMoveEvent(self, event):
        # Handler for mouseMoveEvent
        scenePosition = event.scenePos()
        self.node.position[0] = scenePosition.x()
        self.node.position[1] = scenePosition.y()

        self.prepareGeometryChange()
        self.setPos(scenePosition)
        print("mouseMoveEvent to", scenePosition.x(), ", ", scenePosition.y())
        self.update()
        return

    def mouseDoubleClickEvent(self, event):
        # Handler for mouseDoubleClickEvent
        print("node item double clicked")
        self.update()
        return

    def setPos(self, pos):
        bounding = self.boundingRect()
        offset = bounding.center()
        super().setPos(pos - offset)


class DirectedGraphMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EEE231 Group B Program")

        self.scene = QGraphicsScene(0, 0, 500, 500, self)

        node1 = Node(None, None, "node1", None, [200, 200])
        nodeitem1 = NodeItem(node1)
        self.scene.addItem(nodeitem1)
        self.scene.addItem(NodeItem(Node(None, None, None, None, [100, 100])))

        self.view = QGraphicsView(self.scene)
        self.view.resize(1000, 1000)
        self.view.setRenderHints(QPainter.Antialiasing)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)


if __name__ == "__main__":
    app = QApplication([])

    mainwindow = DirectedGraphMainWindow()
    mainwindow.show()

    sys.exit(app.exec_())
