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
        self.x = self.node.position[0]
        self.y = self.node.position[1]

        self.node_radius = 25.0
        self.node_fill_colour = QColor(226, 170, 243)
        self.node_fill_brush = QBrush(Qt.black, Qt.SolidPattern)
        self.node_fill_brush.setColor(self.node_fill_colour)

        bounding_shape = QRectF(
            self.x - self.node_radius,
            self.y - self.node_radius,
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

    def update_node_radius(self, node_radius_new):
        self.n


class DirectedGraphMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EEE231 Group B Program")

        self.scene = QGraphicsScene(0, 0, 500, 500, self)

        node1 = Node(None, None, "node1", None, [10, 10])
        node1.update_position([100, 100])
        nodeitem1 = NodeItem(node1)
        self.scene.addItem(nodeitem1)

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
