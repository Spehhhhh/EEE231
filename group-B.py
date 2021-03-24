#! /usr/bin/env python3

# Example PySide6 program -- pir -- 22.3.2021

#******************************************************************************
# Insert licence here!



#******************************************************************************

from sys import exit

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtWidgets import QToolBar, QStatusBar
from PySide6.QtWidgets import QFileDialog, QMessageBox

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QBrush
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsSimpleTextItem, QGraphicsItemGroup

#******************************************************************************

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Invoke __init__ of QMainWindow base class

        self.setWindowTitle("EEE231 Group B Program")
        self.mainLayout = QVBoxLayout()

        # Setup menu bar & File menu
        self.fileMenu = self.menuBar().addMenu("&File")
        self.openMenuAction = self.fileMenu.addAction("&Open")
        self.openMenuAction.triggered.connect(self.on_open_action)    # New-style connect!
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
        self.graphicsScene = QGraphicsScene(0, 0, 511, 511, self)   # Naughty! Should not be embedding 'magic' constants in a program!!!
        
        # Set node fill colour
        nodeFillColour = QColor(226, 170, 243)	# Ditto!
        nodeFillBrush = QBrush(Qt.black, Qt.SolidPattern)   
        nodeFillBrush.setColor(nodeFillColour)
        
        # Create example node graphics item (1)
        x1 = 100.0
        y1 = 100.0  
        self.nodeRadius = 25.0
        nodeCentre_1 = QPointF(x1,y1)
        rect_1 = QRectF(x1 - self.nodeRadius, y1 - self.nodeRadius, 2.0 * self.nodeRadius, 2.0 * self.nodeRadius)	# Bounding rectangle of node 'ellipse'
        nodeGraphicsItem_1 = QGraphicsEllipseItem(rect_1)	# NB. Parameter defines the bounding rectangle of the ellipse!
        nodeGraphicsItem_1.setZValue(0)
        nodeGraphicsItem_1.setBrush(nodeFillBrush)	
        nodeGraphicsItem_1.setToolTip("this is node 1")
          
        nodeTextItem_1 = QGraphicsSimpleTextItem("Node 1")
        boundingRect_1 = nodeTextItem_1.boundingRect()
        nodeTextItem_1.setPos(nodeCentre_1.x() - boundingRect_1.width()/2, nodeCentre_1.y() - boundingRect_1.height() / 2)
        nodeGraphicsGroup_1 = QGraphicsItemGroup()
        nodeGraphicsGroup_1.addToGroup(nodeGraphicsItem_1)
        nodeGraphicsGroup_1.addToGroup(nodeTextItem_1)
        self.graphicsScene.addItem(nodeGraphicsGroup_1)

        # Create example node graphics item (1)
        x2 = 100.0
        y2 = 200.0
        nodeCentre_2 = QPointF(x2, y2)
        rect_2 = QRectF(x2 - self.nodeRadius, y2 - self.nodeRadius, 2.0 * self.nodeRadius, 2.0 * self.nodeRadius)
        nodeGraphicsItem_2 = QGraphicsEllipseItem(rect_2)
        nodeGraphicsItem_2.setZValue(0)
        nodeGraphicsItem_2.setBrush(nodeFillBrush)	
        nodeGraphicsItem_2.setToolTip("this is node 2")
        
        nodeTextItem_2 = QGraphicsSimpleTextItem("Node 2")
        boundingRect_2 = nodeTextItem_1.boundingRect()
        nodeTextItem_2.setPos(nodeCentre_2.x() - boundingRect_2.width()/2, nodeCentre_2.y() - boundingRect_2.height() / 2)
        nodeGraphicsGroup_2 = QGraphicsItemGroup()
        nodeGraphicsGroup_2.addToGroup(nodeGraphicsItem_2)
        nodeGraphicsGroup_2.addToGroup(nodeTextItem_2)
        self.graphicsScene.addItem(nodeGraphicsGroup_2)    
        
        # Create example arc (1)
        arc_PainterPath_1 = QPainterPath(nodeCentre_1)
        ctrlX_1 = 50.0
        ctrlY_1 = 150.0
        arc_PainterPath_1.quadTo(ctrlX_1, ctrlY_1, nodeCentre_2.x(), nodeCentre_2.y())
        arcGraphicItem_1 = QGraphicsPathItem(arc_PainterPath_1)
        arcGraphicItem_1.setZValue(-1)	# Hides path below nodes
        arcGraphicItem_1.setToolTip("arc 1")
        self.graphicsScene.addItem(arcGraphicItem_1)
        
        # Create example arc (2)
        arc_PainterPath_2 = QPainterPath(nodeCentre_1)
        ctrlX_2 = 150.0
        ctrlY_2 = 150.0
        arc_PainterPath_2.quadTo(ctrlX_2, ctrlY_2, nodeCentre_2.x(), nodeCentre_2.y())
        arcGraphicItem_2 = QGraphicsPathItem(arc_PainterPath_2)
        arcGraphicItem_2.setZValue(-1)	# Hides path below nodes
        arcGraphicItem_2.setToolTip("arc 2")
        self.graphicsScene.addItem(arcGraphicItem_2)
          
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

    #--------------------------------------------------------------------------

    def on_open_action(self):
        """Handler for 'Open' action"""
        fileName = QFileDialog.getOpenFileName(self, "Open File", ".", ("*.md"))
        print("opening ", fileName[0])
        return
        
    #--------------------------------------------------------------------------
    
    def on_quit_action(self):
        """Handler for 'Quit' action"""
        print("quitting application")
        self.close()  
        return
    #--------------------------------------------------------------------------
       
    def on_preferences_action(self):
        """Handler for 'Preferences' action"""
        print("preferences")
        return
        
    #--------------------------------------------------------------------------
    
    def on_about_action(self):
        """Handler for 'About' action"""
        QMessageBox.about(self, "About this program", "some about text crediting the people who wrote this")
        return
        
#******************************************************************************

# Main program
if __name__ == "__main__":
    application = QApplication([])

    mainWindow = MainWindow()
    mainWindow.show()

    exit(application.exec_())   # Not sure why this still has to be `exec_` with a trailing underscore? Despite what the documentation says...

#******************************************************************************
