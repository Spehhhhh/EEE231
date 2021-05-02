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
from PySide6.QtWidgets import QFileDialog, QMessageBox, QGraphicsItem , QGraphicsLineItem

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QBrush,QFont
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





    #抱歉实在不会写Class， 所以不知道怎么把东西拆开写


    
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("Pyside2 QGraphic View")
        self.setGeometry(300,200,500,500) # Main Window 的信息 （x位置，y位置，宽度，长度）
        self.createui() #创建UI界面
        self.show() #显示界面/UI

 

    def createui(self):
        
        #多余的旋转部分====================================
        button =QPushButton("Rotate - ", self)
        button.setGeometry(200,450, 100,50)
        button.clicked.connect(self.rotate_minus)
 
        button2 = QPushButton("Rotate + ", self)
        button2.setGeometry(320, 450, 100, 50)
        button2.clicked.connect(self.rotate_plus)
        #=================================================


        scene = QGraphicsScene(self) # QGraphicsScene 相当于一个容器，里面包括全部的图形（颜色，位置，大小这些）


        #3种颜色定义 (R,G,B)================================
        CurrentColour = QColor(0,128,128) #青色 代表Current Source
        GroundColour = QColor(255,215,0) #金色 代表Ground Node
        InternalColour = QColor(231,84,128) # 粉色 代表Internal Node

        #=================================================



        # QBrush 用来给图像上色， 青，金，粉=============
        tealBrush = QBrush(CurrentColour) 
        goldBrush = QBrush(GroundColour)
        pinkBrush = QBrush(InternalColour)
        #===============================================



        #图像的轮廓颜色===========================
        # QPen 定义为黑色
        blackOutline = QPen(Qt.black) # QPen = 黑色
        blackOutline.setWidth(1)
         #轮廓粗细
        #=========================================





        #创建图形 

        # 名称 = scene.addEllipse (x位置，y位置，宽，高, 轮廓（就是blackpen）) 创建一个圆形

        #===== 注意 宽和高 一定要一样才能是圆形=================================
        

        #可以用 循环LOOP 来 贴NODE？ 有几个就贴几个??


        #创建一个 Ground Node 位置 20，20， 圆形（30，30），黑色轮廓， 青色
        
        GroundNode = scene.addEllipse(20,20, 30, 30, blackOutline, tealBrush)
 

        #创建一个 Ground Node 位置 50，50， 圆形（30，30），黑色轮廓， 粉色
        InternalNode1 = scene.addEllipse(50,50, 30, 30, blackOutline, goldBrush)


        #创建一个 Current Node 位置 50，50， 圆形（30，30），黑色轮廓， 粉色
        CurrentNode1 = scene.addEllipse(80,80, 30, 30, blackOutline, pinkBrush)
        #=====================================================================



        # scene.addText("123456", QFont("Sanserif", 15)) #给界面上加字体， 应该用不到
 



        #SetFlag 设置Node 可移动=======================================================

        #这个设置也能用循环来写？ 

        GroundNode.setFlag(QGraphicsItem.ItemIsMovable) #设置GroundNode 1 可以移动 （跟鼠标）

        InternalNode1.setFlag(QGraphicsItem.ItemIsMovable) #设置InternalNode 1 可以移动 （跟鼠标）

        CurrentNode1.setFlag(QGraphicsItem.ItemIsMovable) #设置CurrentNode 1 可以移动 （跟鼠标）
        #=================================================================================
 


        #如果  QGraphicsScene 是容器， 那么 QGraphicsView 就是展示这个容器里面的东西
        self.view = QGraphicsView(scene, self)

        # View的参数 (x位置，y位置，宽，高) 这里的 x，y是从Windows的 x，y位置开始算的
        self.view.setGeometry(50,50,400, 400)


 
 
 
 #这里是界面旋转部分的函数=============================
    def rotate_minus(self):
        self.view.rotate(-14)
 
 #应该用不到
    def rotate_plus(self):
        self.view.rotate(14)
 #这里是界面旋转部分的函数==============================

 
 
 
app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())

