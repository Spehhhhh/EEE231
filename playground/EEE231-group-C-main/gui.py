import sys
import random

from PySide6 import QtCore
from PySide6.QtCore import Qt



from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtWidgets import QToolBar, QStatusBar, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #
        self.setWindowTitle("Graph Creator Group C")
        
        self.fileMenu = self.menuBar().addMenu("&File")
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.toolsMenu = self.menuBar().addMenu("&Tools")


        # File menu
        
        self.newMenuAction = self.fileMenu.addAction("&New File")
        self.newMenuAction.setShortcut("CTRL+N")
        self.newMenuAction.triggered.connect(self.on_new_action)
        
        self.openMenuAction = self.fileMenu.addAction("&Open")
        self.openMenuAction.setShortcut("CTRL+O")
        self.openMenuAction.triggered.connect(self.on_open_action)
        
        self.saveMenuAction = self.fileMenu.addAction("&Save")
        self.saveMenuAction.setShortcut("CTRL+S")
        self.saveMenuAction.triggered.connect(self.on_save_action)
        
        self.saveAsMenuAction = self.fileMenu.addAction("&Save As...")
        self.saveAsMenuAction.setShortcut("CTRL+Shift+S")
        self.saveAsMenuAction.triggered.connect(self.on_saveAs_action)
        
        self.fileMenu.addSeparator()
        
        self.exportMenuAction = self.fileMenu.addAction("&Export...")
        self.exportMenuAction.triggered.connect(self.on_export_action)
        
        self.fileMenu.addSeparator()
        
        self.quitMenuAction = self.fileMenu.addAction("&Quit")
        self.quitMenuAction.triggered.connect(self.on_quit_action)
        
        
        
        
        # Edit menu
        
        self.undoMenuAction = self.editMenu.addAction("&Undo")
        self.undoMenuAction.setShortcut("CTRL+Z")
        self.undoMenuAction.triggered.connect(self.on_undo_action)
        
        self.redoMenuAction = self.editMenu.addAction("&Redo")
        self.redoMenuAction.setShortcut("CTRL+Y")
        self.redoMenuAction.triggered.connect(self.on_redo_action)
        
        self.editMenu.addSeparator()
        
        self.cutMenuAction = self.editMenu.addAction("&Cut")
        self.cutMenuAction.setShortcut("CTRL+X")
        self.cutMenuAction.triggered.connect(self.on_cut_action)
        
        self.copyMenuAction = self.editMenu.addAction("&Copy")
        self.copyMenuAction.setShortcut("CTRL+C")
        self.copyMenuAction.triggered.connect(self.on_copy_action)
        
        self.pasteMenuAction = self.editMenu.addAction("&Paste")
        self.pasteMenuAction.setShortcut("CTRL+V")
        self.pasteMenuAction.triggered.connect(self.on_paste_action)
        
        self.editMenu.addSeparator()
        
        self.preferencesMenuAction = self.editMenu.addAction("&Preferences")
        self.preferencesMenuAction.triggered.connect(self.on_preferences_action)
        
        
        # Tools menu
        
        self.nodeMenuAction = self.toolsMenu.addAction("&Node")
        self.nodeMenuAction.setShortcut("N")
        self.nodeMenuAction.triggered.connect(self.on_node_action)
        
        self.arcMenuAction = self.toolsMenu.addAction("&Arc")
        self.arcMenuAction.setShortcut("A")
        self.arcMenuAction.triggered.connect(self.on_arc_action)
        
        self.currentMenuAction = self.toolsMenu.addAction("&Current Source")
        self.currentMenuAction.setShortcut("C")
        self.currentMenuAction.triggered.connect(self.on_current_action)
        
        self.groundMenuAction = self.toolsMenu.addAction("&Ground Node")
        self.groundMenuAction.setShortcut("G")
        self.groundMenuAction.triggered.connect(self.on_ground_action)
        
        self.deleteMenuAction = self.toolsMenu.addAction("&Delete Node")
        self.deleteMenuAction.setShortcut("X")
        self.deleteMenuAction.triggered.connect(self.on_delete_action)
        
        
        
        # About menu
        self.aboutMenu = self.menuBar().addMenu("&About")
        self.aboutMenuAction = self.aboutMenu.addAction("&About")
        self.aboutMenuAction.triggered.connect(self.on_about_action)
        
        # Main toolbar
        self.mainToolBar = QToolBar()
        self.mainToolBar.setMovable(True)
        
        
        
        self.nodeToolButton = self.mainToolBar.addAction("Node")
        self.nodeToolButton.triggered.connect(self.on_node_action)
           
        self.arcToolButton = self.mainToolBar.addAction("Arc")
        self.arcToolButton.triggered.connect(self.on_arc_action)
        
        self.currentToolButton = self.mainToolBar.addAction("Current")
        self.currentToolButton.triggered.connect(self.on_current_action) 
        
        self.groundToolButton = self.mainToolBar.addAction("Ground")    
        self.groundToolButton.triggered.connect(self.on_ground_action)
         
        self.deleteToolButton = self.mainToolBar.addAction("Delete")   
        self.deleteToolButton.triggered.connect(self.on_delete_action)
        
           
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        
        
        #Main Widget
        self.mainWidget = QLabel("Test")
        self.mainWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.mainWidget)
        
        
        
    #File Menu Handlers
        
        
        #--------------------------------------------------------------------------

    def on_new_action(self):
        """Handler for 'New File' action"""
        print("new file ")
        return
        
        #--------------------------------------------------------------------------

    def on_open_action(self):
        """Handler for 'Open' action"""
        print("open file")
        return
    #--------------------------------------------------------------------------

    def on_save_action(self):
        """Handler for 'Save' action"""
        print("save")
        return
    #--------------------------------------------------------------------------

    def on_saveAs_action(self):
        """Handler for 'Save As...' action"""
        print("save as")
        return
    #--------------------------------------------------------------------------

    def on_export_action(self):
        """Handler for 'Export...' action"""
        print("export")
        return
    
    #--------------------------------------------------------------------------

    def on_quit_action(self):
        """Handler for 'Quit' action"""
        self.close()
        print("quit")
        return
    
    #Edit Menu Handlers
        
        
        #--------------------------------------------------------------------------

    def on_undo_action(self):
        """Handler for 'Undo' action"""
        print("Undo")
        return
        
        #--------------------------------------------------------------------------

    def on_redo_action(self):
        """Handler for 'Redo' action"""
        print("Redo")
        return
    #--------------------------------------------------------------------------

    def on_cut_action(self):
        """Handler for 'Cut' action"""
        print("Cut")
        return
    #--------------------------------------------------------------------------

    def on_copy_action(self):
        """Handler for 'Copy' action"""
        print("Copy")
        return
    #--------------------------------------------------------------------------

    def on_paste_action(self):
        """Handler for 'Paste' action"""
        print("Paste")
        return
    
    #--------------------------------------------------------------------------

    def on_preferences_action(self):
        """Handler for 'Preferences' action"""
        self.close()
        print("Preferences")
        return
    
    #Tools Menu Handlers
        
        
        #--------------------------------------------------------------------------

    def on_node_action(self):
        """Handler for 'Node' action"""
        print("Node")
        return
    
        #--------------------------------------------------------------------------

    def on_arc_action(self):
        """Handler for 'Arc' action"""
        print("Arc")
        return
    
        #--------------------------------------------------------------------------

    def on_current_action(self):
        """Handler for 'Current' action"""
        print("Current")
        return
    
        #--------------------------------------------------------------------------

    def on_ground_action(self):
        """Handler for 'Ground' action"""
        print("Ground")
        return
    
        #--------------------------------------------------------------------------

    def on_delete_action(self):
        """Handler for 'Delete' action"""
        print("Delete")
        return
    
    
    
    #About Menu Handlers
        
        
        #--------------------------------------------------------------------------

    def on_about_action(self):
        """Handler for 'About' action"""
        print("About")
        return
        
        
        
        
        
        
        
        
if __name__ == "__main__":
    app = QApplication([])

    
    mainWindow = MainWindow()
    mainWindow.resize(1920,1080)
    mainWindow.show()

    sys.exit(app.exec_())
        
    
