#! /usr/bin/env python3

# selection rectangle is unviewable(strange spelling) when releaseMouseEven is used
# we can change node radius by using nodeRadius function now
# node bias have been solved
# node creating module added and it will connect to ground node automatically
# arc folling module added(but dont know how to fresh the whole painting page)

#v1 07/05/21

#******************************************************************************

from sys import exit

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtWidgets import QToolBar, QStatusBar
from PySide6.QtWidgets import QFileDialog, QMessageBox

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QBrush, QIcon
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsSimpleTextItem, QGraphicsRectItem, QGraphicsItemGroup

from PySide6.QtGui import QFontMetrics

#******************************************************************************
class NodeItem(QGraphicsEllipseItem):
    """
    Node class 
    """
    # Global node colours, brushes, etc. fro all nodes
    nodeRadius = 25.0
    original_x=0
    original_y=0
    nodeFillColour = QColor(226, 170, 243) # Naughty! Should not embed magic constants
    nodeFillBrush = QBrush(Qt.black, Qt.SolidPattern)   
    nodeFillBrush.setColor(nodeFillColour)
    # Add node text 
    nodeText = ""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nodeId=ItemList.maximumNodeId+1
        self.original_x=x
        self.original_y=y
        #self.arc1=ArcItem(QPointF(100,100),QPointF(300,300))
        boundingRect = QRectF(x - self.nodeRadius, y - self.nodeRadius, 2.0 * self.nodeRadius, 2.0 * self.nodeRadius)   # Bounding rectangle of node 'ellipse' i.e. circle
        super().__init__(boundingRect)  # Invoke __init__ of base class
        self.setZValue(0)
        self.setBrush(self.nodeFillBrush)
        self.toolTip =  "node "+str(self.nodeId)
        self.setToolTip(self.toolTip)
        
        # Set node attributes
        self.ItemIsSelectable = True
        self.ItemIsMovable = True
        self.ItemSendsGeometryChanges = True
        
        # Create selection rectangle shown when node is selected
        self.selectionRectangle = QGraphicsRectItem(self.boundingRect())
        self.selectionRectangle.setVisible(False)
         
        return
        
    #-------------------------------------------------------------------
            
    def setNodeRadius(self, radius):
        # Set global node drawing radius
        self.prepareGeometryChange()
        self.nodeRadius = radius
        print("radius", self.nodeRadius)
        return
                
    #-------------------------------------------------------------------

    def setNodeText(self, new_text):
        # Set node text
        self.prepareGeometryChange()
        self.nodeText = new_text
        return

    #-------------------------------------------------------------------
      
    def paint(self, painter, option, parent):
        # Paint the node instance - called by QGraphicView instance
        #boundingRect = self.boundingRect()
        boundingRect = QRectF(self.original_x - self.nodeRadius, self.original_y - self.nodeRadius, 2.0 * self.nodeRadius, 2.0 * self.nodeRadius)
        
        if self.selectionRectangle.isVisible():
            # Paint selection rectangle
            painter.setPen(Qt.SolidLine)
            painter.setBrush(Qt.NoBrush)
            self.selectionRectangle.setRect(boundingRect)
            painter.drawRect(boundingRect)

        # Paint node circle
        painter.setBrush(self.nodeFillBrush)
        painter.drawEllipse(boundingRect)
        
        # Paint node text
        painter.setPen(Qt.black)
        painter.drawText(boundingRect, Qt.AlignCenter, self.nodeText)   # Clips nodeText. TODO - generate more accurate bounding retangle for text

        #print("paint called @ ", self.x, ", ", self.y,)
        
        return
        
    #-------------------------------------------------------------------
    
    def itemChange(self, change, value):
        # Called by scene when item changes
        print("change", self.nodeText, value)
        #if change == self.ItemPositionChange:
            # Redraw all  arcs  connected to node
            
        
        self.update()
        
        return super().itemChange(change, value)
        
     #-------------------------------------------------------------------
     
    def mousePressEvent(self, event):
        # Handler for mouse press event
        mousePos = event.pos()
        print("mouse press event at", mousePos.x(), ", ", mousePos.y())
        
        self.selectionRectangle.setVisible(True)
        self.update()
        
        return

    #-------------------------------------------------------------------
 
    def mouseReleaseEvent(self, event):
        # Handler for mouse release event
        mousePos = event.pos()
        self.selectionRectangle.setVisible(False)
        if self.nodeText!="ground":
            ItemList.AddNodeList(self.nodeId,QPointF(self.x+self.original_x,self.y+self.original_y),self.nodeText,self.nodeRadius)
            print("mouse release event at ", mousePos.x(), ", ", mousePos.y())
        self.update()
              
        return
        
    #-------------------------------------------------------------------
    
    def mouseMoveEvent(self, event):
        # Handler for mouse move event
        if self.nodeText!="ground":
            scenePosition = event.scenePos()
            self.x = scenePosition.x()-self.original_x
            self.y = scenePosition.y()-self.original_y
            
            self.prepareGeometryChange()
            self.setPos(QPointF(self.x,self.y))
            print("node ",self.nodeId," move to (", scenePosition.x(), scenePosition.y(),")")
            self.arc.arcChange(QPointF(self.x,self.y))

            self.update()

        else:
            print("gorund node, can't move")

        return

    #-------------------------------------------------------------------        
    
    def mouseDoubleClickEvent(self, event):
        # Handler for mouse double click event

        if ItemList.selectedNodeId==-1:
            ItemList.selectedNodeId=self.nodeId
        else:
            exec('ItemList.AddArcList(node{},node{})'.format(ItemList.selectedNodeId,self.nodeId))
            ItemList.selectedNodeId=-1

        print("mouse double click event at node",self.nodeId)
        self.update()
        
        return
    
    #-------------------------------------------------------------------        
    
    def arcConnection(self,ArcItem):
        self.arc=ArcItem
        print("arc connection added")

        return

#******************************************************************************

class ArcItem (QGraphicsPathItem):
    C = QPointF(0,0)
    arcID=0

    def __init__(self,nodeCentre_A,nodeCentre_B):
        self.A=nodeCentre_A
        self.B=nodeCentre_B

        self.startPosition=self.B
        self.midPosition=QPointF((self.A.x()+self.B.x())/2,(self.A.y()+self.B.y())/2)
        self.endPosition=self.A

        path=QPainterPath(self.startPosition)
        path.quadTo(self.midPosition.x(),self.midPosition.y(),self.endPosition.x(),self.endPosition.y())
        super().__init__(path)

        #print("path added", path)
        self.setZValue(-1)
        self.toolTip= "this is an arc"
        self.setToolTip(self.toolTip)

        return 
    
    def arcChange(self,nodeCentre_C):
        self.C = nodeCentre_C
        self.prepareGeometryChange()
        self.setPos(QPointF(nodeCentre_C.x(),nodeCentre_C.y()))

        self.startPosition=self.B
        self.midPosition=QPointF((self.A.x()-self.C.x()+self.B.x())/2,(self.A.y()-self.C.y()+self.B.y())/2)
        self.endPosition=QPointF(self.A.x()-self.C.x(),self.A.y()-self.C.y())

        print ("arc change")
        #self.update(0,0,100,100)

        return

    def paint(self, painter, option, parent):
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)

        path=QPainterPath(self.startPosition)
        path.quadTo(self.midPosition.x(),self.midPosition.y(),self.endPosition.x(),self.endPosition.y())

        painter.drawPath(path)
        print("arc move to (",self.startPosition.x(),self.startPosition.y(),") (",self.midPosition.x(),self.midPosition.y(),") (",self.endPosition.x(),self.endPosition.x(),")")
        print("-----------------------------")

        return

#******************************************************************************
  
class ItemList():
    maximumNodeId=0
    maximumArcId=0
    selectedNodeId=-1

    def AddNodeList(ID,position,text,radius):
        tempList=[ID,position.x(),position.y(),text,radius]
        exec('ItemList.nodeList{}={}'.format(ID,tempList))
        print('add node',ID,exec('print(ItemList.nodeList{}, end=" ")'.format(ID)))

    def AddArcList(startNode,endNode):
        arcId=ItemList.maximumArcId+1
        maximumArcId=ItemList.maximumArcId+1

        tempList=[arcId,(startNode.x,startNode.y),(startNode.x+endNode.x)/2,(startNode.y+endNode.y)/2,endNode.x,endNode.y]
        exec('ItemList.arcList{}={}'.format(arcId,tempList))
        print('add arc',arcId,exec('print(ItemList.arcList{}, end=" ")'.format(arcId)))

#******************************************************************************

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EEE231 Group A")
        self.mainLayout = QVBoxLayout()

        # Create ToolBar
        self.createToolBar()

        # Create MenuBar
        self._createMenuBar()

        # Set mainLayout as the central widget
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        
        # Create graphics scene
        self.graphicsScene = QGraphicsScene(0, 0, 511, 511, self)   # Naughty! Should not be embedding 'magic' constants in a program!!!
        
        #-----------------------------(temp)
        ground = NodeItem(300,300)
        self.graphicsScene.addItem(ground)
        ground.setNodeText("ground")
        ground.nodeId=0
        nodeCentre_G=QPointF(ground.x,ground.y)

        #test = NodeItem(150, 100)
        #self.graphicsScene.addItem(test)
        #test.setNodeText("test")
        #test.setNodeRadius(25)
        #nodeCentre_T=QPointF(test.x,test.y)
        
        #arc1=ArcItem(nodeCentre_G,nodeCentre_T)
        #self.graphicsScene.addItem(arc1)
        #test.arcConnection(arc1)
        #---------------------------------
        
        # Create graphics view
        self.graphicsView = QGraphicsView(self.graphicsScene)
        #self.graphicsView.setDragMode(QGraphicsView.RubberBandDrag)
        #self.graphicsView.setRubberBandSelectionMode(Qt.ContainsItemBoundingRect)
        self.graphicsView.setRenderHints(QPainter.Antialiasing)
        self.mainLayout.addWidget(self.graphicsView)

        # Is a status bar needed in this application?
        self.statusBar = QStatusBar()
        self.mainLayout.addWidget(self.statusBar)

        # Set mainLayout as the central widget
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        
    #-------------------------------------------------------------------

    def _createMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = QMenu("&file", self)
        menuBar.addMenu(fileMenu)

        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&help")
        

    #--------------------------------------------------------------------

    def createToolBar(self):

        # Create toolbar buttons, doesn't seem to work outside main window class
        self.mainToolBar = QToolBar()
        self.mainToolBar.setMovable(False)

        # Add Node button
        self.addNodeB = self.mainToolBar.addAction("+ Node") 
        #QIcon addNodeIcon = QIcon.fromTheme("document new", QIcon(":images/new.png")) # Not sure how the icons work exactly
        self.addNodeB.triggered.connect(self.addNode)

        # Add arc button
        self.addArcB = self.mainToolBar.addAction("+ Arc")
        self.addArcB.triggered.connect(self.addArc) 

        # Delete button
        self.deleteB = self.mainToolBar.addAction("Delete")
        self.deleteB.triggered.connect(self.delete)

        # Save button
        self.saveB = self.mainToolBar.addAction("Save")
        self.saveB.triggered.connect(self.save)   

        # Save as button
        self.saveAsB = self.mainToolBar.addAction("Save As") 
        self.saveAsB.triggered.connect(self.saveAs)

        self.addToolBar(self.mainToolBar) # Setting mainToolBar as a Toolbar
        self.mainLayout.addWidget(self.mainToolBar) # Adding mainToolBar to layout widget

    #-------------------------------------------------------------------

    def addNode(self):
        """Handler for addNode action"""
        tempId=ItemList.maximumNodeId+1
        exec('node{} = NodeItem(200,200)'.format(tempId))
        exec('self.graphicsScene.addItem(node{})'.format(tempId))
        exec('node{}.setNodeText("new node")'.format(tempId))

        ItemList.maximumNodeId=ItemList.maximumNodeId+1 

        exec('ItemList.AddNodeList(node{}.nodeId,QPointF(node{}.x,node{}.y),node{}.nodeText,node{}.nodeRadius)'.format(tempId,tempId,tempId,tempId,tempId))

        arc_n=ArcItem(QPointF(300,300),QPointF(200,200))
        self.graphicsScene.addItem(arc_n)
        exec('node{}.arcConnection(arc_n)'.format(tempId))
        return

    #-------------------------------------------------------------------

    def addArc(self):
        """Handler for addArc action"""
        return
    
    #-------------------------------------------------------------------

    def delete(self):
        """Handler for delete action"""
        return

    #-------------------------------------------------------------------

    def save(self):
        """Handler for save action"""
        return
    
    #-------------------------------------------------------------------

    def saveAs(self):
        """Handler for saveAs action"""
        return

#******************************************************************************

if __name__ == "__main__":
    application = QApplication([])

    mainWindow = MainWindow()
    mainWindow.show()

    exit(application.exec_())