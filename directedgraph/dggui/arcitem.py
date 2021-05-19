from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QAction, QPainterPath
from PySide6.QtWidgets import QMenu, QGraphicsPathItem, QInputDialog

import random


class ArcItem(QGraphicsPathItem):
    def __init__(self, arc_instance, main_window_instance=None):
        self.arc = arc_instance
        self.arc.connected_gui = self
        self.arc.connected_window = main_window_instance
        self.connected_window = main_window_instance
        random_list = [-30, -25, -20, -15, -10, 10, 15, 20, 30]
        # self.curvature = random.randint(-30, -10) * random.randint(1)
        self.curvature = random.choice(random_list)
        print(self.curvature)

        self.start_point = QPointF()
        self.start_point.setX(self.arc.nodes[0].position[0])
        self.start_point.setY(self.arc.nodes[0].position[1])

        self.mid_point = QPointF()
        self.mid_point.setX(
            (self.arc.nodes[0].position[0] + self.arc.nodes[1].position[0]) / 2
            - self.curvature * 6
        )
        self.mid_point.setY(
            (self.arc.nodes[0].position[1] + self.arc.nodes[1].position[1]) / 2
            - self.curvature * 6
        )

        self.end_point = QPointF()
        self.end_point.setX(self.arc.nodes[1].position[0])
        self.end_point.setY(self.arc.nodes[1].position[1])

        self.arc_PainterPath = QPainterPath(self.start_point)
        self.arc_PainterPath.quadTo(
            self.mid_point.x(),
            self.mid_point.y(),
            self.end_point.x(),
            self.end_point.y(),
        )
        print("start", self.start_point)
        print("mid", self.mid_point)
        print("end", self.end_point)

        super().__init__(self.arc_PainterPath)
        # self.bounding_rect = self.boundingRect()
        self.setZValue(-1)
        # self.setToolTip("Arc 1")
        # self.line =QLineF(self.start, self.end)
        pass

    # def paint(self, painter, option, parent):
    def paint(self, painter, QStyleOptionGraphicsItem, QWidget_widget=None):
        self.prepareGeometryChange()

        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)

        self.start_point.setX(self.arc.nodes[0].position[0])
        self.start_point.setY(self.arc.nodes[0].position[1])

        self.mid_point.setX(
            (self.arc.nodes[0].position[0] + self.arc.nodes[1].position[0]) / 2
            - self.curvature * 4
        )
        self.mid_point.setY(
            (self.arc.nodes[0].position[1] + self.arc.nodes[1].position[1]) / 2
            - self.curvature * 4
        )

        self.end_point.setX(self.arc.nodes[1].position[0])
        self.end_point.setY(self.arc.nodes[1].position[1])

        self.arc_PainterPath = QPainterPath(self.start_point)
        self.arc_PainterPath.quadTo(
            self.mid_point.x(),
            self.mid_point.y(),
            self.end_point.x(),
            self.end_point.y(),
        )
        # self.setZValue(-1)
        painter.drawPath(self.arc_PainterPath)

        # start_point_map = self.mapToItem(self, self.start_point())
        # end_point_map = self.mapToItem(self, self.end_point())

        # self.bounding_rect = QRectF(
        #     self.start_point_map.x(),
        #     self.end_point_map.y(),
        #     self.end_point_map.x(),
        #     self.start_point_map.y(),
        # )

        # print(self.bounding_rect)
        painter.drawText(
            self.mid_point.x() + self.curvature * 2,
            self.mid_point.y() + self.curvature * 2,
            self.arc.name,
        )
        # painter.drawText(self.bounding_rect, Qt.AlignCenter, self.arc.name)

        # pen = QPen()
        # pen.setWidth(2) #线的宽度 数值越大越宽
        # QPainter.setPen(pen)
        # QPainterPath(self.start)
        # QPainter.drawLine(self.line)

        # QPainter.drawPath(self.line)
        # print("Paint Call")
        self.connected_window.scene.update()
        return

    def mouseMoveEvent(self, event):
        # self.prepareGeometryChange()
        # scenePosition = event.scenePos()
        # self.setPos(scenePosition)
        # self.update()
        return

    def setPos(self, pos):
        # bounding = self.boundingRect()
        # offset = bounding.center()
        # super().setPos(pos - offset)
        # self.update()
        return

    def contextMenuEvent(self, event):
        # Pop up menu for Node
        popmenu = QMenu()

        # Name
        nameAction = QAction("Edit Name")
        popmenu.addAction(nameAction)
        nameAction.triggered.connect(self.on_name_action)

        popmenu.addSeparator()

        # Delete
        deleteAction = QAction("Delete")
        popmenu.addAction(deleteAction)
        deleteAction.triggered.connect(self.on_delete_action)

        # Excute at node Position, so it won't collide with Main windows pop-up menu
        popmenu.exec_(event.screenPos())

    def on_name_action(self):
        text, result = QInputDialog.getText(
            self.connected_window,
            "Input",
            "Enter Name",
            QtWidgets.QLineEdit.Normal,
        )
        if result == True:
            self.arc.name = str(text)

    def on_delete_action(self):
        self.arc.connected_graph.delete_component(self.arc.uid)
        self.connected_window.scene.removeItem(self)
        pass