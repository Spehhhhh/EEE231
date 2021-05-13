import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dgcore import Node, SourceNode, GroundNode, Arc


class Graph:
    """
    init Graph()
    """

    def __init__(self, name=None):
        self.name = name if name else "Untitled"
        self.components = {}

    """
    Control Graph()
    """

    def get(self):
        return True

    def get_name(self):
        return self.name

    def update_name(self, name):
        self.name = name

    # #TODO
    def verify_graph_integrity(self):
        groundnode_counter = 0
        for key in self.components:
            if self.components[key]["type"] == "GroundNode":
                groundnode_counter += 1
        if groundnode_counter != 1:
            return False
        else:
            return True

    # For debugging Graph
    def print_graph_details(self):
        print("------------------------------------")
        print("Graph vars(self):")
        print(vars(self))
        print("------------------------------------")
        print("Graph Components:")
        for (
            component_uid,
            component,
        ) in self.components.items():
            print(
                "UID:",
                component.uid,
                "|",
                "Name:",
                component.name,
            )

    """
    Control GraphComponent()
    """

    def get_component(self, uid):
        # print(self.components[uid].get_name())
        # print("parent_graph:", self.components[uid].get_parent_graph())
        # print(vars(self.components[uid])) # 可以返回对象也可以返回字典
        return self.components[uid]

    # #TODO 按参数里的字典新建组件
    def create_component(self, parameters):
        if parameters.get("type", None) == "Node":
            component = Node(
                self,
                parameters.get("uid", None),
                parameters.get("name", None),
                parameters.get("colour", None),
                [
                    int(parameters.get("position_x", 0)),
                    int(parameters.get("position_y", 0)),
                ],
            )
            self.insert_component(component)
            return component
        elif parameters.get("type", None) == "SourceNode":
            component = SourceNode(
                self,
                parameters.get("uid", None),
                parameters.get("name", None),
                parameters.get("colour", None),
                [
                    int(parameters.get("position_x", 0)),
                    int(parameters.get("position_y", 0)),
                ],
                parameters.get("user_defined_attribute", None),
            )
            self.insert_component(component)
            return component
        elif parameters.get("type", None) == "GroundNode":
            component = GroundNode(
                self,
                parameters.get("uid", None),
                parameters.get("name", None),
                [
                    int(parameters.get("position_x", 0)),
                    int(parameters.get("position_y", 0)),
                ],
                parameters.get("position", None),
            )
            self.insert_component(component)
            return component
        elif parameters.get("type", None) == "Arc":
            component = Arc(
                self,
                parameters.get("uid", None),
                parameters.get("name", None),
                parameters.get("colour", None),
                parameters.get("node1", None),
                parameters.get("node2", None),
                parameters.get("user_define_attribute",None),
                parameters.get("Impedance",None)
            )
            self.insert_component(component)
            return component
        else:
            print("Error: Component Type")

    def insert_component(self, component):
        self.components[component.get_uid()] = component

    def update_component_name(self, uid, name):
        self.components[uid].name = name

    def update_component_colour(self, uid, colour):
        self.components[uid].colour = colour

    # def update_arc_position(uid, uid, uid):
    # def update_arc_position(uid, node1, node2):
    # def update_arc_position(arc1, node1, node2):
    def update_arc_position(self, arc1, node1, node2):
        if isinstance(arc1, Arc):
            arc1.update_position(node1, node2)
        elif isinstance(arc1, str):
            if len(node2) == 12 and self.parent_graph == self:
                self.get_component["arc1"].update_position(node1, node2)

    # #TODO 需要写误删除逻辑
    def delete_component(self, uid):
        if uid in self.components:
            self.components.pop(uid)
            return True
        else:
            return False


if __name__ == "__main__":
    import unittest
    from tests.test_dgcore import TestGraph
    unittest.main()  # Run Unit tests
