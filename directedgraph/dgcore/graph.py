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
        self.connected_gui = None
        self.groundnode_counter = 0
        self.arc_counter = 0

        self.name = name if name else "Untitled"
        self.components = {}

    """
    Control Graph()
    """

    def get(self):
        graph_attribute = []
        graph_attribute.append({"name": self.name})

        graph_components = []
        for component in self.components.values():
            if type(component) == Arc:
                component_dict = {}
                component_dict["type"] = "Arc"
                component_dict["uid"] = str(component.uid)
                component_dict["name"] = str(component.name)
                component_dict["colour"] = str(component.colour)
                component_dict["node1_uid"] = str(component.nodes[0].uid)
                component_dict["node2_uid"] = str(component.nodes[1].uid)
                component_dict["user_defined_attribute"] = str(
                    component.user_defined_attribute
                )
                component_dict["user_defined_arc_type"] = str(
                    component.user_defined_arc_type
                )
                graph_components.append(component_dict)
            elif type(component) == Node:
                component_dict = {}
                component_dict["type"] = "Node"
                component_dict["uid"] = str(component.uid)
                component_dict["name"] = str(component.name)
                component_dict["colour"] = str(component.colour)
                component_dict["position_x"] = str(component.position[0])
                component_dict["position_y"] = str(component.position[1])
                graph_components.append(component_dict)
            elif type(component) == SourceNode:
                component_dict = {}
                component_dict["type"] = "SourceNode"
                component_dict["uid"] = str(component.uid)
                component_dict["name"] = str(component.name)
                component_dict["colour"] = str(component.colour)
                component_dict["position_x"] = str(component.position[0])
                component_dict["position_y"] = str(component.position[1])
                component_dict["user_defined_attribute"] = str(
                    component.user_defined_attribute
                )
                graph_components.append(component_dict)
            elif type(component) == GroundNode:
                component_dict = {}
                component_dict["type"] = "GroundNode"
                component_dict["uid"] = str(component.uid)
                component_dict["name"] = str(component.name)
                component_dict["colour"] = str(component.colour)
                component_dict["position_x"] = str(component.position[0])
                component_dict["position_y"] = str(component.position[1])
                graph_components.append(component_dict)
            else:
                pass
        return (graph_attribute, graph_components)

    def get_name(self):
        return self.name

    def update_name(self, name):
        self.name = name

    def update_component_node_arcs(self):
        self.arc_counter = 0
        components_values = self.components.values()

        for component_inst in components_values:
            if isinstance(component_inst, Node):
                component_inst.arcs.clear()

        for component_inst in components_values:
            if type(component_inst) == Arc:
                self.arc_counter += 1
                component_inst.nodes[0].arcs.append(component_inst)
                component_inst.nodes[1].arcs.append(component_inst)

    def verify_graph_integrity(self):
        return_list = []
        return_list.clear()
        components_values = self.components.values()
        self.groundnode_counter = 0
        self.arc_counter = 0

        # Only one Ground Node is allowed
        for component_inst in components_values:
            if type(component_inst) == GroundNode:
                self.groundnode_counter += 1
        if self.groundnode_counter != 1:
            return_list.append("Only one Ground Node is allowed")
        else:
            pass

        # Source only allows single arcs
        self.update_component_node_arcs()

        for component_inst in components_values:
            if type(component_inst) == SourceNode:
                if len(component_inst.arcs) > 1:
                    return_list.append("Source only allows single arcs")

        if self.arc_counter > 50:
            return_list.append("Too many Arcs")

        return return_list

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
        # print("connected_graph:", self.components[uid].get_connected_graph())
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
                parameters.get("colour", None),
                [
                    int(parameters.get("position_x", 0)),
                    int(parameters.get("position_y", 0)),
                ],
            )
            self.insert_component(component)
            return component
        elif parameters.get("type", None) == "Arc":
            component = Arc(
                self,
                parameters.get("uid", None),
                parameters.get("name", None),
                parameters.get("colour", None),
                parameters.get("node1_uid", None),
                parameters.get("node2_uid", None),
                parameters.get("user_defined_attribute", None),
                parameters.get("user_defined_arc_type", None),
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
        if type(arc1) == Arc:
            arc1.update_position(node1, node2)
        elif isinstance(arc1, str):
            if len(node2) == 12 and self.connected_graph == self:
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
    from tests.test_dgcore_graph import TestGraph

    unittest.main()  # Run Unit tests
