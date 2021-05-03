#! /usr/bin/env python3
import sys
from sys import exit

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtWidgets import QMenuBar, QMenu, QPushButton
from PySide6.QtWidgets import QToolBar, QStatusBar
from PySide6.QtWidgets import QFileDialog, QMessageBox, QGraphicsItem, QGraphicsLineItem

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QBrush, QFont
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


"""class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        #Window name, in this case Trial
        self.setWindowTitle("Trial")
        
        self.setGeometry(300,200,640,520) # xposition, yposition,  width, height

        
        self.show()


        def create_ui(self):
            scene = QGraphicsScene(self) #QGraphicsScene atcs as a container for graphical element

            greenBrush = QBrush(Qt.green)
            greenBrush = QBrush(Qt.blue)

            blackPen = QPen(Qt.black)
            blackPen.setWidth(5)


            ellipse = scene.addEllipse(10,10,200,200, blackPen, greenBrush) #graphical element ellipes contained in scene

            self.view = QGraphicsView(scene, self)
            self.view.setGeometry(0,0,640,440)

        self.create_ui()

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())"""

"""    class GroundNode(QGraphicsEllipseItem):

    
    nodeFillColour = QColor(0,128,128) 
    nodeFillBrush = QBrush(Qt.black, Qt.SolidPattern)
    nodeFillBrush.setColor(nodeFillColour)

    def__init__(self):

    
    self.toolTip = "this is a node"
    self.setToolTip(self.toolTip)"""


# 抱歉实在不会写Class， 所以不知道怎么把东西拆开写


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pyside2 QGraphic View")
        self.setGeometry(
            300, 200, 500, 500
        )  # Main Window 的信息 （x位置，y位置，宽度，长度）   #Some Definition on the Main window
        self.createui()  # 创建UI界面      Create UI
        self.show()  # 显示界面/UI         Shows the UI

    def createui(self):

        # Rotation parts Useless (Maybe)

        # 多余的旋转部分====================================
        button = QPushButton("Rotate - ", self)
        button.setGeometry(200, 450, 100, 50)
        button.clicked.connect(self.rotate_minus)

        button2 = QPushButton("Rotate + ", self)
        button2.setGeometry(320, 450, 100, 50)
        button2.clicked.connect(self.rotate_plus)
        # =================================================

        scene = QGraphicsScene(
            self
        )  # QGraphicsScene 相当于一个容器，里面包括全部的图形（颜色，位置，大小这些）QGraphicsScene is like a container which contain all the shape, location,size

        # Define 3 Colour, Teal, Gold, Pink in terms of R G B , response to Curren, Ground and INternal
        # 3种颜色定义 (R,G,B)================================
        CurrentColour = QColor(0, 128, 128)  # 青色 代表Current Source
        GroundColour = QColor(255, 215, 0)  # 金色 代表Ground Node
        InternalColour = QColor(231, 84, 128)  # 粉色 代表Internal Node

        # =================================================

        # QBrush is used to fill the colour of the node, e.g tealBrsh would make the node colour to be Teal
        # QBrush 用来给图像上色， 青，金，粉=============
        tealBrush = QBrush(CurrentColour)
        goldBrush = QBrush(GroundColour)
        pinkBrush = QBrush(InternalColour)
        # ===============================================

        # The outline of the shape I have define the outline to be black in here
        # 图像的轮廓颜色===========================
        # QPen 定义为黑色
        blackOutline = QPen(Qt.black)  # QPen = 黑色
        blackOutline.setWidth(1)
        # 轮廓粗细  This sets the width of the outline
        # =========================================

        # 创建图形 Create the shapes

        # 名称 = scene.addEllipse (x位置，y位置，宽，高, 轮廓（就是blackpen）) 创建一个圆形 by scen.addEllipse

        # ===== 注意 宽和高 一定要一样才能是圆形=================================

        # 可以用 循环LOOP 来 贴NODE？ 有几个就贴几个??

        # 创建一个 Ground Node 位置 20，20， 圆形（30，30），黑色轮廓， 青色

        # Create a ground node with coordinate 20,20, balckoutline and teal clolur
        GroundNode = scene.addEllipse(20, 20, 30, 30, blackOutline, tealBrush)

        # 创建一个 Ground Node 位置 50，50， 圆形（30，30），黑色轮廓， 粉色

        # Simular to the ground node, but differen x,y coordinate and colour
        InternalNode1 = scene.addEllipse(50, 50, 30, 30, blackOutline, goldBrush)

        # 创建一个 Current Node 位置 50，50， 圆形（30，30），黑色轮廓， 粉色
        # Same prinsipal appied in here
        CurrentNode1 = scene.addEllipse(80, 80, 30, 30, blackOutline, pinkBrush)
        # =====================================================================

        # scene.addText("123456", QFont("Sanserif", 15)) #给界面上加字体， 应该用不到 Add text in the UI, useless (may be)

        # SetFlag 设置Node 可移动=======================================================

        # 这个设置也能用循环来写？

        # setflag to make the node moveable (will follow the mouse)

        GroundNode.setFlag(QGraphicsItem.ItemIsMovable)  # 设置GroundNode 1 可以移动 （跟鼠标）

        InternalNode1.setFlag(
            QGraphicsItem.ItemIsMovable
        )  # 设置InternalNode 1 可以移动 （跟鼠标）

        CurrentNode1.setFlag(QGraphicsItem.ItemIsMovable)  # 设置CurrentNode 1 可以移动 （跟鼠标）
        # =================================================================================

        # 如果  QGraphicsScene 是容器， 那么 QGraphicsView 就是展示这个容器里面的东西
        # To shows all the things above
        self.view = QGraphicsView(scene, self)

        # View的参数 (x位置，y位置，宽，高) 这里的 x，y是从Windows的 x，y位置开始算的
        # define x,y coordinate, with width and height
        self.view.setGeometry(50, 50, 400, 400)

    # Below is the function for the rotation useless (Maybe)
    # 这里是界面旋转部分的函数=============================
    def rotate_minus(self):
        self.view.rotate(-14)

    # 应该用不到
    def rotate_plus(self):
        self.view.rotate(14)


# 这里是界面旋转部分的函数==============================


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
