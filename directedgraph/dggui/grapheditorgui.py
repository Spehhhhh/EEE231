from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtGui import QAction, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QInputDialog,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtWidgets import (
    QMenu,
    QFileDialog,
    QMessageBox,
    QGraphicsScene,
    QGraphicsView,
)

import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import Node, SourceNode, GroundNode, Arc, Graph
from directedgraph.dggui import (
    NodeItem,
    SourceNodeItem,
    GroundNodeItem,
    ArcItem,
    InputDialogArc,
)
from directedgraph.dgutils import FileManager, GraphSimulator


class DirectedGraphScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(DirectedGraphScene, self).__init__(0, 0, 1280, 720, parent)
        self.selected_items = []

    def mouseReleaseEvent(self, event):
        pass
        # if event.button() == 2:  # Right mouse click
        #     # Set previous selections selected
        #     for item in self.prevItem:
        #         item.setSelected(1)

        #     item = self.itemAt(event.lastScenePos().x(), event.lastScenePos().y())
        #     if item:
        #         item.setSelected(1)

        # if event.button() == 1:  # Left mouse click
        #     # Get selected item
        #     items = self.selectedItems()

        #     # Shift click
        #     if event.modifiers() & QtCore.Qt.ShiftModifier:
        #         # Set previous items selected
        #         for item in self.prevItem:
        #             item.setSelected(1)

        #         for item in items:
        #             self.prevItem.append(item)

        #         item = self.itemAt(event.scenePos(), QtGui.QTransform())
        #         if item == None:
        #             self.clearSelection()

        #         # print(self.prevItem)

        #     else:
        #         self.prevItem = []
        #         for item in items:
        #             self.prevItem.append(item)

        # super(DirectedGraphScene, self).mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        if event.modifiers() & QtCore.Qt.ShiftModifier:
            item = self.itemAt(event.scenePos(), QtGui.QTransform())
            # print(type(item))
            if item:
                if type(item) in [NodeItem, SourceNodeItem, GroundNodeItem]:
                    item.selectionRectangle.setVisible(True)
                    if item in self.selected_items:
                        pass
                    else:
                        self.selected_items.append(item)
                        print(self.selected_items)
        else:
            for item in self.selected_items:
                item.selectionRectangle.setVisible(False)
            self.selected_items.clear()

        super(DirectedGraphScene, self).mousePressEvent(event)


class DirectedGraphMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Title of the Windows
        self.setWindowTitle("Graph Editor")

        # Initialise the QGraphicScene
        self.scene = DirectedGraphScene(self)
        self.view = QGraphicsView(self.scene)

        # self.view.setRenderHints(QPainter.Antialiasing) # Performance optimisation
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Set up the Menu Bar
        self.FileMenu = self.menuBar().addMenu("&File")

        self.openMenuAction = self.FileMenu.addAction("&Open...")
        self.openMenuAction.triggered.connect(self.on_open_action)

        self.saveMenuAction = self.FileMenu.addAction("&Save")
        self.saveMenuAction.triggered.connect(self.on_save_action)

        self.saveAsMenuAction = self.FileMenu.addAction("&Save As...")
        self.saveAsMenuAction.triggered.connect(self.on_save_as_action)

        # Setup Graph Component menu
        self.GraphComponentMenu = self.menuBar().addMenu("&Edit")

        self.NodeAction = self.GraphComponentMenu.addAction("&Add Node")
        self.NodeAction.triggered.connect(self.on_node_action)

        self.SourceNodeAction = self.GraphComponentMenu.addAction("&Add Source Node")
        self.SourceNodeAction.triggered.connect(self.on_sourcenode_action)

        self.GroundNodeAction = self.GraphComponentMenu.addAction("&Add Ground Node")
        self.GroundNodeAction.triggered.connect(self.on_groundnode_action)

        self.ArcAction = self.GraphComponentMenu.addAction("&Add Arc")
        self.ArcAction.triggered.connect(self.on_arc_action)

        self.ActionMenu = self.menuBar().addMenu("&Action")
        self.SimulateAction = self.ActionMenu.addAction("&Export Simulation File...")
        self.SimulateAction.triggered.connect(self.on_simulate_action)

        self.graph = Graph()
        self.file_path = ""
        # self.mouse_position = None

    # Menu
    def contextMenuEvent(self, event):
        contextmenu = QMenu(self)

        # self.mouse_position = self.mapToParent(event.pos())

        # print("contextMenuEvent", self.mouse_position)

        # newaction = QAction("New Component")
        # contextmenu.addAction(newaction)
        # newaction.triggered.connect()

        reloadaction = QAction("Reload")
        contextmenu.addAction(reloadaction)
        reloadaction.triggered.connect(self.on_reload_action)
        contextmenu.addSeparator()

        newnodeaction = QAction("New Node")
        contextmenu.addAction(newnodeaction)
        newnodeaction.triggered.connect(self.on_node_action)

        newsourcenodeaction = QAction("New Source Node")
        contextmenu.addAction(newsourcenodeaction)
        newsourcenodeaction.triggered.connect(self.on_sourcenode_action)

        newgroundnodeaction = QAction("New Ground Node")
        contextmenu.addAction(newgroundnodeaction)
        newgroundnodeaction.triggered.connect(self.on_groundnode_action)

        newarcaction = QAction("New Arc Using UID")
        contextmenu.addAction(newarcaction)
        newarcaction.triggered.connect(self.on_arc_action)

        newarcshiftaction = QAction("New Arc Using SHIFT Selection")
        contextmenu.addAction(newarcshiftaction)
        newarcshiftaction.triggered.connect(self.on_arc_shift_action)

        contextmenu.addSeparator()

        openaction = QAction("Open...")
        contextmenu.addAction(openaction)
        openaction.triggered.connect(self.on_open_action)

        saveaction = QAction("Save")
        contextmenu.addAction(saveaction)
        saveaction.triggered.connect(self.on_save_action)

        saveasaction = QAction("Save As...")
        contextmenu.addAction(saveasaction)
        saveasaction.triggered.connect(self.on_save_as_action)

        contextmenu.addSeparator()

        helpaction = QAction("Help...")
        contextmenu.addAction(helpaction)
        helpaction.triggered.connect(self.on_about_action)

        action = contextmenu.exec_(self.mapToGlobal(event.pos()))

        # self.scene.addItem(ArcItem(None, self))

    def on_reload_action(self):
        self.reset_scene()
        fm = FileManager()
        self.graph = fm.open_graph(self.file_path)
        for component in self.graph.components.values():
            if type(component) == Node:
                self.scene.addItem(NodeItem(component, self))
            if type(component) == SourceNode:
                self.scene.addItem(SourceNodeItem(component, self))
            if type(component) == GroundNode:
                self.scene.addItem(GroundNodeItem(component, self))
            if type(component) == Arc:
                self.scene.addItem(ArcItem(component, self))

    # Trigger Function
    def on_open_action(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", ".", ("*.xml"))
        self.file_path = str(file_name[0])

        self.reset_scene()

        fm = FileManager()
        graph1 = fm.open_graph(str(file_name[0]))

        for component in graph1.components.values():
            if type(component) == Node:
                self.scene.addItem(NodeItem(component, self))
            if type(component) == SourceNode:
                self.scene.addItem(SourceNodeItem(component, self))
            if type(component) == GroundNode:
                self.scene.addItem(GroundNodeItem(component, self))
            if type(component) == Arc:
                self.scene.addItem(ArcItem(component, self))

        self.graph = graph1

        return

    def on_save_action(self):
        alert = self.graph.verify_graph_integrity()
        if len(alert) == 0:
            if self.file_path == "":
                QMessageBox.about(
                    self,
                    "Error",
                    "Please Use Save as...",
                )
            else:
                fm = FileManager()
                fm.export_graph_xml(self.file_path, self.graph)
        else:
            for alert_message in alert:
                QMessageBox.about(
                    self,
                    "Error",
                    alert_message,
                )
        return

    def on_save_as_action(self):
        alert = self.graph.verify_graph_integrity()
        if len(alert) == 0:
            fm = FileManager()
            file_name = QtWidgets.QFileDialog.getSaveFileName(self, "Save File")
            fm.export_graph_xml(file_name[0], self.graph)
            self.file_path = file_name[0]  # 把路径保存到实例中
        else:
            for alert_message in alert:
                QMessageBox.about(
                    self,
                    "Error",
                    alert_message,
                )
        return

    def on_preferences_action(self):
        return

    def on_about_action(self):
        QMessageBox.about(
            self,
            "About this program",
            "https://github.com/pirlite2/EEE231-group-B",
        )
        return

    def on_node_action(self):
        name = ""
        text, result = QInputDialog.getText(
            self,
            "Input",
            "Enter Name",
            QtWidgets.QLineEdit.Normal,
        )
        if result == True:
            name = str(text)

        # print("on_node_action", self.mouse_position)

        self.scene.addItem(
            NodeItem(
                self.graph.create_component(
                    {
                        "type": "Node",
                        "name": name,
                        "position_x": "500",
                        "position_y": "500",
                    }
                ),
                self,
            )
        )
        return

    def on_sourcenode_action(self):

        name = ""
        text, result = QInputDialog.getText(
            self,
            "Input",
            "Enter Name",
            QtWidgets.QLineEdit.Normal,
        )
        if result == True:
            name = str(text)

        user_defined_attribute = ""
        text, result = QInputDialog.getText(
            self,
            "Input",
            "Enter User Defined Attribute",
            QtWidgets.QLineEdit.Normal,
        )
        if result == True:
            user_defined_attribute = str(text)

        self.scene.addItem(
            SourceNodeItem(
                self.graph.create_component(
                    {
                        "type": "SourceNode",
                        "name": name,
                        "position_x": "500",
                        "position_y": "500",
                        "user_defined_attribute": user_defined_attribute,
                    }
                ),
                self,
            )
        )
        return

    def on_groundnode_action(self, event):
        name = ""
        text, result = QInputDialog.getText(
            self,
            "Input",
            "Enter Name",
            QtWidgets.QLineEdit.Normal,
        )
        if result == True:
            name = str(text)

        self.scene.addItem(
            NodeItem(
                self.graph.create_component(
                    {
                        "type": "GroundNode",
                        "name": name,
                        "position_x": "500",
                        "position_y": "500",
                    }
                ),
                self,
            )
        )
        return

    def on_arc_action(self):
        input_dialog_arc = InputDialogArc()
        input_dialog_arc.show()
        input_dialog_arc.exec_()
        uid_list = input_dialog_arc.confirm()
        if uid_list[0] in self.graph.components:
            if uid_list[1] in self.graph.components:
                self.scene.addItem(
                    ArcItem(
                        self.graph.create_component(
                            {
                                "type": "Arc",
                                "name": uid_list[0],
                                "node1_uid": uid_list[1],
                                "node2_uid": uid_list[2],
                                "user_defined_arc_type": uid_list[3],
                                "user_defined_attribute": uid_list[4],
                            }
                        ),
                        self,
                    )
                )
        else:
            QMessageBox.about(
                self,
                "Error",
                "Wrong UID",
            )
        return

    def on_arc_shift_action(self):
        input_dialog_arc = InputDialogArc()
        input_dialog_arc.show()
        input_dialog_arc.exec_()
        uid_list = input_dialog_arc.confirm()
        if len(self.scene.selected_items) == 2:
            self.scene.addItem(
                ArcItem(
                    self.graph.create_component(
                        {
                            "type": "Arc",
                            "name": uid_list[0],
                            "node1_uid": self.scene.selected_items[0].node.uid,
                            "node2_uid": self.scene.selected_items[1].node.uid,
                            "user_defined_arc_type": uid_list[3],
                            "user_defined_attribute": uid_list[4],
                        }
                    ),
                    self,
                )
            )
        else:
            QMessageBox.about(
                self,
                "Error",
                "You need to select two Node",
            )

    def on_simulate_action(self):
        alert = self.graph.verify_graph_integrity()
        if len(alert) == 0:
            file_name = QtWidgets.QFileDialog.getSaveFileName(self, "Save File")
            sm = GraphSimulator()
            sm.export(file_name[0], self.graph)
        else:
            for alert_message in alert:
                QMessageBox.about(
                    self,
                    "Error",
                    alert_message,
                )
        return

    # Other Function
    def reset_scene(self):
        for item in self.scene.items():
            item.on_delete_action()
        return


if __name__ == "__main__":
    app = QApplication([])
    mainwindow = DirectedGraphMainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
